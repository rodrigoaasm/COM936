from config import *
from solucao import*

import numpy as np

def refina_sem_abrir(solucao_inicial,passos): #dados_clientes,dados_plantas,match) :

   dados_clientes = {
      "custo" : np.array([[21,23,19,41],[30,40,34,50],[25,36,46,50],[12,40,51,33],[15,20,22,40],[10,30,15,25]]),
      "demanda" : np.array([100,200,100,50,60,90])
   }   
   dados_plantas = {
      'capacidade': [500,400,600,700],
      'custo': [50,40,90,60]
   }

   solucao_inicial = np.array([[1,2,1,3,0,0],[23,34,36,33,15,10]]) 
   
   #-----solucao é a partir daqui----------------------------------------------------------------
   valor_obj_atual = solucao_inicial[1].sum()
   vetor_uso_demanda_insta = np.array([150,200,200,50])

   for i in range(0,passos):
      ind_maior_cliente_alocado = solucao_inicial[1].argmax()
      #menor instalação para o maior cliente
      ind_menor_insta = dados_clientes['custo'][ind_maior_cliente_alocado].argmin()
      
      #avaliar restrições    
      if(dados_plantas['capacidade'][ind_menor_insta] >= vetor_uso_demanda_insta[ind_menor_insta] + dados_clientes['demanda'][ind_maior_cliente_alocado]):
         copia_solucao = copy.deepcopy(solucao_inicial) #dict(solucao_inicial))
         copia_solucao[0][ind_maior_cliente_alocado] = ind_menor_insta
         copia_solucao[1][ind_maior_cliente_alocado] = dados_clientes['custo'][ind_maior_cliente_alocado][ind_menor_insta]

         valor_sum_vizinho = 0
         #calcula funcao objetivo
         for j in range(0,len(copia_solucao[1])):     
            if copia_solucao[1][j] < 0:   
               valor_sum_vizinho += copia_solucao[1][j] *-1 
            else:
               valor_sum_vizinho += copia_solucao[1][j]

         if(valor_sum_vizinho < valor_obj_atual): #avalia se o vizinho analisado é melhor
            vetor_uso_demanda_insta[solucao_inicial[0][ind_maior_cliente_alocado]] -= dados_clientes['demanda'][ind_maior_cliente_alocado]
            vetor_uso_demanda_insta[ind_menor_insta] += dados_clientes['demanda'][ind_maior_cliente_alocado] #atualiza vetor de demandas
            solucao_inicial = copia_solucao #o vizinho passa ser o melhor
            valor_obj_atual = valor_sum_vizinho #guarda o valor objetivo
         else:
            solucao_inicial['custo'][ind_maior_cliente_alocado] *= -1

      else:
         print("estorou[%d]" %(ind_maior_cliente_alocado))

      print(solucao_inicial)
      print(vetor_uso_demanda_insta)
      print("Objetivo: %d" %(valor_obj_atual))

   return
