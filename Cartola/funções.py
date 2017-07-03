from bs4 import BeautifulSoup
import requests


# -----------------------FUNÇÃO PARA ADICIONAR APROVEITAMENTO NA LISTA serie_a-----------------------------#
def aproveitamento():

	times = [
		{
			'Time': 'Corinthians', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Grêmio', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Flamengo', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Palmeiras', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Santos', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Atlético-MG', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Vasco', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Fluminense', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Botafogo', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Coritiba', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Sport', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Ponte Preta', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Cruzeiro', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Atlético-PR', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Chapecoense', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Bahia', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'São Paulo', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Vitória', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Avaí', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
		{
			'Time': 'Atlético-GO', 'Aproveitamento Casa': 0, 'Aproveitamento Fora': 0, 'Total Casa': 0, 'Total Fora': 0,  
		},
	]
	
	url_tabela = requests.get("http://www.tabeladobrasileirao.net/").text
	tabela = BeautifulSoup(url_tabela, 'lxml')

	for link in tabela("div", "simulator-games"):
		rodadaAtual = int(link.find('table', 'table')['data-current-round'])


	def Meta():
		for jogo in range(rodadaAtual-1):
			jogo += 1
			for time in times:
				try:
					if link['data-round'] == str(jogo) and link['data-round'] is not None:
						if link.find("div", "game-club game-club--principal")['title'] == time['Time']:
							time['Total Casa'] += 3
							if int(link.find('div', 'game-scoreboard-input goalshome home').text.split(' ')[1]) > int(link.find('div', 'game-scoreboard-input goalsvisitor visitor').text.split(' ')[1]):
								time['Aproveitamento Casa'] += 3
							if int(link.find('div', 'game-scoreboard-input goalshome home').text.split(' ')[1]) == int(link.find('div', 'game-scoreboard-input goalsvisitor visitor').text.split(' ')[1]):
								time['Aproveitamento Casa'] += 1

						if link.find("div", "game-club game-club--visitor")['title'] == time['Time']:
							time['Total Fora'] += 3
							if int(link.find('div', 'game-scoreboard-input goalshome home').text.split(' ')[1]) < int(link.find('div', 'game-scoreboard-input goalsvisitor visitor').text.split(' ')[1]):
								time['Aproveitamento Fora'] += 3
							if int(link.find('div', 'game-scoreboard-input goalshome home').text.split(' ')[1]) == int(link.find('div', 'game-scoreboard-input goalsvisitor visitor').text.split(' ')[1]):
								time['Aproveitamento Fora'] += 1
				except:
					pass


	for link in tabela("tr", "table-row"):
		Meta()

	for time in times:
		time['Aproveitamento Casa'] = time['Aproveitamento Casa'] / time['Total Casa']
		time['Aproveitamento Fora'] = time['Aproveitamento Fora'] / time['Total Fora']  


	return times


# ----------------------------------------------------------------------------------------------------------#

# -----------------------FUNÇÃO PARA ADICIONAR ADVERSÁRIOS NA LISTA adversarios-----------------------------#
def jogos(link, rodadaAtualString):
 
    casa = None
    fora = None

    
    if link.find("div", "game-club game-club--principal") is not None and rodadaAtualString in link.find("td", "match").a[
        "href"].split("/"):
        casa = link.find("div", "game-club game-club--principal")['title']

    if link.find("div", "game-club game-club--visitor") is not None and rodadaAtualString in link.find("td", "match").a[
        "href"].split("/"):
        fora = link.find("div", "game-club game-club--visitor")['title']

    if casa is not None and fora is not None:
        return {
            "Casa": casa,
            "Fora": fora
        }


# ----------------------------------------------------------------------------------------------------------#

# -----------------------FUNÇÃO PARA ADICIONAR INFORMAÇÕES NA LISTA serie_a---------------------------------#
def tabela_a(link):
    clube = None
    g = None
    gc = None
    apcasa = None
    apfora = None
  
    if link.find("td", "team") is not None:
        clube = link.find("td", "team").div['data-name']
    if link.find("td", "goals_for") is not None:
        g = link.find("td", "goals_for").text
    if link.find("td", "goals_against") is not None:
        gc = link.find("td", "goals_against").text
    if clube is not None:
        return{
            "Clube": clube,
            "Aproveitamento Casa": apcasa,
            "Aproveitamento Fora": apfora,
            "Media do time": None,
            "G": g,
            "GC": gc,
            "Cluster Time Ataque": 0,
            "Cluster Time Defesa": 0,
            "Cluster Time Media": 0,
            "Cluster Time Rodada": 0,
       	}
    else:
        pass


# ----------------------------------------------------------------------------------------------------------#


# ------------------------FUNÇÃO PARA ADICIONAR INFORMAÇÕES NA LISTA jogadores------------------------------#
def jogador_info(link):
    if link.find("div", "cartola-atletas__card-badges").svg is not None:
        status = link.find("div", "cartola-atletas__card-badges").svg['seletor'].split('-')[3]
    else:
        status = 'Nulo'
    time = link.find("div", "cartola-atletas__time").img['title']
    posiçao = link.find("div", "column cartola-atletas__posicao cartola-atletas__posicao--full").text
    jogador = link.find("div", "columns cartola-atletas__apelido").text
    preço = float(link.find("div", "small-14 large-12 text__center column cartola-atletas__preco").text.split()[1])
    media = float(link.find("div", "small-5 large-6 column").text.split()[0])
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
        "Media do time": None,
        "Para valorizar": 999,
        "Cluster": None,
        "Aproveitamento Casa": 0,
        "Aproveitamento Fora": 0,
    }


# ----------------------------------------------------------------------------------------------------------#