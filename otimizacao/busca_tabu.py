
from solucao import *

import time as time

def atualizaTabu(tabu,validade_tabu):
    for ch in list(tabu):
        tabu[ch] += 1
        if(tabu[ch]  > validade_tabu):
            del(tabu[ch])

def busca_tabu_solucao(solucao_inicial_dim_cliente,dados_clientes,dados_plantas,maxIntSemMelhorias,validade_tabu):  

    intSemMelhoria = 0
    #calcula função objetivo 
    solucao_inicial_dim_cliente['total'] = calcula_funcao_objetivo(solucao_inicial_dim_cliente, dados_plantas)
    #guarda solucao inicial como a melhor 
    melhor_solucao = solucao_inicial_dim_cliente
    solucao_inicial_dim_cliente['em_restricao'] = True
    #inicia sistema de flag
    solucao_inicial_dim_cliente['flag_uso'] = np.zeros(len(dados_clientes['demanda']))
    #cria vetor de demanda usadas
    vetor_uso_demanda_insta = calcula_uso_demanda(solucao_inicial_dim_cliente,dados_plantas,dados_clientes)     

    tabu = dict() 
    tabu_s = 0
    
    #busca maior cliente alocado no momento
    ind_maior_cliente_alocado = busca_maior(solucao_inicial_dim_cliente)
            
    #se achar um maior que possa ser movimentado
    while(ind_maior_cliente_alocado >= 0 and intSemMelhoria < maxIntSemMelhorias):        
        (solucao_inicial_dim_cliente, vetor_uso_demanda_insta,tabu) = gera_vizinhos(solucao_inicial_dim_cliente,
                                                                                    dados_plantas,
                                                                                    dados_clientes,
                                                                                    vetor_uso_demanda_insta,
                                                                                    ind_maior_cliente_alocado,
                                                                                    tabu)  
        
        #verifica se houve novos caminhos com indice atual 
        if(len(tabu) > tabu_s):
            tabu_s = len(tabu)
            solucao_inicial_dim_cliente['flag_uso'] = np.zeros(len(dados_clientes['demanda']))
        else:
            solucao_inicial_dim_cliente['flag_uso'][ind_maior_cliente_alocado] = 1        

        #se houve melhorias atualiza melhor estado e zera contador de intervalos sem melhoria
        if(solucao_inicial_dim_cliente['total'] < melhor_solucao['total'] and solucao_inicial_dim_cliente['em_restricao']):            
            melhor_solucao = solucao_inicial_dim_cliente         
            intSemMelhoria = 0             
        else:
            intSemMelhoria += 1 
        
        atualizaTabu(tabu,validade_tabu)
       # print(tabu)


            
        ind_maior_cliente_alocado = busca_maior(solucao_inicial_dim_cliente)  

    return melhor_solucao 

#retorna o indice da instalação ideal para determinado clinte
def gera_vizinhos(solucao_inicial_dim_cliente,dados_plantas,dados_clientes,vetor_uso_demanda,ind_cliente,tabu):

    prim_sol_encontrada_fact = False
    _tabu = tabu
    solucao_temp = solucao_inicial_dim_cliente
    vetor_uso_demanda_temp = vetor_uso_demanda
   #retorna instalação que aloca o maior cliente alocado
    ind_insta_maior_cliente = solucao_inicial_dim_cliente['instalacao'][ind_cliente]

   #percorre o vetor de instalações por cliente fazendo troca entre o cliente iterado e com maior
    for i in range(0,len(solucao_inicial_dim_cliente['instalacao'])):

        copia_solucao = copy.deepcopy(dict(solucao_inicial_dim_cliente))
        
        #Evita gerar o mesmo estado que já esta, chegar em um estado tabu e fazer trocas entre clientes atendidos pela mesma instalação
        if( i != ind_cliente 
            and str(copia_solucao['instalacao']) not in tabu
            and copia_solucao['instalacao'][i] != copia_solucao['instalacao'][ind_cliente] ):           
            
            #gera vizinho 
            copia_tabu = copy.deepcopy(tabu)
            copia_vetor_uso_demanda = copy.deepcopy(vetor_uso_demanda)
            #possivel atualização para o tabu
            copia_tabu[str(copia_solucao['instalacao'])] = 0
            #realiza a troca entre as instalações
            antiga_insta = copia_solucao['instalacao'][ind_cliente]
            copia_vetor_uso_demanda[antiga_insta] -= dados_clientes['demanda'][ind_cliente]

            copia_solucao['instalacao'][ind_cliente] = copia_solucao['instalacao'][i] 
            copia_vetor_uso_demanda[copia_solucao['instalacao'][i]] -= dados_clientes['demanda'][i]
            copia_vetor_uso_demanda[copia_solucao['instalacao'][i]] += dados_clientes['demanda'][ind_cliente]           
            copia_solucao['custo'][ind_cliente] = dados_clientes['custo'][ind_cliente][copia_solucao['instalacao'][ind_cliente]]  
            
            copia_solucao['instalacao'][i] = antiga_insta
            copia_solucao['custo'][i] = dados_clientes['custo'][i][copia_solucao['instalacao'][i]]
            copia_vetor_uso_demanda[antiga_insta] += dados_clientes['demanda'][i]

            #realiza os calculos de restrição e objetivo
            if(avalia_restricao(copia_vetor_uso_demanda,dados_plantas)):
                copia_solucao['total'] = calcula_funcao_objetivo(copia_solucao, dados_plantas)

                #se o vizinho for menor, define como a melhor solucao, ou se o vizinho for o primeiro vizinho válido
                if( (copia_solucao['total'] < solucao_temp['total']) or not prim_sol_encontrada_fact):
                    #atualiza informações do melhor
                    prim_sol_encontrada_fact = True
                    solucao_temp = copia_solucao                
                    vetor_uso_demanda_temp = copia_vetor_uso_demanda
                    _tabu = copia_tabu

    return (solucao_temp, vetor_uso_demanda_temp,_tabu)
