
from config import *
from auxiliares.funcoes_entrada_saida import *
from auxiliares.funcoes_auxiliares import *
from auxiliares.funcoes_auxiliares import _iniSolucao
from auxiliares.funcoes_avaliacao import *
from heuristicas.construtivo_hibrido import *
from heuristicas.construtivo_guloso import *
from heuristicas.construtivo_aleatorio import *
from heuristicas.refinamentos import *
from sol_unica.busca_tabu import *
from sol_populacional.pso import *

if __name__ == '__main__':

    dados_clientes, dados_plantas, solucao = zera_vetores()
    caminho = "../dataset/p3.txt"
   
    print("Lendo Dataset...")
    entrada_dados(dados_clientes,dados_plantas, caminho)

    pso(dados_clientes,dados_plantas,5)



''' print("Iniciando Solucao Inicial..")
    solucao_ini = _iniSolucao(dados_clientes) #inicia o array de solucao.    
    #solucao_ini = solucao_aleatoria(dados_clientes, solucao_ini,dados_plantas)
    instalacoes_removidas = [] #cria um vetor para armazenar as instalações que serão removidas nas particulas, faz isso para que não repetir a instalação fechada
    solucao_gulosa_2_aleatoria(dados_clientes, dados_plantas, solucao_ini, 1, 1, instalacoes_removidas)

    print("Buscando melhor solucao por tabu..")
    solucao_ini = busca_tabu_solucao(solucao_ini,dados_clientes,dados_plantas,max_int_tabu,validade_tabu)    
    print(calcula_funcao_objetivo(solucao_ini,dados_plantas))

    print("Refinando..")
    solucao_ini = refina_sem_abrir(solucao_ini,dados_clientes,dados_plantas,False)    
    print(calcula_funcao_objetivo(solucao_ini,dados_plantas))

    print(cria_vetor_solucao(solucao_ini,dados_plantas))'''


'''

        hora_inicio = time.time()
        criaSolInicial(dados_clientes,dados_plantas,solucao)        
        solucao = busca_tabu_solucao(solucao,dados_clientes,dados_plantas,400,validade_tabu)
        solucao = refina_sem_abrir(solucao,dados_clientes,dados_plantas,False)  
        hora_fim = time.time()

        tempo_execucao = hora_fim - hora_inicio   

        print("Busca tabu:")
        print(solucao['total'])
        print('Tempo de execu��o da estrat�gia refinamento: {}ms'.format(tempo_execucao)) 
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
'''

