import copy
import numpy as np


dados_clientes = {
    'custo': [],
    'demanda': [],
    'disponivel': [],
    'posicao': []
}

dados_plantas = {
    'custo': [],
    'capacidade': [],
    'posicao': [],
}

solucao = {
    'instalacao': [],
    'custo': [],
    'total': int
}

inst = "p3"

caminho = "../dataset/" + inst + ".txt"

# Possiveis
#   'gulosa'
#   'aleatoria'
#   'hibrida'

estrategia = 'aleatoria'

estrategias = ['aleatoria']
