import sys
import traceback
import re
import numpy as np
from config import * 

#chama e faz a medida da função construtiva definida no config.py
def criaSolInicial(dados_clientes, dados_plantas, solucao):
    _iniSolucao(solucao, dados_clientes) #inicia o array de solucao
    if estrategias:
        for estrat in estrategias:
            metodo_construtivo = globals()['_solucao_%s' % estrat]
            hora_inicio = time()
            metodo_construtivo(dados_clientes, dados_plantas, solucao)
            hora_fim = time()
            tempo_execucao = hora_fim - hora_inicio
            print('Tempo de execução da estratégia {}: {} ms'.format(estrat, tempo_execucao))

            #vet = [] #esolhendo na mão as instalações
            #vet.append(3)
            #vet.append(1)
            #state = _solucao_gulosa_2(dados_clientes, dados_plantas, solucao, vet)
            #if state == 1:
             #   print("foi")
            #else :
             #   print("nao foi")
            #_solucao_gulosa_delimitada_demanda(dados_clientes, dados_plantas, solucao)

            #for i in range(0, len(solucao['instalacao'])):
             #   print(" Cliente: %d - Insta: %d - Custo: %d" % (i, solucao['instalacao'][i], solucao['custo'][i]))

            print("Valor: %d "%calcula_funcao_objetivo(solucao, dados_plantas))

#Função que inicia o vetor que conterá a solução
def _iniSolucao( dados_clientes):
    solucao = {
        'instalacao': [],
        'custo': [],
        'total' : int,
        'uso_demanda' : []
    }
    
    for i in range(0, len(dados_clientes['demanda'])):
        solucao['instalacao'].append(0)
        solucao['custo'].append(0)
    return solucao

#Pega um valor expecifico de qualquer dicionario, de forma a ser genérico
def getValor(dados_clientes, dados_plantas, solucao, tipo, pos):#tipo terá duas funcionalidades, 1- dizer se é para cliente ou para instalacoes
    if tipo == -1: #caso seja para clientes, ele guardará a posição do cliente que está sendo manipulado
        return dados_plantas['custo'][pos]
    elif tipo == -2:
        return solucao['custo'][pos]
    elif tipo == -3:
        return dados_plantas['capacidade'][pos]/dados_plantas['custo'][pos]
    else:
        return dados_clientes['custo'][pos][tipo]


def trocaValores(dados_clientes, dados_plantas, solucao, oldPos, newPos, tipo):
    if tipo == -1 or tipo == -3: #Troca valores do dictionary de plantas, sendo que eles deveram estar em oldPos e newPos
        dados_plantas['custo'][oldPos], dados_plantas['custo'][newPos] = dados_plantas['custo'][newPos], dados_plantas['custo'][oldPos]
        dados_plantas['posicao'][oldPos], dados_plantas['posicao'][newPos] = dados_plantas['posicao'][newPos], dados_plantas['posicao'][oldPos]
        dados_plantas['capacidade'][oldPos], dados_plantas['capacidade'][newPos] = dados_plantas['capacidade'][newPos], dados_plantas['capacidade'][oldPos]
    elif tipo == -2: #Troca valores do dictionary de clientes, seguindo o mesmo principio do anterior, mas com a diferença que tipo é a posição da instalação para ordenar os custos dos clientes
        solucao['custo'][oldPos], solucao['custo'][newPos] = solucao['custo'][newPos], solucao['custo'][oldPos]
        solucao['instalacao'][oldPos], solucao['instalacao'][newPos] = solucao['instalacao'][newPos], solucao['instalacao'][oldPos]
        solucao['posicao'][oldPos], solucao['posicao'][newPos] = solucao['posicao'][newPos], solucao['posicao'][oldPos]
        solucao['demanda'][oldPos], solucao['demanda'][newPos] = solucao['demanda'][newPos], solucao['demanda'][oldPos]
    else:
        dados_clientes['demanda'][oldPos], dados_clientes['demanda'][newPos] = dados_clientes['demanda'][newPos], dados_clientes['demanda'][oldPos]
        dados_clientes['posicao'][oldPos], dados_clientes['posicao'][newPos] = dados_clientes['posicao'][newPos],dados_clientes['posicao'][oldPos]
        dados_clientes['disponivel'][oldPos], dados_clientes['disponivel'][newPos] = dados_clientes['disponivel'][newPos], dados_clientes['disponivel'][oldPos]
        #print(" Cliente old: %d - custo: %d, Cliente new: %d - custo: %d"%(oldPos, dados_clientes['custo'][oldPos][tipo], newPos,dados_clientes['custo'][newPos][tipo]))
        dados_clientes['custo'][oldPos], dados_clientes['custo'][newPos] = \
            dados_clientes['custo'][newPos], dados_clientes['custo'][oldPos]

