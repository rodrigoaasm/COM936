import copy
import numpy as np
import random as random

inst = "p55"

caminho = "../dataset/" + inst + ".txt"

validade_tabu = 400

# Possiveis
#   'gulosa'
#   'aleatoria'
#   'hibrida'

random.seed(3)

estrategia = 'gulosa'

estrategias = ['gulosa']

erros_solucao = []
