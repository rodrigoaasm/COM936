from config import *
from solucao import*

import numpy as np

def busca_menor_alocacao_cliente(vec_custos_insta,dados_plantas,dados_clientes,vetor_uso_demanda,ind_cliente):
   menor_custo = vec_custos_insta[0]
   menor_indice = 0
   for i in range(1,len(vec_custos_insta)):
      if (vec_custos_insta[i] < menor_custo and
            dados_plantas['capacidade'][i] >= vetor_uso_demanda[i] + dados_clientes['demanda'][ind_cliente]):
         menor_custo = vec_custos_insta[i]
         menor_indice = i
   return menor_indice

def calcula_uso_demanda(solucao,dados_plantas):
   vetor_gasto_demanda =  np.zeros(len(dados_plantas['capacidade']))
   print(vetor_gasto_demanda)
   for i in range(0,len(solucao['instalacao'])):
      vetor_gasto_demanda[solucao['instalacao'][i]] += solucao['custo'][i]
   print(vetor_gasto_demanda)


def refina_sem_abrir(solucao_inicial,dados_clientes,dados_plantas,passos): #dados_clientes,dados_plantas,match) :

#   dados_clientes = {
 #     "custo" : np.array([[21,23,19,41],[30,40,34,50],[25,36,46,50],[12,40,51,33],[15,20,22,40],[10,30,15,25]]),
  #    "demanda" : np.array([100,200,100,50,60,90])
   #}   
  # dados_plantas = {
   #   'capacidade': [500,400,600,700],
    #  'custo': [5000,4000,9000,6000]
  # }

   #solucao_inicial = np.array([[1,2,1,3,0,0],[23,34,36,33,15,10]]) 
   
   #-----solucao é a partir daqui----------------------------------------------------------------
   valor_obj_atual = calcula_funcao_objetivo(solucao_inicial)

 #  vetor_uso_demanda_insta = np.array([150,200,200,50])
   calcula_uso_demanda(solucao_inicial,dados_plantas)

   for i in range(0,passos):
      ind_maior_cliente_alocado = solucao_inicial['custo'].argmax()
      #menor instalação para o maior cliente
      ind_teste = dados_clientes['custo'][ind_maior_cliente_alocado].argmin()

      ind_menor_insta = busca_menor_alocacao_cliente(dados_clientes['custo'][ind_maior_cliente_alocado],
                                                         dados_plantas,dados_clientes,vetor_uso_demanda_insta,
                                                         ind_maior_cliente_alocado)
            
      copia_solucao = copy.deepcopy(solucao_inicial) #dict(solucao_inicial))
      copia_solucao[0][ind_maior_cliente_alocado] = ind_menor_insta
      copia_solucao[1][ind_maior_cliente_alocado] = dados_clientes['custo'][ind_maior_cliente_alocado][ind_menor_insta]

      valor_sum_vizinho = calcula_funcao_objetiva(copia_solucao)

      if(valor_sum_vizinho < valor_obj_atual): #avalia se o vizinho analisado é melhor
         vetor_uso_demanda_insta[solucao_inicial[0][ind_maior_cliente_alocado]] -= dados_clientes['demanda'][ind_maior_cliente_alocado]
         vetor_uso_demanda_insta[ind_menor_insta] += dados_clientes['demanda'][ind_maior_cliente_alocado] #atualiza vetor de demandas
         solucao_inicial = copia_solucao #o vizinho passa ser o melhor
         valor_obj_atual = valor_sum_vizinho #guarda o valor objetivo
      else:
         solucao_inicial[1][ind_maior_cliente_alocado] *= -1

   print("Objetivo: %d" %(valor_obj_atual))

   return
