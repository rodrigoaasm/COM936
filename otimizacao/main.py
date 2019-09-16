import numpy as np
from time import time

from config import *
from funcoes_auxiliares import *
from solucao import *
from refinamentos import *


if __name__ == '__main__':
   
  entrada_dados(dados_clientes,dados_plantas)
  #  calcula_cxb(dados_plantas)

  criaSolInicial(dados_clientes,dados_plantas,solucao)
  solucao = refina_sem_abrir(solucao,dados_clientes,dados_plantas,200)
  #solucao = formataSaida(solucao)
  print(solucao)
  
