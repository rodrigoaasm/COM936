from time import time
from auxiliares.funcoes_avaliacao import *
from auxiliares.funcoes_auxiliares import *

#gera um conjunto de vizinhos por diversificação e busca melhor solução
def busca_local_por_diversificacao(solucao_inicial_dim_cliente,solucao_inicial_dim_insta,dados_plantas,dados_clientes,vetor_uso_demanda,ind_cliente,first,sentido):

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
      
      #percorre o vetor de clientes alocados e busca de tirar o melhor
      for j in range(0,len(solucao_inicial_dim_insta[i])):
         copia_solucao['instalacao'][solucao_inicial_dim_insta[i][j]] = antiga_insta
         copia_solucao['custo'][j] = dados_clientes['custo'][j][antiga_insta]         
        
         #aplica restrição de capacidade         
         if( ( dados_plantas['capacidade'][ind_insta_maior_cliente] >= ( vetor_uso_demanda[ind_insta_maior_cliente] - dados_clientes['demanda'][ind_cliente] 
                                                                        + dados_clientes['demanda'][j] ) )
                  and ( dados_plantas['capacidade'][i] >= (vetor_uso_demanda[i] - dados_clientes['demanda'][j]
                                                                        + dados_clientes['demanda'][ind_cliente]))):

            copia_solucao['total'] = calcula_funcao_objetivo(copia_solucao, dados_plantas)
            # se a função objetivo do vizinho for menor
            if(copia_solucao['total'] < solucao_temp['total']):                
               solucao_temp = copy.deepcopy(dict(copia_solucao))
               ind_menor_custo = i
               ind_do_outro_trocado = j 
               antiga_insta_melhor = antiga_insta
               #se for metodo first 
               if(first): 
                  #corrige vetor de demandas
                  vetor_uso_demanda[ind_insta_maior_cliente] -= dados_clientes['demanda'][ind_cliente]
                  vetor_uso_demanda[ind_insta_maior_cliente] += dados_clientes['demanda'][ind_do_outro_trocado]
                  vetor_uso_demanda[ind_menor_custo] -= dados_clientes['demanda'][ind_do_outro_trocado]
                  vetor_uso_demanda[ind_menor_custo] += dados_clientes['demanda'][ind_cliente]

                  #Abaixa todas as flags
                  solucao_temp['flag_uso'] = np.zeros(len(dados_clientes['demanda']))
                  return solucao_temp    

   if(ind_menor_custo >= 0):
      #codigo é igual lá de cima
      vetor_uso_demanda[ind_insta_maior_cliente] -= dados_clientes['demanda'][ind_cliente]
      vetor_uso_demanda[ind_insta_maior_cliente] += dados_clientes['demanda'][ind_do_outro_trocado]
      vetor_uso_demanda[ind_menor_custo] -= dados_clientes['demanda'][ind_do_outro_trocado]
      vetor_uso_demanda[ind_menor_custo] += dados_clientes['demanda'][ind_cliente]

      solucao_temp['flag_uso'] = np.zeros(len(dados_clientes['demanda']))      
      solucao_inicial_dim_cliente = solucao_temp      
   else:
      #caso não consiga nenhuma mudança levanta flag
      solucao_inicial_dim_cliente['flag_uso'][ind_cliente] = 1 

   return solucao_inicial_dim_cliente


def refina_sem_abrir(solucao_inicial_dim_cliente,dados_clientes,dados_plantas,first):
  
   #cria dimensão das instalações
   solucao_inicial_dim_insta = cria_vetor_solucao(solucao_inicial_dim_cliente,dados_plantas)
   #calcula função objetivo 
   solucao_inicial_dim_cliente['total'] = calcula_funcao_objetivo(solucao_inicial_dim_cliente, dados_plantas)
   #cria vetor de demanda usadas
   vetor_uso_demanda_insta = calcula_uso_demanda(solucao_inicial_dim_cliente,dados_plantas,dados_clientes)
   solucao_inicial_dim_cliente['flag_uso'] = np.zeros(len(dados_clientes['demanda']))

   flag_sentido = 1
   ind_maior_cliente_alocado = busca_maior(solucao_inicial_dim_cliente)
   while(ind_maior_cliente_alocado >= 0):     

      solucao_inicial_dim_cliente = busca_local_por_diversificacao( solucao_inicial_dim_cliente,
                                                         solucao_inicial_dim_insta,
                                                         dados_plantas,
                                                         dados_clientes,
                                                         vetor_uso_demanda_insta,
                                                         ind_maior_cliente_alocado,
                                                         first,
                                                         flag_sentido)  
         
      solucao_inicial_dim_insta = cria_vetor_solucao(solucao_inicial_dim_cliente,dados_plantas)
                                                 
      #Inverte o sentido se for metodo first
      if(first):
         flag_sentido *= -1     

      #busca maior
      ind_maior_cliente_alocado = busca_maior(solucao_inicial_dim_cliente)                                           

   return solucao_inicial_dim_cliente 

def chama_refinamento(solucao_inicial_vect,dados_clientes_vect,dados_plantas_vect,first):
    hora_inicio = time()
    solucao = refina_sem_abrir(solucao_inicial_vect,dados_clientes_vect,dados_plantas_vect,first)
    hora_fim = time()
    tempo_execucao = hora_fim - hora_inicio
    print('Tempo de execução da estratégia refinamento: {}ms'.format(tempo_execucao))
    return solucao

