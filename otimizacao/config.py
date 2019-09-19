import copy
import numpy as np
import time as time

inst = "p3"

caminho = "../dataset/" + inst + ".txt"

# Possiveis
#   'gulosa'
#   'aleatoria'
#   'hibrida'

estrategia = 'gulosa'

estrategias = ['aleatoria']

erros_solucao = []
