
from config import *
from random import *
from heuristicas.construtiva import *
from auxiliares.funcoes_avaliacao import *
from auxiliares.funcoes_auxiliares import *
from auxiliares.funcoes_auxiliares import _iniSolucao

#Essa função tem objetivo de inicializar os vetores de dados das particulas
def pso_init(dados_clientes,dados_plantas,numParticulas):

    particulas = []
    melhorPosicionamentoCadaParticula = []
    velocidade = []
    maxRand = len(dados_clientes['demanda'])

    for i in range(numParticulas):
        #cria particula
        particulas.append(_iniSolucao(dados_clientes))
        solucao_aleatoria(dados_clientes,particulas[i], dados_plantas)
                 
        #calcula função objetivo e inicia melhor posição
        particulas[i]['total'] = calcula_funcao_objetivo(particulas[i],dados_plantas)
        melhorPosicionamentoCadaParticula.append(particulas[i])

        #gera velocidade da particula
        velocidade.append(random.sample(range(0,maxRand), 2))

    return (particulas,melhorPosicionamentoCadaParticula,velocidade)

#define novas posições das particulas
def defineNovaPosicao(particulas, melhores_posicionamento,velocidades_particulas,numParticulas,dados_clientes,dados_plantas):

    lider = 0
    objetivo_lider = 0

    for i in range(numParticulas):
        #faz a troca de posições
        temp_ind_insta = particulas[i]['instalacao'][velocidades_particulas[i][0]]

        particulas[i]['instalacao'][velocidades_particulas[i][0]] = particulas[i]['instalacao'][velocidades_particulas[i][1]]        
        particulas[i]['custo'][velocidades_particulas[i][0]] = dados_clientes['custo'][velocidades_particulas[i][0]][particulas[i]['instalacao'][velocidades_particulas[i][1]]]
        #fazer o calculo
        particulas[i]['instalacao'][velocidades_particulas[i][1]] =  temp_ind_insta
        particulas[i]['custo'][velocidades_particulas[i][1]] = dados_clientes['custo'][velocidades_particulas[i][1]][temp_ind_insta]
        #fazer o calculo

        particulas[i]['total'] = calcula_funcao_objetivo(particulas[i],dados_plantas)

        #Se a posição atual da particula for melhor que a melhor posição registrada, atual posição passa a ser a melhor
        if(melhores_posicionamento[i]['total'] > particulas[i]['total']):
            melhores_posicionamento[i] = particulas[i]

        #se for a primeira particula e dada como a melhor
        if(i == 0):
            objetivo_lider = particulas[i]['total']
        elif(objetivo_lider > particulas[i]['total']): # se a melhor particula for mais pesada que atual: a atual passa a ser a melhor
            lider = i
            objetivo_lider = particulas[i]['total']
    return (lider)


#Metodo principal do pso
def pso (dados_clientes,dados_plantas,numParticulas,numCiclos):

    for i in range(0,numCiclos):
        #instancia dados das particulas
        (particulas, melhores_posicionamento,velocidades_particulas) = pso_init(dados_clientes,dados_plantas,numParticulas)
        
        lider = defineNovaPosicao(particulas, melhores_posicionamento,velocidades_particulas,numParticulas,dados_clientes,dados_plantas)

    
    