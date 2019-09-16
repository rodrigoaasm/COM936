from config import *
from solucao import *

#retorna o indice da instalação ideal para determinado clinte
def busca_menor_alocacao_cliente(vec_custos_insta,dados_plantas,dados_clientes,vetor_uso_demanda,ind_cliente):
   menor_custo = vec_custos_insta[0]
   menor_indice = 0
   for i in range(1,len(vec_custos_insta)):
      # se for o menor e a sua alocação não quebre a restrição, então é o conjunto ideal
      if (vec_custos_insta[i] < menor_custo and
            dados_plantas['capacidade'][i] >= vetor_uso_demanda[i] + dados_clientes['demanda'][ind_cliente]):
         menor_custo = vec_custos_insta[i]
         menor_indice = i
   return menor_indice

#Cria um vetor p/ armezenar as alocações
def calcula_uso_demanda(solucao,dados_plantas):
   vetor_gasto_demanda =  np.zeros(len(dados_plantas['capacidade']))
   for i in range(0,len(solucao['instalacao'])):
      vetor_gasto_demanda[solucao['instalacao'][i]] += solucao['custo'][i]
   return vetor_gasto_demanda


def refina_sem_abrir(solucao_inicial_vect,dados_clientes_vect,dados_plantas_vect,passos): #dados_clientes,dados_plantas,match) :

   print("--------------------------------refinamento ------------------")
   dados_clientes = {
    'custo': np.array(dados_clientes_vect['custo']),
    'demanda':  np.array(dados_clientes_vect['demanda']),
    'disponivel':  np.array(dados_clientes_vect['disponivel']),
    'posicao':  np.array(dados_clientes_vect['posicao']),
   }  

   dados_plantas = {
      'custo':  np.array(dados_plantas_vect['custo']),
      'capacidade': np.array(dados_plantas_vect['capacidade']),
      'posicao': np.array(dados_plantas_vect['posicao']),
   }

   solucao_inicial = {
    'instalacao': np.array(solucao_inicial_vect['instalacao']),
    'custo': np.array(solucao_inicial_vect['custo']),
   }

   valor_obj_atual = calcula_funcao_objetivo(solucao_inicial)
   print("Objetivo Construtiva: %d" %(valor_obj_atual))

   vetor_uso_demanda_insta = calcula_uso_demanda(solucao_inicial,dados_plantas)

   for i in range(0,passos):
      #busca maior
      ind_maior_cliente_alocado = solucao_inicial['custo'].argmax()

      print("Maior escolhido %d" %(solucao_inicial['custo'][ind_maior_cliente_alocado]))
      #se o numero negativo para iteração
      if(solucao_inicial['custo'][ind_maior_cliente_alocado] <= 0):
         break

      #menor instalação para o maior cliente
      ind_teste = dados_clientes['custo'][ind_maior_cliente_alocado].argmin()

      #pega a instalação ideal para esse cliente
      ind_menor_insta = busca_menor_alocacao_cliente(dados_clientes['custo'][ind_maior_cliente_alocado],
                                                         dados_plantas,dados_clientes,vetor_uso_demanda_insta,
                                                         ind_maior_cliente_alocado)

      #instancia possivel solução      
      copia_solucao = copy.deepcopy(solucao_inicial) #dict(solucao_inicial))
      copia_solucao['instalacao'][ind_maior_cliente_alocado] = ind_menor_insta
      copia_solucao['custo'][ind_maior_cliente_alocado] = dados_clientes['custo'][ind_maior_cliente_alocado][ind_menor_insta]

      valor_sum_vizinho = calcula_funcao_objetivo(copia_solucao)
      #avalia se o vizinho analisado é o melhor
      if(valor_sum_vizinho < valor_obj_atual): 
         vetor_uso_demanda_insta[solucao_inicial['instalacao'][ind_maior_cliente_alocado]] -= dados_clientes['demanda'][ind_maior_cliente_alocado]
         vetor_uso_demanda_insta[ind_menor_insta] += dados_clientes['demanda'][ind_maior_cliente_alocado] #atualiza vetor de demandas
         solucao_inicial = copia_solucao #o vizinho passa ser o melhor
         valor_obj_atual = valor_sum_vizinho #guarda o valor objetivo
      else:
         solucao_inicial['custo'][ind_maior_cliente_alocado] *= -1

      print("Objetivo refinado: %d" %(valor_obj_atual))
      print("-------------------")

   return solucao_inicial
