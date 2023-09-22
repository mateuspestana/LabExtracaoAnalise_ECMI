# Projetos de Webscraping
import time

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm
import re


# Webscraping Letras
session = requests.Session()
url = 'https://www.letras.mus.br/jorge-aragao/'
requisicao = session.get(url).content
soup = BeautifulSoup(requisicao, 'lxml')
musicas = soup.find_all('li', {'class': 'songList-table-row'})
lista_letras = []
for musica in tqdm(musicas):
    titulo = musica.find('span').text
    url_musica = 'https://www.letras.mus.br' + musica.find('a').get('href')
    requisicao_musica = session.get(url_musica).content
    letra_page = BeautifulSoup(requisicao_musica, 'lxml')
    letra = letra_page.find('div', {'class': 'lyric-original'}).text
    exibicoes = letra_page.find('div', {'class': 'head-info-exib'}).find('b').text
    exibicoes = int(exibicoes.replace('.', ''))
    dados = {'titulo': titulo, 'url': url_musica, 'letra': letra, 'exibicoes': exibicoes}
    lista_letras.append(dados)
pd.DataFrame(lista_letras).drop_duplicates().to_excel('~/Downloads/LetrasJorge.xlsx', index=False)

# Webscraping resultados Rússia
session = requests.Session()

url = 'https://en.wikipedia.org/wiki/2021_Russian_legislative_election'

requisicao = session.get(url).content
soup = BeautifulSoup(requisicao, 'lxml')
anteriores = soup.find('td', {'class': 'navbox-list-with-group navbox-list navbox-even hlist'}).find_all('li')
eleicoes_para_raspar = []
for link in anteriores:
    eleicao = link.find('a').text
    try:
        url_eleicao = 'https://en.wikipedia.org' + link.find('a').get('href')
        print(eleicao)
        eleicao = int(eleicao)
        if (eleicao >= 1993):
            if eleicao < 2026:
                eleicoes_para_raspar.append({'eleicao': eleicao, 'url': url_eleicao})
    except:
        pass

eleicoes_para_raspar.append({'eleicao': 2021, 'url': url})

for eleicao in eleicoes_para_raspar:
    print(eleicao['eleicao'])
    tabelas = pd.read_html(eleicao['url'], match='Votes')
    tabela = tabelas[0]
    tabela['eleicao'] = eleicao['eleicao']
    tabela.to_excel(f'~/Downloads/Russia{eleicao["eleicao"]}.xlsx')

# Scraping FBREF
session = requests.Session()
lista_campeonatos = []

url_base = 'https://fbref.com/'
url = url_base + '/en/squads/d9fdd9d9/Botafogo-RJ-Stats'

while True:
    requisicao = session.get(url).content
    soup = BeautifulSoup(requisicao, 'lxml')
    ano = soup.find('h1').text.split()[0]
    print('Raspando ano: ', ano)
    if int(ano) < 2014:
        break
    time.sleep(5)
    tabela = pd.read_html(url, match='Comp')[0]
    tabela['ano'] = ano
    lista_campeonatos.append(tabela)
    prev_link = soup.find('div', {'class': 'prevnext'}).find('a')
    if prev_link.text == 'Previous Season':
        url = url_base + soup.find('div', {'class': 'prevnext'}).find('a').get('href')
    else:
        break

# Scraping discursos Vargas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

url = 'http://www.biblioteca.presidencia.gov.br/presidencia/presidencia/ex-presidentes/getulio-vargas'

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get(url)
time.sleep(5)

content = driver.page_source
soup = BeautifulSoup(content, 'lxml')
anos_discursos = soup.find('div', {'id': 'f84b41b10df14a67a7250c2b2bf06c07'}).find_all('a')
url_anos = []
for ano in anos_discursos:
    url = ano.get('href')
    num_ano = ano.text
    url_anos.append({'ano': num_ano, 'url': url})

for ano in url_anos:
    print(f'>>> Raspando ano: {ano["ano"]}')
    driver.get(ano['url'])
    time.sleep(10)
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')
    discursos = soup.find_all('a', {'class': 'summary url'})
    print(f'Foram encontrados {len(discursos)}')
    while soup.find('a', {'class': 'proximo'}):
        print('     >>>>> Tem mais de uma página!')
        driver.get(soup.find('a', {'class': 'proximo'}).get('href'))
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        discursos.extend(soup.find_all('a', {'class': 'summary url'}))
    for i, discurso in enumerate(discursos):
        url = discurso.get('href')
        driver.get(url)
        time.sleep(10)
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')
        while not soup.find('div', {'id': 'portal-title'}):
            driver.refresh()
            time.sleep(10)
        print(f'    >>> Raspando {i+1}º discurso do ano {ano["ano"]}')
        link = soup.find('div', {'id': 'content-core'}).find('a').get('href')
        driver.get(link)
        time.sleep(5)

# Raspa Shein
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://br.shein.com/trends/New-in-Trends-FW-sc-00654387.html?ici=br_tab01navbar02&src_module=topcat&src_tab_page_id=page_home1693859583259&src_identifier=fc%3DWomen%60sc%3DTEND%C3%8ANCIA%60tc%3D0%60oc%3D0%60ps%3Dtab01navbar02%60jc%3DitemPicking_00654387&srctype=category&userpath=category-TEND%C3%8ANCIA&page='
links_produtos = []

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

for i in tqdm(range(1, 20)):
    driver.get(url+str(i))
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    produtos = soup.find('div', {'class': 'product-list'}).find_all('section', {'class': 'product-list__item'})
    if produtos:
        for produto in produtos:
            link = 'https://br.shein.com' + produto.find('a').get('href')
            titulo = produto.find('a').get('aria-label')
            preco = float(produto.find('span', {'role': 'contentinfo'}).text.replace('R$', '').replace(',', '.'))
            links_produtos.append({'titulo': titulo, 'preco': preco, 'link': link})
    else:
        print('Acabou a raspagem!')
        break
driver.quit()
