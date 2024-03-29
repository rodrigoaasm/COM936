from time import time
import numpy as np
from config import *


#Função que calcula a função objetivo, ou seja, o custo de abertura das instalações mais de alocação de cada cliente
def calcula_funcao_objetivo(solucao, dados_plantas):
    valor = 0
    insta = [] #vetor que guardará as instalações já somadas aos custos, para que não se repitam
    for i in range(0, len(solucao['instalacao'])):
        if not insta.__contains__(solucao['instalacao'][i]):#verifica se a instalação já foi atribuida, senao considera seu valor
            valor += dados_plantas['custo'][solucao['instalacao'][i]]  # atribui ao valor, o custo de abertura de cada instalação
            insta.append(solucao['instalacao'][i]) # e a insere no vetor de instalações, para que seu valor não seja contado novamente 
        valor += abs(solucao['custo'][i]) #considera o custo de alocacao de cada cliente para cada instalação

    return valor

def avalia_restricao(vetor_demandas_atendidas,dados_plantas):
   ret = True
   for i in range(0,len(vetor_demandas_atendidas)):
      if(dados_plantas['capacidade'][i] < vetor_demandas_atendidas[i]):
         ret = False
   return ret

def busca_maior(solucao_inicial):
   ind_maior = -1
   maior_valor = -1
   for i in range(0,len(solucao_inicial['instalacao'])):      
      if(solucao_inicial['custo'][i] > maior_valor and solucao_inicial['flag_uso'][i] != 1):    
         maior_valor = solucao_inicial['custo'][i]
         ind_maior = i
   return ind_maior  

#Cria um vetor p/ armezenar as alocações
def calcula_uso_demanda(solucao,dados_plantas,dados_clientes):
   vetor_gasto_demanda =  np.zeros(len(dados_plantas['capacidade']))
   for i in range(0,len(solucao['instalacao'])):
      vetor_gasto_demanda[solucao['instalacao'][i]] += dados_clientes['demanda'][i]
   return vetor_gasto_demanda


