# Script para demonstrar como obter dados do Telegram usando o SNScraper

# Importando a biblioteca pandas e snscrape
import snscrape.modules.telegram as sntelegram
import pandas as pd

# Aumentando o número de colunas que o pandas mostra
pd.options.display.max_columns = 20

# Definindo o grupo do Telegram que queremos baixar
grupo_telegram = 'russiabeyond_br'

# Criando um objeto do tipo TelegramChannelScraper
sn_channel = sntelegram.TelegramChannelScraper(grupo_telegram)

# Criando uma lista vazia para armazenar os dados
lista_msgs = []

# Definindo o número de mensagens que queremos baixar
n_msgs = 10

# Iterando sobre as mensagens do grupo
# O i é para registrarmos em qual posição estamos, e o msg é a mensagem propriamente dita.
for i, msg in enumerate(sn_channel.get_items()):
    # Criando um dicionário com os dados que queremos
    data = {'date': msg.date,
            'id': msg.url,
            'account_handle': grupo_telegram,
            'description': msg.content,
            'outlinks': ', '.join(msg.outlinks)}
    # Adicionando o dicionário à lista
    lista_msgs.append(data)
    # Se a posição atual for maior que o número de mensagens definido anteriormente, paramos o loop
    if i > n_msgs:
        break

# Transformando a lista em um dataframe
msgs = pd.DataFrame(lista_msgs)
msgs['date'] = msgs['date'].dt.tz_  localize(None)

# Salvando o dataframe como um arquivo em Excel
msgs.to_excel(f"{grupo_telegram}_telegram.xlsx", index=False)
print('Arquivo salvo!')