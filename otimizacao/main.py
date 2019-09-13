import numpy as np
from time import time

from config import *
from funcoes_auxiliares import *
from solucao import *


if __name__ == '__main__':
    entrada_dados()
    calcula_cxb()

    criaSolInicial()
    calcula_funcao_objetivo()

    saida_dados([dados_clientes], 'clientes')
    saida_dados([dados_plantas], 'plantas')
