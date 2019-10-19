import copy
import numpy as np
import random as random

inst = "p55"

caminho = "../dataset/" + inst + ".txt"

<<<<<<< .mine
validade_tabu = 400

=======
validade_tabu = 4
max_tentativas = 10
>>>>>>> .theirs

# Possiveis
#   'gulosa'
#   'aleatoria'
#   'hibrida'

random.seed(3)

estrategia = 'gulosa'

estrategias = ['gulosa']

erros_solucao = []
