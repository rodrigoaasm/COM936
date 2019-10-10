import copy
import numpy as np

inst = "p55"

caminho = "../dataset/" + inst + ".txt"

validade_tabu = 4
max_tentativas = 10

# Possiveis
#   'gulosa'
#   'aleatoria'
#   'hibrida'

estrategia = 'gulosa'

estrategias = ['gulosa']

erros_solucao = []
