from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

hoje = datetime.today()
primeiro_dia = datetime(2023, 1, 1)
dias = (hoje - primeiro_dia).days

print('### Iniciando a raspagem da agenda presidencial...')
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})
url = f'https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica-lula/agenda-do-presidente-da-republica/{hoje.strftime("%Y-%m-%d")}'

print('#>> Fazendo a requisição da primeira página da agenda...')
requisicao = session.get(url).content
soup = BeautifulSoup(requisicao, 'lxml')

agenda = []

print('   >>> Iniciando o loop de raspagem da agenda...')
for i in tqdm(range(dias)):
    compromissos = soup.find_all('li', {'class': 'item-compromisso-wrapper'})
    for compromisso in compromissos:
        data = url.split('/')[-1]
        horario = compromisso.find('time', {'class': 'compromisso-inicio'}).text
        data_hora = data + ' ' + horario.replace('h', ':') + ':00'
        titulo = compromisso.find('h2', {'class': 'compromisso-titulo'}).text
        if compromisso.find('div', {'class': 'compromisso-local'}):
            local = compromisso.find('div', {'class': 'compromisso-local'}).text
        else:
            local = ''
        dados = {'data_hora': data_hora, 'data': data, 'horario': horario, 'titulo': titulo, 'local': local}
        agenda.append(dados)

    if soup.find('a', {'class': 'previous'}):
        url = soup.find('a', {'class': 'previous'}).get('href')
        requisicao = session.get(url).content
        soup = BeautifulSoup(requisicao, 'lxml')
    else:
        break

print('   >>> Salvando a agenda em um arquivo Excel...')
agenda = pd.DataFrame(agenda)
agenda.to_excel('bases/agenda_presidencial.xlsx', index=False)
print('   >>> Fim da raspagem da agenda presidencial!')
