import numpy as np
from time import time

from config import *
from funcoes_auxiliares import *
from solucao import *
from refinamentos import *


if __name__ == '__main__':
   
  entrada_dados(dados_clientes,dados_plantas)
  criaSolInicial(dados_clientes,dados_plantas,solucao)
  solucao = chama_refinamento(solucao,dados_clientes,dados_plantas,2700,False)
  solucao = cria_vetor_solucao(solucao,dados_plantas)
  saida_dados_format(solucao)

  
