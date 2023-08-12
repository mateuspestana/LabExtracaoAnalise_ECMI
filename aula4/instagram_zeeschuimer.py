# Script para demonstrar o processamento de um arquivo .ndjson entregue pelo Zeeschuimer

# Importando a biblioteca pandas e matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# Aumentando o número de colunas que o pandas mostra
pd.options.display.max_columns = 20

# Lendo o arquivo .ndjson. Importante: o parâmetro lines=True é necessário para que o pandas consiga ler o arquivo.
# Isso é específico para arquivos .ndjson
casimiro = pd.read_json('../bases/casimiro_instagram.ndjson', lines=True)

# A variável que eu quero analisar é a 'data'. Vamos transformá-la em um dataframe.
# A variável data é um dicionário, então precisamos usar o método json_normalize para transformá-la em um dataframe.
casimiro = pd.json_normalize(casimiro['data'])

print(casimiro.columns)

# Como podemos ver, temos muitas colunas. Vamos selecionar apenas as que nos interessam.
colunas_desejadas = ['id', 'like_count', 'comment_count', 'user.username',
                     'user.full_name', 'user.is_verified', 'caption.text',
                     'caption.created_at', 'play_count', 'video_duration',
                     'code']
casimiro = casimiro[colunas_desejadas]

# Consertando a coluna 'caption.created_at'
casimiro['caption.created_at'] = casimiro['caption.created_at'].apply(lambda x: pd.Timestamp(x, unit='s'))

# Vamos filtrar apenas os posts com mais de 100.000 likes
casimiro = casimiro[casimiro['like_count'] > 100_000]

# Legal. Qual será o post com mais likes do nosso dataset?
print(
    f"Post com mais likes: \n{casimiro.sort_values(by='like_count', ascending=False).head(1)[['code', 'caption.created_at', 'like_count']]}\n\n")

# E o post com mais comentários?
print(
    f"Post com mais comentários: \n{casimiro.sort_values(by='comment_count', ascending=False).head(1)[['code', 'caption.created_at', 'comment_count']]}\n\n")

# E o post com mais visualizações?
print(
    f"Post com mais views: \n{casimiro.sort_values(by='play_count', ascending=False).head(1)[['code', 'caption.created_at', 'play_count']]}\n\n")

# Qual a média de likes por post?
print(f"Média de likes por post: {casimiro['like_count'].mean()}\n\n")

# Qual a média de comentários por post?
print(f"Média de comentários por post: {casimiro['comment_count'].mean()}\n\n")

# Plotando um lineplot com a quantidade de likes por dia
plt.plot(casimiro['caption.created_at'], casimiro['like_count'])
plt.title('Quantidade de likes por dia/post')
plt.xlabel('Data')
plt.ylabel('Quantidade de likes')
plt.show()
