import traceback as tb
import numpy as np
import time as time
import sys
import config
from datetime import datetime

from config import *
from entrada_saida import *
from funcoes_auxiliares import*
from solucao import*
from construtiva import*
from refinamentos import*
from busca_tabu import *


if __name__ == '__main__':
    for v in range(4, 5):
        validade_tabu = v
        for p in range(1, 58): #para executar para todos os datasets basta colocar 58 no fim do range
            print('------P{}--------------------------------------------'.format(p))

<<<<<<< .mine
    dados_clientes, dados_plantas, solucao = zera_vetores()
    caminho = "../dataset/p3.txt"
   
    entrada_dados(dados_clientes,dados_plantas, caminho)

    solucao = solucao_aleatoria(dados_clientes, solucao,dados_plantas)

    solucao_dim_insta = cria_vetor_solucao(solucao,dados_plantas)

    print(solucao_dim_insta)

    '''
    for p in range(1, 58): #para executar para todos os datasets basta colocar 58 no fim do range
        print('------P{}--------------------------------------------'.format(p))
        dados_clientes, dados_plantas, solucao = zera_vetores()
        caminho = "../dataset/p" + str(p) + ".txt"
   
        entrada_dados(dados_clientes,dados_plantas, caminho)
=======
            dados_clientes, dados_plantas, solucao = zera_vetores()
            caminho = "../dataset/p" + str(p) + ".txt"
















>>>>>>> .theirs

<<<<<<< .mine
        hora_inicio = time.time()
        criaSolInicial(dados_clientes,dados_plantas,solucao)        
        solucao = busca_tabu_solucao(solucao,dados_clientes,dados_plantas,400,validade_tabu)
        solucao = refina_sem_abrir(solucao,dados_clientes,dados_plantas,False)  
        hora_fim = time.time()
=======
            entrada_dados(dados_clientes,dados_plantas, caminho)
            criaSolInicial(dados_clientes,dados_plantas,solucao)
            #solucao = chama_refinamento(solucao,dados_clientes,dados_plantas,False)
            #solucao = cria_vetor_solucao(solucao,dados_plantas)
            #print(calcula_funcao_objetivo(solucao,dados_plantas))
>>>>>>> .theirs

<<<<<<< .mine
        tempo_execucao = hora_fim - hora_inicio   

        print("Busca tabu:")
        print(solucao['total'])
        print('Tempo de execução da estratégia refinamento: {}ms'.format(tempo_execucao)) 
        #saida_dados_format(solucao)
=======
            fobjAnt = calcula_funcao_objetivo(solucao,dados_plantas)





>>>>>>> .theirs

<<<<<<< .mine
        '''

        #try:
        #    criaSolInicial(dados_clientes, dados_plantas, solucao)
        #    solucao = refina_sem_abrir(solucao,dados_clientes,dados_plantas,200,True)
        #except ValueError as e:
        #    print_error()
        #except IndexError as e:
        #    print_error()
        #print('---SOLUCOES---')
        #print('p{} -->  {}'.format(p, solucao))
        #solucao = formataSaida(solucao,dados_plantas)
        #print(solucao)
=======
            tentativas = 0
            hora_inicio = datetime.now()
            while(True):
                inicio_tabu = datetime.now()
                solucao = busca_tabu_solucao(solucao,dados_clientes,dados_plantas,400,validade_tabu)
                fim_tabu = datetime.now()
                tempo_tabu = fim_tabu - inicio_tabu
                print('Tempo Tabu: {}'.format(str(tempo_tabu)))
                saida_dados_excel(p, solucao['total'], 'Tabu', validade_tabu)
                saida_dados_excel(p, str(tempo_tabu), 'Refinamento', validade_tabu)
                solucao = refina_sem_abrir(solucao,dados_clientes,dados_plantas,False)


>>>>>>> .theirs

                if (fobjAnt > solucao['total']) or tentativas == max_tentativas:
                    break
                tentativas += 1

            hora_fim = datetime.now()
            tempo_execucao = hora_fim - hora_inicio
            saida_dados_excel(p, solucao['total'], 'Tabu->Refinamento', validade_tabu)
            saida_dados_excel(p, str(tempo_execucao), 'Tempo', validade_tabu)
            print("Busca tabu: %d" %solucao['total'])

            #saida_dados_format(solucao)

            #try:
            #    criaSolInicial(dados_clientes, dados_plantas, solucao)
            #    solucao = refina_sem_abrir(solucao,dados_clientes,dados_plantas,200,True)
            #except ValueError as e:
            #    print_error()
            #except IndexError as e:
            #    print_error()
            #print('---SOLUCOES---')
            #print('p{} -->  {}'.format(p, solucao))
            #solucao = formataSaida(solucao,dados_plantas)
            #print(solucao)


