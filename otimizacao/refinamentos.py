from config import *
from solucao import *
from funcoes_auxiliares import *

#retorna o indice da instalação ideal para determinado clinte
def busca_menor_alocacao_cliente(solucao_inicial_dim_cliente,solucao_inicial_dim_insta,dados_plantas,dados_clientes,vetor_uso_demanda,ind_cliente,first,sentido):

   #variaveis de estado   
   solucao_temp = copy.deepcopy(dict(solucao_inicial_dim_cliente))
   ind_menor_custo = -1
   ind_do_outro_trocado = -1 
   antiga_insta_melhor = -1
   ind_insta_maior_cliente = solucao_inicial_dim_cliente['instalacao'][ind_cliente]

   #determina o sentido que vai percorrer
   inicio = 0
   final = len(vetor_uso_demanda)
   incr = 1
   if(first and sentido == -1):
      inicio = final-1
      final = -1
      incr = -1 

   #percorre o vetor de custo do cliente para cada instalações em busca da melhor instalação para esse cliente
   for i in range(inicio,final,incr):

      #gera vizinho
      copia_solucao = copy.deepcopy(dict(solucao_inicial_dim_cliente))
      antiga_insta = copia_solucao['instalacao'][ind_cliente]
      copia_solucao['instalacao'][ind_cliente] = i
      copia_solucao['custo'][ind_cliente] = dados_clientes['custo'][ind_cliente][i]
      
      #percorre o vetor de clientes alocados em busca de tirar o melhor
      for j in range(0,len(solucao_inicial_dim_insta[i])):
         copia_solucao['instalacao'][solucao_inicial_dim_insta[i][j]] = antiga_insta
         copia_solucao['custo'][j] = dados_clientes['custo'][j][antiga_insta]
         

         #print("\t valor_objetivo %d" %(copia_solucao['total']))
        
         #aplica restrição de capacidade         
         if( ( dados_plantas['capacidade'][ind_insta_maior_cliente] >= ( vetor_uso_demanda[ind_insta_maior_cliente] - dados_clientes['demanda'][ind_cliente] 
                                                                        + dados_clientes['demanda'][j] ) )
                  and ( dados_plantas['capacidade'][i] >= (vetor_uso_demanda[i] - dados_clientes['demanda'][j]
                                                                        + dados_clientes['demanda'][ind_cliente]))):

            copia_solucao['total'] = calcula_funcao_objetivo(copia_solucao)   
            # se a função objetivo do vizinho for menor
            if(copia_solucao['total'] < solucao_temp['total']):                     
               solucao_temp = copia_solucao   
               ind_menor_custo = i
               ind_do_outro_trocado = j 
               antiga_insta_melhor = antiga_insta
               #print('melhor') 
               #se for metodo first 
               if(first): 
                  #corrige vetor de demandas
                  vetor_uso_demanda[ind_insta_maior_cliente] -= dados_clientes['demanda'][ind_cliente]
                  vetor_uso_demanda[ind_insta_maior_cliente] += dados_clientes['demanda'][ind_do_outro_trocado]
                  vetor_uso_demanda[ind_menor_custo] -= dados_clientes['demanda'][ind_do_outro_trocado]
                  vetor_uso_demanda[ind_menor_custo] += dados_clientes['demanda'][ind_cliente]

                  #corrige dimensão de instalação
                  solucao_inicial_dim_insta[antiga_insta_melhor][solucao_inicial_dim_insta[antiga_insta_melhor].index(ind_cliente)] = solucao_inicial_dim_insta[ind_menor_custo][ind_do_outro_trocado]
                  solucao_inicial_dim_insta[ind_menor_custo][ind_do_outro_trocado] = ind_cliente

                  #Abaixa todas as flags
                  solucao_temp['flag_uso'] = np.zeros(len(dados_clientes['demanda']))
                  return solucao_temp     
         #else:
            #print("quebrou restrição")        

   if(ind_menor_custo >= 0):
      #codigo é igual lá de cima
      vetor_uso_demanda[ind_insta_maior_cliente] -= dados_clientes['demanda'][ind_cliente]
      vetor_uso_demanda[ind_insta_maior_cliente] += dados_clientes['demanda'][ind_do_outro_trocado]
      vetor_uso_demanda[ind_menor_custo] -= dados_clientes['demanda'][ind_do_outro_trocado]
      vetor_uso_demanda[ind_menor_custo] += dados_clientes['demanda'][ind_cliente]
      solucao_inicial_dim_insta[antiga_insta_melhor][solucao_inicial_dim_insta[antiga_insta_melhor].index(ind_cliente)] = solucao_inicial_dim_insta[ind_menor_custo][ind_do_outro_trocado]
      solucao_inicial_dim_insta[ind_menor_custo][ind_do_outro_trocado] = ind_cliente
      solucao_temp['flag_uso'] = np.zeros(len(dados_clientes['demanda']))
      solucao_inicial_dim_cliente = solucao_temp
   else:
      #caso não consiga nenhuma mudança levanta flag
      solucao_inicial_dim_cliente['flag_uso'][ind_cliente] = 1 
             

   print("Objetivo refinado: %d" %(solucao_temp['total']))
   return solucao_inicial_dim_cliente

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

