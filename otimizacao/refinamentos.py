from config import *
from solucao import *

#retorna o indice da instalação ideal para determinado clinte
def busca_menor_alocacao_cliente(solucao_inicial,vec_custos_insta,dados_plantas,dados_clientes,vetor_uso_demanda,ind_cliente,first,sentido):
   print("\tSolucao atual: %d" %(solucao_inicial['total']))
   
   ind_menor_custo = -1
   ind_insta_maior_cliente = solucao_inicial['instalacao'][ind_cliente]

   inicio = 0
   final = len(vec_custos_insta)
   incr = 1
   if(first and sentido == -1):
      inicio = final-1
      final = -1
      incr = -1 

   for i in range(inicio,final,incr):
      #e a sua alocação não quebra a restrição      
      if (dados_plantas['capacidade'][i] >= vetor_uso_demanda[i] + dados_clientes['demanda'][ind_cliente]):  
         copia_solucao = copy.deepcopy(dict(solucao_inicial))
         copia_solucao['instalacao'][ind_cliente] = i
         copia_solucao['custo'][ind_cliente] = dados_clientes['custo'][ind_cliente][i]
         copia_solucao['total'] = calcula_funcao_objetivo(copia_solucao)
         print("\t instalação: %d valor_objetivo %d capacidade %d demanda %d" %(i,copia_solucao['total'],
            dados_plantas['capacidade'][i],vetor_uso_demanda[i]+ dados_clientes['demanda'][ind_cliente]))
         # se a função objetivo do vizinho for menor
         if(copia_solucao['total'] < solucao_inicial['total']):                     
            solucao_inicial = copia_solucao   
            ind_menor_custo = i  
              
            if(first): break #se for pelo metodo first fecha agora
            

   if(ind_menor_custo >= 0):
      vetor_uso_demanda[ind_insta_maior_cliente] -= dados_clientes['demanda'][ind_cliente]
      vetor_uso_demanda[ind_menor_custo] += dados_clientes['demanda'][ind_cliente]
      solucao_inicial['flag_uso'] = np.zeros(len(dados_clientes['demanda']))
   else:
      solucao_inicial['flag_uso'][ind_cliente] = 1        

   print("Objetivo refinado: %d" %(solucao_inicial['total']))
   return solucao_inicial

#Cria um vetor p/ armezenar as alocações
def calcula_uso_demanda(solucao,dados_plantas,dados_clientes):
   vetor_gasto_demanda =  np.zeros(len(dados_plantas['capacidade']))
   for i in range(0,len(solucao['instalacao'])):
      vetor_gasto_demanda[solucao['instalacao'][i]] += dados_clientes['demanda'][i]
   return vetor_gasto_demanda

def busca_maior(solucao_inicial):
   ind_maior = -1
   maior_valor = -1
   for i in range(0,len(solucao_inicial['instalacao'])):
      if(solucao_inicial['custo'][i] > maior_valor and solucao_inicial['flag_uso'][i] != 1):
         ind_maior = i
         maior_valor = solucao_inicial['custo'][i]
   return ind_maior     

def refina_sem_abrir(solucao_inicial_vect,dados_clientes_vect,dados_plantas_vect,passos,first): #dados_clientes,dados_plantas,match) :
  
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
    'flag_uso' : np.zeros(len(dados_clientes['demanda'])),    
    'total': int
   }   

   solucao_inicial['total'] = calcula_funcao_objetivo(solucao_inicial)
   print("Objetivo Construtiva: %d" %( solucao_inicial['total']))

   vetor_uso_demanda_insta = calcula_uso_demanda(solucao_inicial,dados_plantas,dados_clientes)
   print(vetor_uso_demanda_insta)
   print(dados_plantas_vect['capacidade'])

   flag_sentido = 1
   for i in range(0,passos):
      #busca maior
      ind_maior_cliente_alocado = busca_maior(solucao_inicial)
      #ind_maior_cliente_alocado2 = solucao_inicial['custo'].argmax()
      
      if(ind_maior_cliente_alocado >= 0):
         print("Maior escolhido %d em %d" %(solucao_inicial['custo'][ind_maior_cliente_alocado],ind_maior_cliente_alocado))    
         solucao_inicial = busca_menor_alocacao_cliente(solucao_inicial,dados_clientes['custo'][ind_maior_cliente_alocado],
                                                         dados_plantas,dados_clientes,vetor_uso_demanda_insta,
                                                         ind_maior_cliente_alocado,first,flag_sentido)
      else: break                                                   
      #se execucao busca apenas o primeiro inverte o sentido
      if(first):
         flag_sentido *= -1                                                    
      
      print("-------------------")

   return solucao_inicial 
