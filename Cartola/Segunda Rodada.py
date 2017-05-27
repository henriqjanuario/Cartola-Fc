from bs4 import BeautifulSoup
import requests
from operator import itemgetter
times = ['Atlético-GO','Atlético-MG','Atlético-PR','Avaí','Bahia','Botafogo','Chapecoense','Corinthians','Coritiba','Cruzeiro','Flamengo','Fluminense','Grêmio','Palmeiras','Ponte Preta','Santos','Sport','São Paulo','Vasco','Vitória']
jogador = []
preco = []
media = []
valor = []
posicao = []
status = []
time = []

with open("cartola.html", encoding="utf8") as html:
    soup = BeautifulSoup(html, "lxml")

for link in soup.find_all("div", {"class": "columns cartola-atletas__apelido"}):
    jogador.append(link.get_text())

for link in soup.find_all("div", {"class": "small-14 large-12 text__center column cartola-atletas__preco"}):
    preco.append(float(link.get_text().split()[1]))

for link in soup.find_all("div", {"class": "small-5 large-6 column"}):
    media.append(float(link.get_text().split()[0]))

for link in soup.find_all("div", {"class": "column cartola-atletas__posicao cartola-atletas__posicao--full"}):
    posicao.append(link.get_text())

for link in soup.find_all("svg", {"class": "status-atleta-icone"}):
    if 'provavel' in str(link):
        status.append('provavel')
    elif 'duvida' in str(link):
         status.append('duvida')
    elif 'contundido' in str(link):
        status.append('contundido')
    elif 'suspenso' in str(link):
        status.append('suspenso')


info = list(zip(posicao, jogador, preco, media, status))
info.sort(key=itemgetter(2), reverse = True)

for inf in info:
    p = inf[2]
    m = inf[3]
    v = int(p*0.37*2)
    v = v - m
    valor.append(v)

valor = list(zip(info,valor))
valor.sort(key=itemgetter(1))
print('|POSIÇÃO|NOME|PREÇO|MEDIA|STATUS|PONTUAÇÃO PARA VALORIZAR')
i=0
for val in valor:
    print(val)
    i+=1
    print(i)

valor = list(str(valor))
"""with open("Melhores para segunda rodada.txt", 'w' ,encoding="utf8") as melhores:
    for val in valor:
        melhores.writelines(val.split())
        melhores.write('\n')"""