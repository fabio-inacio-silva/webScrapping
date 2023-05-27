import warnings as warn
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from random import randint
from time import sleep

paginas = np.arange(1, 5, 50)
headers = {'Accept-language': 'pt-BR,q=0.8'}
titulo = []
years = []
genero = []
runtimes = []
imdb_ratings = []
imdb_ratings_standardized = []
votos = []
ratings = []

#  
# 

for pagina in paginas:
    response = get('https://www.imdb.com/search/title?genres=sci-fi&'+ 
                   'start=' + str(pagina) + 
                   '&explore=title_type,genres&ref_=adv_prv', headers=headers)
    
    sleep(randint(8,15))

    if response.status_code != 200:
        warn(f'O pedido: {resquests}; Retornou código {response.status_code}')
    
    # pegando cada arquivo html da aplicação
    page_html = BeautifulSoup(response.text, 'html.parser')

    movie_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')

    # separando informações em container individuais
    for container in movie_containers:

        #capturar os tituloes
        if container.find('div', class_ = 'ratings-metascore') is not None:
            title = container.h3.a.text
            titulo.append(title)

            # capturar anos
            if container.h3.find('span', class_ = 'lister-item-year text-muted unbold') is not None:
                year = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
                years.append(year)
            else:
                years.append(None)

            # captutar avaliações
            if container.p.find('span', class_ = 'certificate') is not None:
                rating = container.p.find('span', class_ = 'certificate').text
                ratings.append(rating)
            else:
                ratings.append(None)

            # captutar genero 
            if container.p.find('span', class_ = 'genre') is not None:
                genre = container.p.find('span', class_ = 'genre').text.replace('\n','').strip().split()
                genero.append(genre)
            else:
                genero.append(None)

            # captutar duração do filme 
            if container.p.find('span', class_ = 'runtime') is not None:
                runtime = int(container.p.find('span', class_ = 'runtime').text.replace('min','').strip())
                runtimes.append(runtime)
            else:
                runtimes.append(None)
            
            # capturar a avaliação IMDB
            if container.strong.text is not None:
                imdb = float(container.strong.text.replace(',','.'))
                imdb_ratings.append(imdb)
            else:
                imdb_ratings.append(None)

            # capturar os vontos
            if container.find('span', attrs={'name':'nv'})['data-value'] is not None:
                voto = int(container.find('span', attrs={'name':'nv'})['data-value'])
                votos.append(voto)
            else:
                votos.append(None)            


df_inicial = pd.DataFrame({
    'ano': years,
    'genero': genero,
    'duração': runtimes,
    'imdb': imdb_ratings,
    'votos': votos
})

# separar colunes e corrigir tipagem de dados

df_inicial.loc[ :, 'ano'] = df_inicial['ano'].str[-5:-1]
df_inicial['n_imdc'] = df_inicial['imdb'] * 10
df_final = df_inicial.loc[df_inicial['ano']!= 'Movie']

# print(df_final.head())

#sns.heatmap(df_final.corr(), annot=True)

# ax = df_final['imdb'].value_counts().plot(kind='bar', figsize=(14,8), title='Número de Filmes por Vontos')
# ax.set_xlabel('Votos')
# ax.set_ylabel("Quantidade de Filmes")
# ax.plot()

# relação entre duração do filme / votos

# plt.scatter(df_final['duração'], df_final['imdb'])
# plt.xlabel('Duração dos filmes')
# plt.ylabel('Nota IMDB')

sep_genero = df_final.explode('genero')
genero_counts = sep_genero['genero'].value_counts()
genero_counts.plot(kind='barh')

plt.show()
