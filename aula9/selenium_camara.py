import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

print("Abrindo o navegador...")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

print("Abrindo o site da Câmara...")
driver.get('https://camara.leg.br')
time.sleep(5)

print("Clicando em Atividade Legislativa...")
atvleg = driver.find_element(By.ID, 'atvlegislativa')
atvleg.click()
propostas = driver.find_element(By.LINK_TEXT, 'Propostas legislativas')
propostas.click()
time.sleep(5)

print("Clicando em Pesquisar...")
pesquisa = driver.find_element(By.ID, 'txtTextoCompleto')

print("Digitando 'redes sociais'...")
pesquisa.send_keys('redes sociais')

pecs = driver.find_element(By.ID, 'PEC - Proposta de Emenda à Constituição')
pecs.click()

pl = driver.find_element(By.ID, 'PL')
pl.click()

ano = driver.find_element(By.ID, 'txtAno')
ano.send_keys('2023')

pesquisar = driver.find_element(By.NAME, 'pesquisar')
pesquisar.click()
# Ou poderíamos ir por: pesquisa.send_keys(Keys.ENTER)
time.sleep(10)
driver.save_screenshot('screenshot1.png')
body = driver.find_element(By.TAG_NAME, 'body')
body.click()
body.send_keys(Keys.END)
time.sleep(0.5)
driver.save_screenshot('screenshot2.png')
soup = BeautifulSoup(driver.page_source, 'lxml')
lista_resultados = soup.find('div', {'id': 'lista-resultados'}).find_all('div', {'class': 'col-11'})

lista_projetos = []
for pl in lista_resultados:
    if pl.find('h6'):
        projeto = pl.find('h6').text.strip()
        autor = pl.find('div').text.replace('Autor: ', '').strip()
        ementa = pl.find('div', {'class': 'infoProposicao'}).find('p').text
        link = pl.find('a').get('href')
        dados = {'projeto': projeto, 'autor': autor, 'ementa': ementa, 'link': link}
        lista_projetos.append(dados)

pd.DataFrame(lista_projetos)

print("Fechando o navegador...")
driver.quit()

