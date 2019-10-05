import traceback as tb
import numpy as np
from time import time
import sys
import config

from config import *
from entrada_saida import *
from funcoes_auxiliares import*
from solucao import*
from construtiva import*
from refinamentos import*


if __name__ == '__main__':

    for p in range(1, 58): #para executar para todos os datasets basta colocar 58 no fim do range
        print('------P{}--------------------------------------------'.format(p))
        dados_clientes, dados_plantas, solucao = zera_vetores()
        caminho = "../dataset/p" + str(p) + ".txt"
   
        entrada_dados(dados_clientes,dados_plantas, caminho)
        criaSolInicial(dados_clientes,dados_plantas,solucao)
        solucao = chama_refinamento(solucao,dados_clientes,dados_plantas,False)
        solucao = cria_vetor_solucao(solucao,dados_plantas)
        saida_dados_format(solucao)

        #try:
        #    criaSolInicial(dados_clientes, dados_plantas, solucao)
        #    solucao = refina_sem_abrir(solucao,dados_clientes,dados_plantas,200,True)
        #except ValueError as e:
        #    print_error()
        #except IndexError as e:
        #    print_error()
        #print('---SOLUCOES---')
        #print('p{} -->  {}'.format(p, solucao))
        #solucao = formataSaida(solucao,dados_plantas)
        #print(solucao)

    