def avalia_restricao(vetor_demandas_atendidas,dados_plantas):
   ret = True
   for i in range(0,len(vetor_demandas_atendidas)):
      print("%d -- %d" %(i,dados_plantas['capacidade'][i] - vetor_demandas_atendidas[i]))
      if(dados_plantas['capacidade'][i] < vetor_demandas_atendidas[i]):
         ret = False
   return ret


def refina_sem_abrir(solucao_inicial_vect,dados_clientes_vect,dados_plantas_vect,passos,first):
  
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

   solucao_inicial_dim_cliente = {
    'instalacao': np.array(solucao_inicial_vect['instalacao']),
    'custo': np.array(solucao_inicial_vect['custo']),
    'flag_uso' : np.zeros(len(dados_clientes['demanda'])),    
    'total': int
   }   

#cria dimensão das instalações
   solucao_inicial_dim_insta = cria_vetor_solucao(solucao_inicial_dim_cliente,dados_plantas)
#calcula função objetivo 
   solucao_inicial_dim_cliente['total'] = calcula_funcao_objetivo(solucao_inicial_dim_cliente)
   print("Objetivo Construtiva: %d" %( solucao_inicial_dim_cliente['total']))
#cria vetor de demanda usadas
   vetor_uso_demanda_insta = calcula_uso_demanda(solucao_inicial_dim_cliente,dados_plantas,dados_clientes)

   flag_sentido = 1
   for i in range(0,passos):
      #busca maior
      ind_maior_cliente_alocado = busca_maior(solucao_inicial_dim_cliente)
            
      #se achar um maior que possa ser movimentaaado
      if(ind_maior_cliente_alocado >= 0):

         print("Maior escolhido %d em %d" %(solucao_inicial_dim_cliente['custo'][ind_maior_cliente_alocado],ind_maior_cliente_alocado))
         
         solucao_inicial_dim_cliente = busca_menor_alocacao_cliente( solucao_inicial_dim_cliente,
                                                         solucao_inicial_dim_insta,
                                                         dados_plantas,
                                                         dados_clientes,
                                                         vetor_uso_demanda_insta,
                                                         ind_maior_cliente_alocado,
                                                         first,
                                                         flag_sentido)        
      else: break                                                   
      #se execucao busca apenas o primeiro inverte o sentido
      if(first):
         flag_sentido *= -1                                                
      
      print("-------------------")
   if(not avalia_restricao(vetor_uso_demanda_insta,dados_plantas)):
      print("RESTRIÇÃO QUEBRADA")

   return solucao_inicial_dim_cliente 
