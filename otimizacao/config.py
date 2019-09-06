dados_clientes = {
    'custo': [],
    'demanda': [],
    'posicao': [],
    'disponivel': []
}


dados_plantas = {
    'custo': [],
    'capacidade': []
}

solucao = []

inst = "p3"

caminho = "../dataset/" + inst + ".txt"


# Possiveis
#   'gulosa'
#   'aleatoria'
#   'hibrida'

estrategia = 'gulosa'
