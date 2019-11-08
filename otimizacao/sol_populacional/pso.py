
from config import *
from random import *
from heuristicas.construtivo_aleatorio import *
from auxiliares.funcoes_avaliacao import *
from auxiliares.funcoes_auxiliares import *
from auxiliares.funcoes_auxiliares import _iniSolucao

#Essa função tem objetivo de inicializar os vetores de dados das particulas
def pso_init(dados_clientes,dados_plantas,numParticulas):

    particulas = []
    melhorPosicionamentoCadaParticula = []
    velocidade = []
    maxRand = len(dados_clientes['demanda'])

    lider = 0
    objetivo_lider = 0
    
    for i in range(numParticulas):
        #cria particula
        particulas.append(_iniSolucao(dados_clientes))
        particulas[i] = solucao_aleatoria(dados_clientes, dados_plantas,particulas[i])
        particulas[i]['uso_demanda'] = calcula_uso_demanda(particulas[i],dados_plantas,dados_clientes)
                 
        #calcula função objetivo e inicia melhor posição
        particulas[i]['total'] = calcula_funcao_objetivo(particulas[i],dados_plantas)
        melhorPosicionamentoCadaParticula.append(copy.deepcopy(particulas[i]))

        velocidade.append([[1,3]])

        if(i == 1):
            objetivo_lider = particulas[i]['total']
        elif(objetivo_lider > particulas[i]['total']):
            lider = i
            objetivo_lider = particulas[i]['total']



    return (particulas,melhorPosicionamentoCadaParticula,lider,velocidade)

#define novas posições das particulas
def defineNovaPosicao(particulas, melhores_posicionamento,velocidades_particulas,numParticulas,dados_clientes,dados_plantas):

    lider = 0
    objetivo_lider = 0
    retricao_lider = True

    for i in range(numParticulas):        
        for tr in velocidades_particulas[i]:         
            #faz a transferencia de instalação            
            particulas[i]['instalacao'][tr[0]] = tr[1]
            particulas[i]['custo'][tr[0]] = dados_clientes['custo'][tr[0]][tr[1]]
            particulas[i]['uso_demanda'] = calcula_uso_demanda(particulas[i],dados_plantas,dados_clientes)

        particulas[i]['total'] = calcula_funcao_objetivo(particulas[i],dados_plantas)
        particulas[i]['restricao'] = avalia_restricao(particulas[i]['uso_demanda'],dados_plantas)

        #Se a posição atual da particula for melhor que a melhor posição registrada, atual posição passa a ser a melhor
        if(melhores_posicionamento[i]['total'] > particulas[i]['total'] and particulas[i]['restricao']):
            melhores_posicionamento[i] = copy.deepcopy(particulas[i])        

        #se for a primeira particula e dada como a melhor
        if(i == 0):
            objetivo_lider = particulas[i]['total']
        elif(objetivo_lider > particulas[i]['total'] 
                and (particulas[i]['restricao'] == particulas[lider]['restricao'] or particulas[i]['restricao'])): # se a melhor particula for mais pesada que atual: a atual passa a ser a melhor
            lider = i
            objetivo_lider = particulas[i]['total']
    return (lider)

def diffPosicoes(vecta,vectb):
    diff = []
    for i in range(len(vecta)):
        if(vecta[i] != vectb[i]):
            diff.append([i,vectb[i]]) 

    return diff

#Metodo principal 
def calculaNovasVelocidade(particulas,melhores_posicionamento,lider,const_soc,const_ind,numParticulas,velocidades_particulas):
    
    for i in range(numParticulas):
        diff_ind = diffPosicoes(particulas[i]['instalacao'],melhores_posicionamento[i]['instalacao'])
        try:
            velocidades_particulas[i] = random.sample(diff_ind,const_ind)     
        except:
            velocidades_particulas[i] = diff_ind

        diff_lid = diffPosicoes(particulas[i]['instalacao'],particulas[lider]['instalacao'])
        try:
            velocidades_particulas[i] += random.sample(diff_lid,const_soc)     
        except:
            velocidades_particulas[i] += diff_lid

    return velocidades_particulas

def melhorPosicao(posicoes):
    indexMelhor = 0
    fitnessMelhor = posicoes[0]['total']
    i = 0

    for pos in posicoes:          
        if(i != 0 and pos['total'] < fitnessMelhor):
            indexMelhor = i
            fitnessMelhor = pos['total']
        i += 1

    return (posicoes[indexMelhor])

#Metodo principal do pso
def pso (dados_clientes,dados_plantas,numParticulas,numCiclos,const_soc,const_ind):

    #instancia dados das particulas
    (particulas, melhores_posicionamento,lider,velocidades_particulas) = pso_init(dados_clientes,dados_plantas,numParticulas)
    #Inicia velocidades das particulas
    velocidades_particulas = calculaNovasVelocidade(particulas,melhores_posicionamento,lider,const_soc,const_ind,numParticulas,velocidades_particulas)

    for i in range(0,numCiclos):                
        lider = defineNovaPosicao(particulas, melhores_posicionamento,velocidades_particulas,numParticulas,dados_clientes,dados_plantas)
        velocidades_particulas = calculaNovasVelocidade(particulas,melhores_posicionamento,lider,2,2,numParticulas,velocidades_particulas)

    return melhorPosicao(melhores_posicionamento)