#Função de partição do quicksort
def partition(dados_clientes, dados_plantas, solucao, tipo, ini, fim):
    pos = ini
    pivot = getValor(dados_clientes, dados_plantas, solucao, tipo, ini) #recebe qual posição sera o pivo

    for i in range(ini+1, fim+1):
        if(tipo == -3):
            if getValor(dados_clientes, dados_plantas, solucao, tipo, i) > pivot:
                pos = pos + 1
                if i != pos:
                    trocaValores(dados_clientes, dados_plantas, solucao, pos, i, tipo)
        else:
            if getValor(dados_clientes, dados_plantas, solucao, tipo, i) < pivot:
                pos = pos + 1
                if i != pos:
                    trocaValores(dados_clientes, dados_plantas, solucao, pos, i, tipo)

    trocaValores(dados_clientes, dados_plantas, solucao, pos, ini, tipo)
    return pos #retorna pivo


#Chamada da função quick que permite as subdivisões
#Tipo simbolizará se quick é para ordenar clientes ou instalações
#caso esteja menor do que 0 será para instalações, e se for maior será para clientes
#Sendo que tipo também fará a função de ser o indice da instalação para ordenar os clientes
def quickSort(dados_clientes, dados_plantas, solucao, tipo, ini, fim):
    if ini < fim:
        pi = partition(dados_clientes, dados_plantas, solucao, tipo, ini, fim)
        quickSort(dados_clientes, dados_plantas, solucao, tipo, ini, pi - 1)
        quickSort(dados_clientes, dados_plantas, solucao, tipo, pi + 1, fim)



def calcula_cxb(dados_plantas):
    dados_plantas['cxb'] = []
    for i in range(0, len(dados_plantas['custo'])):
        dados_plantas['cxb'].append(dados_plantas['capacidade'][i] /
                                  dados_plantas['custo'][i])

def formata_solucao(unform_sol,dados_plantas):
    listFormat =[ [] for i in range(0,len(dados_plantas['custo'])) ]
    
    for i in range(0,len(unform_sol['instalacao'])):
        listFormat[unform_sol['instalacao'][i]].append(i)
    return (listFormat)


def compara_vetor(a,b):
    try:
        for i in range(0,len(a)):            
            if(sum(a[i])!= sum(b[i])):
                return False
        return True
    except:
        return False

def compara_diff_solucoes(solucaoA,solucaoB):
    tam = len(solucaoA)
    diff = np.zeros(tam)
    for i in range(0,tam):
        diff[i] =  (solucaoA['aberta'][i] and not solucaoB['aberta'][i] ) or (not solucaoA['aberta'][i]  and solucaoB['aberta'][i])
    return diff

def zera_vetores():
    dados_clientes = {
        'custo': [],
        'demanda': [],
        'disponivel': [],
        'posicao': []
    }

    dados_plantas = {
        'custo': [],
        'capacidade': [],
        'posicao': [],
    }

    solucao = {
        'instalacao': [],
        'custo': [],
        'flag_uso': [],
        'em_restricao': bool,
        'total': int
    }

    return dados_clientes, dados_plantas, solucao

def print_error():
    traceback_template = '''Traceback (most recent call last):
      File "%(filename)s", line %(lineno)s, in %(name)s
    %(type)s: %(message)s\n'''

    exc_type, exc_value, exc_traceback = sys.exc_info()  # most recent (if any) by default

    traceback_details = {
        'filename': exc_traceback.tb_frame.f_code.co_filename,
        'lineno': exc_traceback.tb_lineno,
        'name': exc_traceback.tb_frame.f_code.co_name,
        'type': exc_type.__name__,
        'message': exc_value,  # or see traceback._some_str()
    }

    del (exc_type, exc_value, exc_traceback)

    print(traceback.format_exc())
    print(traceback_template % traceback_details)

def _formata_linha(linha):
    linha = re.sub('\.', '', linha)
    return linha.split()

