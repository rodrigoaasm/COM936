import copy
import numpy as np

inst = "p55"

caminho = "../dataset/" + inst + ".txt"

validade_tabu = 3

# Possiveis
#   'gulosa'
#   'aleatoria'
#   'hibrida'

estrategia = 'gulosa'

estrategias = ['gulosa_delimitada_demanda']

erros_solucao = []
