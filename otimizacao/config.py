import copy
import numpy as np

inst = "p55"

caminho = "../dataset/" + inst + ".txt"

# Possiveis
#   'gulosa'
#   'aleatoria'
#   'hibrida'

estrategia = 'gulosa'

estrategias = ['gulosa_delimitada_demanda']

erros_solucao = []
