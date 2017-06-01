from bs4 import BeautifulSoup
import requests

jogadores = []
serie_a = []
mando = [
        {"Time": "Botafogo", "Estadio": "Engenhão", "Estadio2": ' '},
        {"Time": "Vasco", "Estadio": "São Januário", "Estadio2": ' '},
        {"Time": "São Paulo", "Estadio": "Morumbi", "Estadio2": ' '},
        {"Time": "Santos", "Estadio": "Vila Belmiro", "Estadio2": "Pacaembu"},
        {"Time": "Vitória", "Estadio": "Fonte Nova", "Estadio2": "Barradão"},
        {"Time": "Atlético-PR", "Estadio": "Arena da Baixada", "Estadio2": ' '},
        {"Time": "Chapecoense", "Estadio": "Arena Condá", "Estadio2": ' '},
        {"Time": "Atlético-GO", "Estadio": "Serra Dourada", "Estadio2": "Olímpico"},
        {"Time": "Sport", "Estadio": "Ilha do Retiro", "Estadio2": ' '},
        {"Time": "Atético-MG", "Estadio": "Independência","Estadio2": "Mineirão"},
        {"Time": "Coritiba", "Estadio": "Couto Pereira", "Estadio2": ' '},
        {"Time": "Corinthians", "Estadio": "Arena Corinthians", "Estadio2": "Pacaembu"},
        {"Time": "Ponte Preta", "Estadio": "Moisés Lucarelli", "Estadio2": ' '},
        {"Time": "Grêmio", "Estadio": "Arena do Grêmio", "Estadio2": ' '},
        {"Time": "Avaí", "Estadio": "Ressacada", "Estadio2": ' '},
        {"Time": "Cruzeiro", "Estadio": "Mineirão", "Estadio2": ' '},
        {"Time": "Bahia", "Estadio": "Fonte Nova", "Estadio2": ' '},
        {"Time": "Palmeiras", "Estadio": "Arena Palmeiras", "Estadio2": ' '},
        {"Time": "Fluminense", "Estadio": "Maracanã", "Estadio2": ' '},
        {"Time": "Flamengo", "Estadio": "Maracanã", "Estadio2": ' '}
         ]

def tabela_a(link):
    clube =  None
    classificaçao = None

    if link.find("td", "tabela-times-posicao") is not None:
        classificaçao = link.find("td", "tabela-times-posicao").text
    if link.find("td", "tabela-times-time") is not None:
        clube = link.find("td", "tabela-times-time").a['title']
    if clube is not None and classificaçao is not None:
        return{
            "Clube": clube,
            "Classificaçao": classificaçao,
            "Media do time": None
        }
    else:
        pass

def jogador_info(link):
    if(link.find("div", "cartola-atletas__card-badges").svg is not None):
        status = link.find("div", "cartola-atletas__card-badges").svg['seletor'].split('-')[3]
    else: status = 'Nulo'
    time = link.find("div", "cartola-atletas__time").img['title']
    posiçao = link.find("div", "column cartola-atletas__posicao cartola-atletas__posicao--full").text
    jogador = link.find("div", "columns cartola-atletas__apelido").text
    preço = float(link.find("div", "small-14 large-12 text__center column cartola-atletas__preco").text.split()[1])
    media = float(link.find("div", "small-5 large-6 column").text.split()[0])
    precisa = int((preço*0.37*2) - media)
    qtde_jogos = link.find("div", "small-5 large-5 column large-push-1").span.text
    if qtde_jogos == '-':
        qtde_jogos = 0

    return {
        "Posiçao": posiçao,
        "Status": status,
        "Nome": jogador,
        "Time": time,
        "Preço": preço,
        "Media": media,
        "Jogos": qtde_jogos,
        "Para valorizar": precisa,
        "Media do time" : None
        #"Mando": None,
        #"Mando2": None

    }

url_tabela = requests.get("http://globoesporte.globo.com/futebol/brasileirao-serie-a/").text
tabela = BeautifulSoup(url_tabela, 'lxml')

with open("cartola.html", encoding="utf8") as html:
    soup = BeautifulSoup(html, "lxml")

for link in soup('div', 'cartola-atletas__card'):
    jogadores.append(jogador_info(link))

for link in tabela('tr', 'tabela-body-linha'):
    if tabela_a(link) is not None:
        serie_a.append(tabela_a(link))

for jogador in jogadores: #Coloca a classifiçao do time nos jogadores
    for classi in serie_a:
        if jogador['Time'] == classi['Clube']:
            jogador['Classificaçao'] = classi['Classificaçao']

for classi in serie_a: #Coloca a media do time na lista serie_a
    for jogador in jogadores:
        if jogador['Posiçao'] == 'Técnico' and jogador['Time'] == classi['Clube']:
            classi['Media do time'] = jogador['Media']

for jogador in jogadores: #Coloca a Media do time em todos os jogadores
    for classi in serie_a:
        if jogador['Time'] == classi['Clube']:
            jogador['Media do time'] = classi['Media do time']

"""for jogador in jogadores: #Adiciona o mando de campo nos jogadores
    for casafora in mando:
        if jogador['Time'] == casafora['Time']:
            jogador['Mando'] = casafora['Estadio']
            jogador['Mando2'] = casafora['Estadio2']
""" #Mando dos jogadores

for jogador in jogadores: #Cluster
    m = float(jogador['Media']) * 5
    mt = float(jogador['Media do time']) * 3
    p = float(jogador['Preço']) * 2
    c = (int(jogador['Classificaçao']))/5
    j = int(jogador['Jogos']) * 3
    jogador['Cluster'] = (((p + mt + m + j)/13) - c)
    if jogador['Jogos'] == 0:
        jogador['Cluster'] = -100


jogadores.sort(key = lambda valor: (valor['Posiçao'], valor['Para valorizar'], valor['Cluster']))

for jogador in jogadores:
    print(jogador)

with open("Melhores para segunda rodada.txt", 'w', encoding="utf8") as melhores:
    for jogador in jogadores:
        melhores.write(jogador['Posiçao'] + ' - ' + jogador['Nome'] + ' - ' + jogador['Time'] + ' - C$' + str(jogador['Preço']) + ' - (' + str(jogador['Para valorizar']) + ') Pontos' + ' - ' + jogador["Status"] + ' - Jogos: ' + str(jogador['Jogos']))
        melhores.write('\n')
        melhores.write(80*'-')
        melhores.write('\n')
