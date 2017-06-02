from bs4 import BeautifulSoup
import requests
import os.path

jogadores = []
serie_a = []
adversarios = []
mando_fora = ["Atlético-PR", "Santos", "Vitória", "Botafogo", "Vasco", "São Paulo", "Atlético-MG", "Sport",
              "Chapecoense", "Atlético-GO"]

time_tipo_1 = ["Grêmio", "Flamengo", "Corinthians", "Palmeiras", "Atlético-MG", "São Paulo", "Santos", "Cruzeiro"]
time_tipo_2 = ["Fluminense", "Ponte Preta", "Coritiba", "Vasco", "Atlético-PR", "Chapecoense"]
time_tipo_3 = ["Bahia", "Vitória", "Avaí", "Atlético-GO", "Sport", "Botafogo"]
Rodada = 3


# -----------------------FUNÇÃO PARA ADICIONAR ADVERSÁRIOS NA LISTA adversarios-----------------------------#
def jogos(link):
    casa = None
    fora = None
    if link.find("div", "game-club game-club--principal") is not None and '4-rodada' in link.find("td", "match").a[
        "href"].split("/"):
        casa = link.find("div", "game-club game-club--principal")['title']

    if link.find("div", "game-club game-club--visitor") is not None and '4-rodada' in link.find("td", "match").a[
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
    aproveitamento = None
    g = None
    gc = None

    if link.find("td", "percent") is not None:
        aproveitamento = link.find("td", "percent").text
    if link.find("td", "team") is not None:
        clube = link.find("td", "team").div['data-name']
    if link.find("td", "goals_for") is not None:
        g = link.find("td", "goals_for").text
    if link.find("td", "goals_against") is not None:
        gc = link.find("td", "goals_against").text
    if clube is not None and aproveitamento is not None:
        return {
            "Clube": clube,
            "Aproveitamento": aproveitamento,
            "Media do time": None,
            "G": g,
            "GC": gc,
            "Cluster Time Ataque": 0,
            "Cluster Time Defesa": 0,
            "Cluster Time Media": 0,
            "Cluster Time Rodada": 0
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
        "Cluster": None
    }


# ----------------------------------------------------------------------------------------------------------#


# ------------------------ACIONA OS SITES DO CARTOLA DE DA TABELA DE CLASSIFICAÇÃO--------------------------#
url_tabela = requests.get("http://www.tabeladobrasileirao.net/").text
tabela = BeautifulSoup(url_tabela, 'lxml')

with open("C:/Users/rique_000/Documents/GitHub/Cartola-Fc/HTML/cartola.html", encoding="utf8") as html:
    soup = BeautifulSoup(html, "lxml")
# -----------------------------------------------------------------------------------------------------------#


# -----------------------------PROCURA TODOS OS JOGADORES DO CARTOLA-----------------------------------------#
for link in soup('div', 'cartola-atletas__card'):
    jogadores.append(jogador_info(link))
# -----------------------------------------------------------------------------------------------------------#


# -----------------------------PROCURA TODOS OS TIMES NA TABELA DE CLASSIFICAÇÃO-----------------------------#
for link in tabela('tr', 'table-row'):
    if tabela_a(link) is not None:
        serie_a.append(tabela_a(link))
# -----------------------------------------------------------------------------------------------------------#


# ------------------------------COLOCA O APROVEITAMENTO DO TIME NOS JOGADORES--------------------------------#
for jogador in jogadores:
    for classi in serie_a:
        if jogador['Time'] == classi['Clube']:
            jogador['Aproveitamento'] = classi['Aproveitamento']
# -----------------------------------------------------------------------------------------------------------#


# ------------------------------COLOCA A MEDIA DO TIME NA LISTA serie_a--------------------------------------#
for classi in serie_a:
    for jogador in jogadores:
        if jogador['Posiçao'] == 'Técnico' and jogador['Time'] == classi['Clube']:
            classi['Media do time'] = jogador['Media']
# -----------------------------------------------------------------------------------------------------------#


# ------------------------------COLOCA A MEDIA DO TIME EM TODOS OS JOGADORES---------------------------------#
for jogador in jogadores:
    for classi in serie_a:
        if jogador['Time'] == classi['Clube']:
            jogador['Media do time'] = classi['Media do time']
# -----------------------------------------------------------------------------------------------------------#

# ---------------------COLOCA A QUANTIDADE DE GOLS FEITOS PELA EQUIPE NOS ATACANTES E MEIO CAMPOS -----------#
for jogador in jogadores:  # Coloca quantidade de gols feito pela equipe nos atacantes
    for classi in serie_a:
        if jogador["Posiçao"] == 'Ataque' or jogador["Posiçao"] == 'Meia':
            if jogador['Time'] == classi['Clube']:
                jogador['Gols equipe'] = int(classi['G'])
# -----------------------------------------------------------------------------------------------------------#


# -----------------------COLOCA A QUANTIDADE DE GOLS SOFRIDOS PELA EQUIPE NOS DEFENSORES---------------------#
for jogador in jogadores:  # Coloca quantidade de gols sofridos pela equipe nos defensores
    for classi in serie_a:
        if jogador["Posiçao"] == 'Zagueiro' or jogador["Posiçao"] == 'Lateral' or jogador["Posiçao"] == 'Goleiro':
            if jogador['Time'] == classi['Clube']:
                jogador['Gols sofridos equipe'] = int(classi['GC'])
# -----------------------------------------------------------------------------------------------------------#


# ------------------------------CALCULO DE CLUSTER DOS JOGADORES---------------------------------------------#
for jogador in jogadores:
    m = float(jogador['Media']) * 5  # MEDIA DO JOGADOR
    mt = (float(jogador['Media do time'])) * 3  # MEDIA DO TIME
    j = int(jogador['Jogos']) / Rodada # QUANTIDADE DE JOGOS
    if float(jogador['Aproveitamento']) == 0:  # APROVEITAMENTO SE FOR 0
        a = 0.1
    else:  # APROVEITAMENTO NORMAL
        a = (float(jogador['Aproveitamento']) / 100)
    jogador['Cluster'] = (mt + m)/8

    if jogador["Cluster"] < 0:
        jogador["Cluster"] = jogador["Cluster"] - (jogador["Cluster"] * (1-j))
    else:
        jogador['Cluster'] = jogador['Cluster'] * j
    if jogador["Cluster"] < 0:
        jogador['Cluster'] = jogador['Cluster'] - (jogador["Cluster"] * (1-a))
    else:
        jogador['Cluster'] = jogador['Cluster'] * a

    if jogador["Time"] in mando_fora:  # MULTIPLICA CLUSTER POR 0.7 SE FOR JOGAR FORA
        if jogador["Cluster"] < 0:
            jogador["Cluster"] = jogador["Cluster"] + (jogador["Cluster"]*0.3)
        else:
            jogador["Cluster"] = jogador["Cluster"] * 0.7

    if jogador["Time"] in time_tipo_1:  # MULTIPLICA O CLUSTER POR 1.1 SE FOR TIME GRANDE
        if jogador["Cluster"] < 0:
            jogador["Cluster"] = jogador["Cluster"] * 0.9
        else:
            jogador["Cluster"] = jogador["Cluster"] * 1.1

    if jogador["Time"] in time_tipo_3:  # MULTIPLICA O CLUSTER POR 0.9 SE FOR TIME PEQUENO
        if jogador["Cluster"] < 0:
            jogador["Cluster"] = jogador["Cluster"] * 1.1
        else:
            jogador["Cluster"] = jogador["Cluster"] * 0.9

    if jogador["Posiçao"] == "Ataque" or jogador[
        "Posiçao"] == 'Meia':  # MULTIPLICA O CLUSTER POR MEDIA DE GOLS POR PARTIDA PARA ATACANTES E MEIO CAMPOS
        if jogador["Gols equipe"] == 0:
            gols_feitos = 0.7 / Rodada
            if jogador["Cluster"] < 0:
                jogador["Cluster"] = jogador["Cluster"] - (jogador["Cluster"] * (1/gols_feitos))
            else:
                jogador["Cluster"] = jogador["Cluster"] * gols_feitos
        else:
            gols_feitos = jogador["Gols equipe"] / Rodada
            if jogador["Cluster"] < 0:
                jogador["Cluster"] = jogador["Cluster"] - (jogador["Cluster"] * (1/gols_feitos))
            else:
                jogador["Cluster"] = jogador["Cluster"] * gols_feitos

    if jogador["Posiçao"] == "Zagueiro" or jogador["Posiçao"] == "Lateral" \
            or jogador[
                "Posiçao"] == 'Goleiro':  # DIVIDE O CLUSTER POR MEDIA DE GOLS SOFRIDOS POR PARTIDA PARA DESEFA
        if jogador["Gols sofridos equipe"] != 0:
            gols_sofridos = int(jogador["Gols sofridos equipe"]) / Rodada
            if jogador["Cluster"] < 0:
                jogador["Cluster"] = jogador["Cluster"] - (jogador["Cluster"] / gols_sofridos)
            else:
                jogador["Cluster"] = jogador["Cluster"] / gols_sofridos
        else:
            gols_sofridos = 0.7 / Rodada
            if jogador["Cluster"] < 0:
                jogador["Cluster"] = jogador["Cluster"] - (jogador["Cluster"] / gols_sofridos)
            else:
                jogador["Cluster"] = jogador["Cluster"] / gols_sofridos

    if int(jogador["Jogos"]) == 1:
        jogador["Para valorizar"] = jogador["Preço"] * 0.75
        jogador["Para valorizar"] = jogador["Para valorizar"] - jogador["Media"]

# -----------------------------------------------------------------------------------------------------------#
jogadores.sort(key=lambda valor: (valor['Posiçao'], valor['Cluster']), reverse=True)
for jogador in jogadores:
    print(jogador)
    print()
# ------------------------CLUSTERIZA OS TIMES PARA A RODADA E SOMA O CLUSTER DO TIME EM CADA JOGADOR---------#

for classi in serie_a:
    i = 0
    for jogador in jogadores:
        if jogador["Status"] == 'provavel':
            if jogador["Posiçao"] == 'Atacante' or jogador["Posiçao"] == 'Meia':
                if jogador['Time'] == classi['Clube']:
                    classi["Cluster Time Ataque"] = classi["Cluster Time Ataque"] + jogador['Cluster']
                    i += 1
    classi["Cluster Time Ataque"] = classi["Cluster Time Ataque"] / i

for classi in serie_a:
    i = 0
    for jogador in jogadores:
        if jogador["Status"] == 'provavel':
            if jogador["Posiçao"] == 'Zagueiro' or jogador["Posiçao"] == 'Lateral' or jogador["Posiçao"] == 'Goleiro':
                if jogador['Time'] == classi['Clube']:
                    classi["Cluster Time Defesa"] = classi["Cluster Time Defesa"] + jogador['Cluster']
                    i += 1
    classi["Cluster Time Defesa"] = classi["Cluster Time Defesa"] / i

for classi in serie_a:
    classi["Cluster Time Media"] = (classi["Cluster Time Ataque"] + classi["Cluster Time Defesa"]) / 2

# -----------------------------------------------------------------------------------------------------------#


# -----------------------------PROCURA TODOS OS ADVERSÁRIOS DA RODADA----------------------------------------#
for link in tabela("tr", "table-row"):
    if jogos(link) is not None:
        adversarios.append(jogos(link))
# -----------------------------------------------------------------------------------------------------------#


# -----------------------ATUALIZA O CLUSTER DOS JOGADORES COM O CLUSTER DOS ADVERSÁRIOS----------------------#
for jogador in jogadores:
    for classi in serie_a:
        for cluster in adversarios:
            if jogador["Time"] == classi["Clube"]:
                if cluster["Casa"] == jogador["Time"]:
                    jogador["Adversario"] = cluster["Fora"]
                elif cluster["Fora"] == jogador["Time"]:
                    jogador["Adversario"] = cluster["Casa"]

for jogador in jogadores:
    for classi in serie_a:
        if jogador["Adversario"] == classi["Clube"]:
            if jogador["Posiçao"] == 'Atacante' or jogador["Posiçao"] == 'Meia':
                if jogador["Cluster"] < 0:
                    jogador["Cluster"] = (jogador["Cluster"] - classi["Cluster Time Defesa"])
                else:
                    jogador["Cluster"] = (jogador["Cluster"] - classi["Cluster Time Defesa"])
for jogador in jogadores:
    for classi in serie_a:
        if jogador["Adversario"] == classi["Clube"]:
            if jogador["Posiçao"] == 'Zagueiro' or jogador["Posiçao"] == 'Lateral' or jogador["Posiçao"] == 'Goleiro':
                if jogador["Cluster"] < 0:
                    jogador["Cluster"] = (jogador["Cluster"] - classi["Cluster Time Ataque"])
                else:
                    jogador["Cluster"] = (jogador["Cluster"] - classi["Cluster Time Ataque"])

for classi in serie_a:
    i = 0
    media_para_tecnico = 0
    for jogador in jogadores:
        if jogador["Time"] == classi["Clube"] and jogador["Status"] == 'provavel' and jogador["Posiçao"] != 'Técnico':
            media_para_tecnico = media_para_tecnico + jogador["Cluster"]
            i += 1
    classi["Cluster Time Rodada"] = media_para_tecnico/i

for jogador in jogadores:
    for classi in serie_a:
        if jogador["Posiçao"] == 'Técnico':
            if jogador["Time"] == classi["Clube"]:
                jogador["Cluster"] = classi["Cluster Time Rodada"]
# -----------------------------------------------------------------------------------------------------------#


# ---------------------------ORDENA A LISTA DE JOGADORES-----------------------------------------------------#
jogadores.sort(key=lambda valor: (valor['Posiçao'], valor['Cluster']), reverse=True)
serie_a.sort(key=lambda valor: valor['Cluster Time Rodada'], reverse=True)
# -----------------------------------------------------------------------------------------------------------#


# -----------------------------SALVA AS PRINCIPAIS INFORMAÇÕES EM UM ARQUIVO TXT-----------------------------#
with open("C:/Users/rique_000/Documents/GitHub/Cartola-Fc/Cluster/Rodada 4/Melhores para proxima rodadav2.txt", 'w', encoding="utf8") as melhores:
    for jogador in jogadores:
        melhores.write(jogador['Posiçao'] + ' - ' + jogador['Nome'] + ' - ' + jogador['Time'] + ' - C$' + str(
            jogador['Preço']) + ' - ' + jogador["Status"] + ' - (%.2f)' % (jogador["Cluster"]))
        melhores.write('\n')
        melhores.write(150 * '-')
        melhores.write('\n')
# -----------------------------------------------------------------------------------------------------------#


# ---------------------------SALVA OS VINTE MELHORES JOGADORES DE CADA POSIÇÃO EM UM ARQUIVO TXT-------------#
with open("C:/Users/rique_000/Documents/GitHub/Cartola-Fc/Cluster/Rodada 4/20 Melhores para proxima rodadav2.txt", 'w', encoding="utf8") as melhores:
    cont = 0
    for jogador in jogadores:
        if jogador["Posiçao"] == 'Goleiro' and jogador["Status"] == 'provavel' and cont < 20:
            cont += 1
            melhores.write(jogador['Posiçao'] + ' - ' + jogador['Nome'] + ' - ' + jogador['Time'] + ' - C$' + str(
                jogador['Preço']) + ' - ' + jogador["Status"] + ' - (%.2f)' % (jogador["Cluster"]))
            melhores.write('\n')
            melhores.write(150 * '-')
            melhores.write('\n')

    cont = 0
    for jogador in jogadores:
        if jogador["Posiçao"] == 'Zagueiro' and jogador["Status"] == 'provavel' and cont < 20:
            cont += 1
            melhores.write(jogador['Posiçao'] + ' - ' + jogador['Nome'] + ' - ' + jogador['Time'] + ' - C$' + str(
                jogador['Preço']) + ' - ' + jogador["Status"] + ' - (%.2f)' % (jogador["Cluster"]))
            melhores.write('\n')
            melhores.write(150 * '-')
            melhores.write('\n')

    cont = 0
    for jogador in jogadores:
        if jogador["Posiçao"] == 'Lateral' and jogador["Status"] == 'provavel' and  cont < 20:
            cont += 1
            melhores.write(jogador['Posiçao'] + ' - ' + jogador['Nome'] + ' - ' + jogador['Time'] + ' - C$' + str(
                jogador['Preço']) + ' - ' + jogador["Status"] + ' - (%.2f)' % (jogador["Cluster"]))
            melhores.write('\n')
            melhores.write(150 * '-')
            melhores.write('\n')

    cont = 0
    for jogador in jogadores:
        if jogador["Posiçao"] == 'Meia' and jogador["Status"] == 'provavel' and cont < 20:
            cont += 1
            melhores.write(jogador['Posiçao'] + ' - ' + jogador['Nome'] + ' - ' + jogador['Time'] + ' - C$' + str(
                jogador['Preço']) + ' - ' + jogador["Status"] + ' - (%.2f)' % (jogador["Cluster"]))
            melhores.write('\n')
            melhores.write(150 * '-')
            melhores.write('\n')

    cont = 0
    for jogador in jogadores:
        if jogador["Posiçao"] == 'Atacante' and jogador["Status"] == 'provavel' and cont < 20:
            cont += 1
            melhores.write(jogador['Posiçao'] + ' - ' + jogador['Nome'] + ' - ' + jogador['Time'] + ' - C$' + str(
                jogador['Preço']) + ' - ' + jogador["Status"] + ' - (%.2f)' % (jogador["Cluster"]))
            melhores.write('\n')
            melhores.write(150 * '-')
            melhores.write('\n')

    cont = 0
    for jogador in jogadores:
        if jogador["Posiçao"] == 'Técnico' and jogador["Status"] == 'provavel' and cont < 20:
            cont += 1
            melhores.write(jogador['Posiçao'] + ' - ' + jogador['Nome'] + ' - ' + jogador['Time'] + ' - C$' + str(
                jogador['Preço']) + ' - ' + jogador["Status"] + ' - (%.2f)' % (jogador["Cluster"]))
            melhores.write('\n')
            melhores.write(150 * '-')
            melhores.write('\n')

            # -----------------------------------------------------------------------------------------------------------#
# -----------------------------------------------------------------------------------------------------------#


# -----------------------------SALVA AS INFORMAÇÕES DE VALORIZAÇÃO EM UM ARQUIVO TXT-------------------------#
with open("C:/Users/rique_000/Documents/GitHub/Cartola-Fc/Cluster/Rodada 4/Melhores para valorizar.txt", 'w', encoding="utf8") as melhores:
    jogadores.sort(key=lambda valor: (valor['Posiçao'], valor['Para valorizar'], valor['Preço']))
    for jogador in jogadores:
        if int(jogador["Jogos"]) == 1 and jogador["Status"] == 'provavel':
            melhores.write(jogador['Posiçao'] + ' - ' + jogador['Nome'] + ' - ' + jogador['Time'] + ' - C$' + str(
                jogador['Preço']) + ' - ' + jogador["Status"] + ' - (%.2f)' % (jogador["Para valorizar"]))
            melhores.write('\n')
            melhores.write(150 * '-')
            melhores.write('\n')
# ------------------------------------------------------------------------------------------------------------#


# --------------------------PRINTA TODAS AS INFORMAÇÕES DOS JOGADORES----------------------------------------#
# for jogador in jogadores:
#    print(jogador)
#    print()
# -----------------------------------------------------------------------------------------------------------#


# --------------------------PRINTA TODAS AS INFORMAÇÕES DOS CLUBES-------------------------------------------#
for classi in serie_a:
    print()
    print(classi)
# -----------------------------------------------------------------------------------------------------------#

