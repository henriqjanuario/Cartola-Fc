from bs4 import BeautifulSoup
import requests
from funções import *

def diferenca(time_tipo_1, time_tipo_2, time_tipo_3, arquivo_dif, arquivo_20_dif, arquivo_val, rodadaAtual):

    jogadores = []
    serie_a = []
    adversarios = []
    mando_fora = []
    rodadaAtualString = str(rodadaAtual) + '-rodada'
    rodadaAtual = rodadaAtual - 1

    # ------------------------ACIONA OS SITES DO CARTOLA DE DA TABELA DE CLASSIFICAÇÃO--------------------------#
    url_tabela = requests.get("http://www.tabeladobrasileirao.net/").text
    tabela = BeautifulSoup(url_tabela, 'lxml')

    with open("C:/Users/rique_000/Documents/GitHub/Cartola-Fc/HTML/cartola.html", encoding="utf8") as html:
        soup = BeautifulSoup(html, "lxml")

    # -----------------------------------------------------------------------------------------------------------#
    print("PASSO 1 - LEU HTML DO CARTOLA")

    # -----------------------------PROCURA TODOS OS JOGADORES DO CARTOLA-----------------------------------------#
    for link in soup('div', 'cartola-atletas__card'):
        jogadores.append(jogador_info(link))
    # -----------------------------------------------------------------------------------------------------------#
    print("PASSO 2 - ACHOU TODOS OS JOGADORES DO CARTOLA")

    # -----------------------------PROCURA TODOS OS TIMES NA TABELA DE CLASSIFICAÇÃO-----------------------------#
    for link in tabela('tr', 'table-row'):
        if tabela_a(link) is not None:
            serie_a.append(tabela_a(link))
    print("PASSO 3 - ACHOU TODOS OS TIMES NA TABELA")    
    times = aproveitamento()
    for time in times:
        for classi in serie_a:
            if time['Time'] == classi['Clube']:
                classi['Aproveitamento Casa'] = time['Aproveitamento Casa']
                classi['Aproveitamento Fora'] = time['Aproveitamento Fora']
    # -----------------------------------------------------------------------------------------------------------#
    print("PASSO 3.1 - COLOCOU APROVEITAMENTO NOS TIMES")

    # ------------------------------COLOCA O APROVEITAMENTO DO TIME NOS JOGADORES--------------------------------#
    for jogador in jogadores:
        for classi in serie_a:
            if jogador['Time'] == classi['Clube']:
                jogador['Aproveitamento Casa'] = classi['Aproveitamento Casa']
                jogador['Aproveitamento Fora'] = classi['Aproveitamento Fora']
    # -----------------------------------------------------------------------------------------------------------#
    print("PASSO 4 - ADICIONOU O APROVEITAMENTO DOS TIMES NOS JOGADORES")

    # ------------------------------COLOCA A MEDIA DO TIME NA LISTA serie_a--------------------------------------#
    for classi in serie_a:
        for jogador in jogadores:
            if jogador['Posiçao'] == 'Técnico' and jogador['Time'] == classi['Clube']:
                classi['Media do time'] = jogador['Media']
    # -----------------------------------------------------------------------------------------------------------#
    print("PASSO 5 - COLOCOU A MEDIA DO TIME NA LISTA serie_a")

    # ------------------------------COLOCA A MEDIA DO TIME EM TODOS OS JOGADORES---------------------------------#
    for jogador in jogadores:
        for classi in serie_a:
            if jogador['Time'] == classi['Clube']:
                jogador['Media do time'] = classi['Media do time']
    # -----------------------------------------------------------------------------------------------------------#
    print("PASSO 6 - COLOCOU A MEDIA DO TIME EM TODOS OS JOGADORES")

    # ---------------------COLOCA A QUANTIDADE DE GOLS FEITOS PELA EQUIPE NOS ATACANTES E MEIO CAMPOS -----------#
    for jogador in jogadores:  # Coloca quantidade de gols feito pela equipe nos atacantes
        for classi in serie_a:
            if jogador["Posiçao"] == 'Ataque' or jogador["Posiçao"] == 'Meia':
                if jogador['Time'] == classi['Clube']:
                    jogador['Gols equipe'] = int(classi['G'])
    # -----------------------------------------------------------------------------------------------------------#
    print("PASSO 7 - COLOCOU A QUANTIADE DE GOLS FEITOS")

    # -----------------------COLOCA A QUANTIDADE DE GOLS SOFRIDOS PELA EQUIPE NOS DEFENSORES---------------------#
    for jogador in jogadores:  # Coloca quantidade de gols sofridos pela equipe nos defensores
        for classi in serie_a:
            if jogador["Posiçao"] == 'Zagueiro' or jogador["Posiçao"] == 'Lateral' or jogador["Posiçao"] == 'Goleiro':
                if jogador['Time'] == classi['Clube']:
                    jogador['Gols sofridos equipe'] = int(classi['GC'])
    # -----------------------------------------------------------------------------------------------------------#
    print("PASSO 8 - COLOCOU A QUANTIADE DE GOLS SOFRIDOS")


     # -----------------------------PROCURA TODOS OS ADVERSÁRIOS DA RODADA----------------------------------------#
    for link in tabela("tr", "table-row"):
        if jogos(link, rodadaAtualString) is not None:
            adversarios.append(jogos(link, rodadaAtualString))

    for adversario in adversarios:
        mando_fora.append(adversario['Fora'])

    # -----------------------------------------------------------------------------------------------------------#
    print("PASSO 8.1 - ACHOU OS ADVERSÁRIOS")


    # ------------------------------CALCULO DE CLUSTER DOS JOGADORES---------------------------------------------#
    for jogador in jogadores:
        m = float(jogador['Media']) * 5  # MEDIA DO JOGADOR
        mt = (float(jogador['Media do time'])) * 3  # MEDIA DO TIME
        j = int(jogador['Jogos']) / rodadaAtual # QUANTIDADE DE JOGOS

        jogador['Cluster'] = (mt + m)/8

        if jogador["Cluster"] < 0:
            jogador["Cluster"] = jogador["Cluster"] - (jogador["Cluster"] * (1-j))
        else:
            jogador['Cluster'] = jogador['Cluster'] * j
        
        if jogador["Time"] in mando_fora:
            if jogador["Cluster"] < 0:
                jogador["Cluster"] = jogador["Cluster"] + (jogador["Cluster"] * (1-jogador['Aproveitamento Fora']))
            else:
                jogador["Cluster"] = jogador["Cluster"] * jogador['Aproveitamento Fora']
        else:
            if jogador["Cluster"] < 0:
                jogador["Cluster"] = jogador["Cluster"] + (jogador["Cluster"] * (1-jogador['Aproveitamento Casa']))
            else:
                jogador["Cluster"] = jogador["Cluster"] * jogador['Aproveitamento Casa']

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
                gols_feitos = 0.7 / rodadaAtual
                if jogador["Cluster"] < 0:
                    jogador["Cluster"] = jogador["Cluster"] - (jogador["Cluster"] * (1/gols_feitos))
                else:
                    jogador["Cluster"] = jogador["Cluster"] * gols_feitos
            else:
                gols_feitos = jogador["Gols equipe"] / rodadaAtual
                if jogador["Cluster"] < 0:
                    jogador["Cluster"] = jogador["Cluster"] - (jogador["Cluster"] * (1/gols_feitos))
                else:
                    jogador["Cluster"] = jogador["Cluster"] * gols_feitos

        if jogador["Posiçao"] == "Zagueiro" or jogador["Posiçao"] == "Lateral" \
                or jogador[
                    "Posiçao"] == 'Goleiro':  # DIVIDE O CLUSTER POR MEDIA DE GOLS SOFRIDOS POR PARTIDA PARA DESEFA
            if jogador["Gols sofridos equipe"] != 0:
                gols_sofridos = int(jogador["Gols sofridos equipe"]) / rodadaAtual
                if jogador["Cluster"] < 0:
                    jogador["Cluster"] = jogador["Cluster"] - (jogador["Cluster"] / gols_sofridos)
                else:
                    jogador["Cluster"] = jogador["Cluster"] / gols_sofridos
            else:
                gols_sofridos = 0.7 / rodadaAtual
                if jogador["Cluster"] < 0:
                    jogador["Cluster"] = jogador["Cluster"] - (jogador["Cluster"] / gols_sofridos)
                else:
                    jogador["Cluster"] = jogador["Cluster"] / gols_sofridos

        if int(jogador["Jogos"]) == 1:
            jogador["Para valorizar"] = jogador["Preço"] * 0.75
            jogador["Para valorizar"] = jogador["Para valorizar"] - jogador["Media"]

    print("PASSO 9 - CALCULOU O CLUSTER DOS JOGADORES")

    #jogadores.sort(key=lambda valor: (valor['Posiçao'], valor['Cluster']), reverse=True)
    #for jogador in jogadores:
    #    print(jogador)
    #    print()
    # ------------------------CLUSTERIZA OS TIMES PARA A RODADA E SOMA O CLUSTER DO TIME EM CADA JOGADOR---------#

    for classi in serie_a:
        i = 0
        for jogador in jogadores:
            if jogador["Status"] == 'provavel':
                if jogador["Posiçao"] == 'Atacante' or jogador["Posiçao"] == 'Meia':
                    if jogador['Time'] == classi['Clube']:
                        classi["Cluster Time Ataque"] = classi["Cluster Time Ataque"] + jogador['Cluster']
                        i += 1
        if i > 0:
            classi["Cluster Time Ataque"] = classi["Cluster Time Ataque"] / i

    for classi in serie_a:
        i = 0
        for jogador in jogadores:
            if jogador["Status"] == 'provavel':
                if jogador["Posiçao"] == 'Zagueiro' or jogador["Posiçao"] == 'Lateral' or jogador["Posiçao"] == 'Goleiro':
                    if jogador['Time'] == classi['Clube']:
                        classi["Cluster Time Defesa"] = classi["Cluster Time Defesa"] + jogador['Cluster']
                        i += 1
        if i > 0:
            classi["Cluster Time Defesa"] = classi["Cluster Time Defesa"] / i

    for classi in serie_a:
        classi["Cluster Time Media"] = (classi["Cluster Time Ataque"] + classi["Cluster Time Defesa"]) / 2

    # -----------------------------------------------------------------------------------------------------------#
    print("PASSO 10 - CLUSTERIZOU OS TIMES PARA A RODADA")

   
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
                    jogador["Cluster"] = (jogador["Cluster"] - classi["Cluster Time Defesa"])
                   

    for jogador in jogadores:
        for classi in serie_a:
            if jogador["Adversario"] == classi["Clube"]:
                if jogador["Posiçao"] == 'Zagueiro' or jogador["Posiçao"] == 'Lateral' or jogador["Posiçao"] == 'Goleiro' and classi["Cluster Time Ataque"] > 0:
                    jogador["Cluster"] = (jogador["Cluster"] - classi["Cluster Time Ataque"])

    for classi in serie_a:
        i = 0
        media_para_tecnico = 0
        for jogador in jogadores:
            if jogador["Time"] == classi["Clube"] and jogador["Status"] == 'provavel' and jogador["Posiçao"] != 'Técnico':
                media_para_tecnico = media_para_tecnico + jogador["Cluster"]
                i += 1
        if i > 0:
            classi["Cluster Time Rodada"] = media_para_tecnico/i

    for jogador in jogadores:
        for classi in serie_a:
            if jogador["Posiçao"] == 'Técnico':
                if jogador["Time"] == classi["Clube"]:
                    jogador["Cluster"] = classi["Cluster Time Rodada"]
    # -----------------------------------------------------------------------------------------------------------#
    print("PASSO 11 - ATUALIZOU OS CLUSTERS DOS JOGADORES COM O DO TIME ADVERSÁRIO")

    # ---------------------------ORDENA A LISTA DE JOGADORES-----------------------------------------------------#
    jogadores.sort(key=lambda valor: (valor['Posiçao'], valor['Cluster']), reverse=True)
    serie_a.sort(key=lambda valor: valor['Cluster Time Rodada'], reverse=True)
    # -----------------------------------------------------------------------------------------------------------#
    print("PASSO 12 - ORDENOU AS LISTAS jogadores E serie_a")

    # -----------------------------SALVA AS PRINCIPAIS INFORMAÇÕES EM UM ARQUIVO TXT-----------------------------#
    with open(arquivo_dif, 'w', encoding="utf8") as melhores:
        for jogador in jogadores:
            melhores.write(jogador['Posiçao'] + ' - ' + jogador['Nome'] + ' - ' + jogador['Time'] + ' - C$' + str(
                jogador['Preço']) + ' - ' + jogador["Status"] + ' - (%.2f)' % (jogador["Cluster"]))
            melhores.write('\n')
            melhores.write(150 * '-')
            melhores.write('\n')
    # -----------------------------------------------------------------------------------------------------------#


    # ---------------------------SALVA OS VINTE MELHORES JOGADORES DE CADA POSIÇÃO EM UM ARQUIVO TXT-------------#
    with open(arquivo_20_dif, 'w', encoding="utf8") as melhores:
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
    with open(arquivo_val, 'w', encoding="utf8") as melhores:
        jogadores.sort(key=lambda valor: (valor['Posiçao'], valor['Para valorizar'], valor['Preço']))
        for jogador in jogadores:
            if int(jogador["Jogos"]) == 1 and jogador["Status"] == 'provavel':
                melhores.write(jogador['Posiçao'] + ' - ' + jogador['Nome'] + ' - ' + jogador['Time'] + ' - C$' + str(
                    jogador['Preço']) + ' - ' + jogador["Status"] + ' - (%.2f)' % (jogador["Para valorizar"]))
                melhores.write('\n')
                melhores.write(150 * '-')
                melhores.write('\n')
    # ------------------------------------------------------------------------------------------------------------#
    print("PASSO 13 - SALVOU TODAS AS INFORMAÇÕES NOS ARQUIVOS .TXT")

    # --------------------------PRINTA TODAS AS INFORMAÇÕES DOS JOGADORES----------------------------------------#
    # for jogador in jogadores:
    #    print(jogador)
    #    print()
    # -----------------------------------------------------------------------------------------------------------#


    # --------------------------PRINTA TODAS AS INFORMAÇÕES DOS CLUBES-------------------------------------------#
    #for classi in serie_a:
    #    print()
    #    print(classi)
    # -----------------------------------------------------------------------------------------------------------#

