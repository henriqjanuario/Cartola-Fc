from ClusterCartolaFcDivisão import *
from ClusterCartolaFcDiferença import *


time_tipo_1 = ["Grêmio", "Flamengo", "Corinthians", "Palmeiras", "Atlético-MG", "São Paulo", "Santos", "Cruzeiro"]
time_tipo_2 = ["Fluminense", "Ponte Preta", "Coritiba", "Vasco", "Atlético-PR", "Chapecoense"]
time_tipo_3 = ["Bahia", "Vitória", "Avaí", "Atlético-GO", "Sport", "Botafogo"]

print(10*'-' + 'DIVISÃO' + 10*'-')
divisao(time_tipo_1, time_tipo_2, time_tipo_3)
print(10*'-' + 'DIFERENÇA' + 10*'-')
diferenca(time_tipo_1, time_tipo_2, time_tipo_3)