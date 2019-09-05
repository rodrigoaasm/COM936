import numpy as np
from time import time

from config import *
from funcoes_auxiliares import *
from solucao import *


if __name__ == '__main__':
    entrada_dados()
    calcula_cxb()
    hora_inicio = time()

    criaSolInicial()
    calcula_funcao_objetivo()


    #encontra_menor_demanda()

    hora_fim = time()

    tempo_execucao = hora_fim - hora_inicio
    hr, resto = divmod(tempo_execucao, 3600)
    min, seg = divmod(resto, 60)

    print('Tempo de execução medido: {}h {}min {}seg'.format(int(hr), int(min), seg))
    saida_dados([dados_clientes], 'clientes')
    saida_dados([dados_plantas], 'plantas')
