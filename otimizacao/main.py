import sys

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

    #recebendo parâmetros
    dataset = sys.argv[1]
    inst = sys.argv[2]
    seed = sys.argv[3]
    try:
        num_particulas = int(sys.argv[4])
        max_int_pso = int(sys.argv[5])
    except:
        no_arg = True

    #filtrando datasets
    if dataset == '1':
        caminho = "../dataset/" + inst + ".txt"
    elif dataset == '2':
        caminho = "../datasets/Holmberg_Instances/"+inst
    elif dataset == '3':
        caminho = "../datasets/OR-Library_Instances/"+inst
    elif dataset == '4':
        caminho = "../datasets/Yang_Instances/" + inst + ".dat"

    random.seed(seed)
    #lendo datasets
    dados_clientes, dados_plantas, solucao = zera_vetores()
    entrada_dados(dados_clientes,dados_plantas, caminho)

    #aplica pso > tabu > ref
    hora_inicio = time()
    solucao = pso(dados_clientes,dados_plantas,num_particulas,max_int_pso,1,1)     
    solucao = busca_tabu_solucao(solucao,dados_clientes,dados_plantas,max_int_tabu,validade_tabu) 
    solucao = refina_sem_abrir(solucao,dados_clientes,dados_plantas,False)  
    hora_fim = time()
    tempo_execucao = hora_fim - hora_inicio

    print("{} {} => time: {} s\tfitness: {}".format(inst,seed,tempo_execucao,solucao['total']))
    
    saida_dados_format(solucao,dados_plantas,inst,seed)
            
    
