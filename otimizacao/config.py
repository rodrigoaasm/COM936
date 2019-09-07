dados_clientes = {
    'custo': [],
    'demanda': [],
    'disponivel': [],
    'posicao': []
}

dados_plantas = {
    'custo': [],
    'capacidade': [],
    'posicao': []
}

solucao = []

inst = "p3"

caminho = "../dataset/" + inst + ".txt"


# Possiveis
#   'gulosa'
#   'aleatoria'
#   'hibrida'

estrategia = 'gulosa'
