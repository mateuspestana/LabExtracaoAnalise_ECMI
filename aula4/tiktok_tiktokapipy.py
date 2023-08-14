# Script para demonstrar como obter dados do TikTok usando o TikTokAPI
# Importando a biblioteca pandas e tiktokapipy
# LEMBRANDO: rodar no console python -m playwright install
from tiktokapipy.api import TikTokAPI
import pandas as pd
from tqdm import tqdm

# Aumentando o número de colunas que o pandas mostra
pd.options.display.max_columns = 20

# Definindo o desafio ou usuário que queremos baixar
challenge = 'ukraine'
user = 'itsmatheuscosta'

# Criando um objeto do tipo TikTokAPI
n_videos = 20

# Criando uma lista vazia para armazenar os dados
with TikTokAPI() as api:
    lista_videos = []
    # Obtendo os dados
    # tiktoks = api.challenge(challenge, video_limit=n_videos)
    tiktoks = api.user(user, video_limit=n_videos)
    # Iterando sobre os vídeos
    for i, video in tqdm(enumerate(tiktoks.videos), total=n_videos):
        user = video.author.unique_id
        url = video.url
        id = video.id
        desc = video.desc
        music = video.music.title
        likes = video.stats.digg_count
        comments = video.stats.comment_count
        shares = video.stats.share_count
        views = video.stats.play_count
        date = video.create_time
        challenges = video.challenges
        lista_challenges = []
        if challenges is not None:
            for challenge in challenges:
                lista_challenges.append(challenge.title)
        challenges = ', '.join(lista_challenges)
        duration = video.video.duration
        dados = {'user': user,
                 'url': url,
                 'id': id,
                 'desc': desc,
                 'music': music,
                 'likes': likes,
                 'comments': comments,
                 'shares': shares,
                 'views': views,
                 'date': date,
                 'challenges': challenges,
                 'duration': duration}
        lista_videos.append(dados)

# Transformando a lista em um dataframe
df = pd.DataFrame(lista_videos)
df['date'] = df['date'].apply(lambda x: x.replace(tzinfo=None))

# Salvando o dataframe como um arquivo em Excel
df.to_excel(f"base_tiktok.xlsx", index=False)