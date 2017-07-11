from ClusterCartolaFcDivisão import *
from ClusterCartolaFcDiferença import *


time_tipo_1 = ["Grêmio", "Flamengo", "Corinthians", "Palmeiras", "Atlético-MG", "São Paulo", "Santos", "Cruzeiro"]
time_tipo_2 = ["Fluminense", "Ponte Preta", "Coritiba", "Vasco", "Atlético-PR", "Chapecoense"]
time_tipo_3 = ["Bahia", "Vitória", "Avaí", "Atlético-GO", "Sport", "Botafogo"]

arquivo_20_div = "C:/Users/rique_000/Documents/GitHub/Cartola-Fc/Cluster/Rodada 13/20 Melhores para proxima rodada divisão.txt"
arquivo_div = "C:/Users/rique_000/Documents/GitHub/Cartola-Fc/Cluster/Rodada 13/Melhores para proxima rodada divisão.txt"
arquivo_20_dif = "C:/Users/rique_000/Documents/GitHub/Cartola-Fc/Cluster/Rodada 13/20 Melhores para proxima rodada.txt"
arquivo_dif = "C:/Users/rique_000/Documents/GitHub/Cartola-Fc/Cluster/Rodada 13/Melhores para proxima rodada.txt"
arquivo_val = "C:/Users/rique_000/Documents/GitHub/Cartola-Fc/Cluster/Rodada 13/Melhores para valorizar.txt"

rodadaAtual = 13

print(10*'-' + 'DIVISÃO' + 10*'-')
divisao(time_tipo_1, time_tipo_2, time_tipo_3, arquivo_div, arquivo_20_div, arquivo_val, rodadaAtual)
print(10*'-' + 'DIFERENÇA' + 10*'-')
diferenca(time_tipo_1, time_tipo_2, time_tipo_3, arquivo_dif, arquivo_20_dif, arquivo_val, rodadaAtual)