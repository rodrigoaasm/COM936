import copy

from config import*
from auxiliares.funcoes_auxiliares import *

def _cliente_cabe(demanda_cliente, capacidade_planta, utilizado_plantas, planta_pos):

    total_c_cliente = utilizado_plantas[planta_pos] + demanda_cliente

    if total_c_cliente > capacidade_planta:
        return False

    utilizado_plantas[planta_pos] += demanda_cliente
    return True

#metodo construtivo aleatório
def solucao_aleatoria(dados_clientes, dados_plantas, solucao):

    capacidade_plantas = copy.deepcopy(dados_plantas['capacidade'])
    demanda_clientes = copy.deepcopy(dados_clientes['demanda'])
    clientes_planta = [[] for item in range(0, len(capacidade_plantas))]

    clientes = [pos for pos in range(0, len(demanda_clientes))]
    plantas = [pos for pos in range(0, len(capacidade_plantas))]
    utilizado_plantas = [0 for pos in range(0, len(capacidade_plantas))]
    random.shuffle(clientes)
    random.shuffle(plantas)

    for cliente_pos in clientes:
        idx_planta = 0
        planta_pos = plantas[idx_planta]
        while not _cliente_cabe(demanda_clientes[cliente_pos],
                                capacidade_plantas[planta_pos],
                                utilizado_plantas,
                                planta_pos):
            idx_planta += 1
            planta_pos = plantas[idx_planta]
        clientes_planta[planta_pos].append(cliente_pos)

    custo_total = 0
    for planta_pos in range(0, len(clientes_planta)):
        custo_planta = sum([dados_clientes['custo'][i][planta_pos] for i in clientes_planta[planta_pos]])
        custo_total += custo_planta
        if clientes_planta[planta_pos]:
            custo_total += dados_plantas['custo'][planta_pos]

        for cliente in clientes_planta[planta_pos]:
            solucao['instalacao'][cliente] = planta_pos
            solucao['custo'][cliente] = dados_clientes['custo'][cliente][planta_pos]

    return solucao