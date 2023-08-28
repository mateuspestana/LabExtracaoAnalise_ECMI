from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import concurrent.futures
import time


inicio = time.time()
hoje = datetime.today()
primeiro_dia = datetime(2023, 1, 1)
dias = (hoje - primeiro_dia).days

print('### Iniciando a raspagem da agenda presidencial...')
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

url = f'https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica-lula/agenda-do-presidente-da-republica/{hoje.strftime("%Y-%m-%d")}'
urls = []
while url:
    urls.append(url)
    print(f'Baixando dia {url.split("/")[-1]}...')
    content = session.get(url).content
    soup = BeautifulSoup(content, 'lxml')
    prev_link = soup.find('a', {'class': 'previous'})
    url = prev_link.get('href') if prev_link else None


def scrape_url(url):
    local_agenda = []
    content = session.get(url).content
    soup = BeautifulSoup(content, 'lxml')

    compromissos = soup.find_all('li', {'class': 'item-compromisso-wrapper'})
    for compromisso in compromissos:
        data = url.split('/')[-1]
        horario = compromisso.find('time', {'class': 'compromisso-inicio'}).text
        data_hora = data + ' ' + horario.replace('h', ':') + ':00'
        titulo = compromisso.find('h2', {'class': 'compromisso-titulo'}).text
        local = compromisso.find('div', {'class': 'compromisso-local'}).text if compromisso.find('div', {
            'class': 'compromisso-local'}) else ''
        dados = {'data_hora': data_hora, 'data': data, 'horario': horario, 'titulo': titulo, 'local': local}
        local_agenda.append(dados)

    return local_agenda

agenda = []
print('   >>> Iniciando o loop de raspagem da agenda...')
with concurrent.futures.ThreadPoolExecutor(50) as executor:
    results = list(tqdm(executor.map(scrape_url, urls), total=len(urls)))

    for result in results:
        agenda.extend(result)

print('   >>> Salvando a agenda em um arquivo Excel...')
agenda_df = pd.DataFrame(agenda)
agenda_df.to_excel('agenda_presidencial.xlsx', index=False)
print('   >>> Fim da raspagem da agenda presidencial!')
print(f'Tempo de execução: {time.time() - inicio} segundos')