import numpy as np
from time import time

from config import *
from funcoes_auxiliares import *
from solucao import *


if __name__ == '__main__':

    # refina_sem_abrir(solucao,4)
    entrada_dados(dados_clientes, dados_plantas)
    calcula_cxb(dados_plantas)
    
    criaSolInicial(dados_clientes, dados_plantas, solucao)
    #valor = calcula_funcao_objetivo(solucao)
    #print("Valor Obtido: %d" %valor)

    #saida_dados([dados_clientes], 'clientes')
    #saida_dados([dados_plantas], 'plantas')
