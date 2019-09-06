from config import *
import operator
import copy

def encontra_menor_demanda():
    menor = 0
    for i in range(0, len(dados_clientes['demanda'])):
        if dados_clientes['demanda'][i] < dados_clientes['demanda'][menor]:
            menor = i
    print('Menor demanda - Cliente: %s / Valor: %s'
          % (menor + 1, dados_clientes['demanda'][menor]))

def calcula_funcao_objetivo():
    valor = 0
    for i in range(0, len(solucao)):
        valor += dados_plantas['custo'][solucao[i]]
        valor += dados_clientes['custo'][i][solucao[i]]

    print("Custo: %d" %(valor))

def criaSolInicial():
    _iniSolucao()
    if estrategia:
        solucao = globals()['_solucao_%s' % estrategia]
        solucao()
    else:
         _solucao_padrao()


def _ordenaPlantas():
    sorted_x = dados_plantas
    # cliente = dados_clientes['custo'][instalacao].index(min(dados_clientes['custo'][instalacao]))

def _iniSolucao():
    for i in range(0, len(dados_clientes['demanda'])):
        solucao.append(0)

def _solucao_gulosa():
    print ('solucao gulosa')
    #ordenar Plantas
    instalacao = 0
    qtdDemandaInsta = dados_plantas['capacidade'][0]

    i = 0
    qtd = len(dados_clientes['demanda'])
    while i < qtd:
        #clientes.sort(key =lambda x:x['custo']['instalacao'], reverse=True)
        #ordenar Clientes
        j = 0
        while qtdDemandaInsta < dados_clientes['demanda'][j] or dados_clientes['disponivel'][j] == 0:
            j += 1
            if j >= qtd:
                break

        if j < qtd:
            solucao[dados_clientes['posicao'][j]] = instalacao
            dados_clientes['disponivel'][j] = 0
            qtdDemandaInsta -= dados_clientes['demanda'][j]
            i += 1
        else:
            instalacao += 1
            qtdDemandaInsta = dados_plantas['capacidade'][instalacao]

    print(" qtd %d" %len(dados_clientes['demanda']))
    for i in range(0, len(solucao)):
        print(" Clientes: %d - %d"%(i, solucao[i]))

    return solucao


def _solucao_aleatoria():
    print('solucao aleatoria')
    raise NotImplemented()

def _solucao_hibrida():
    print('solucao hibrida')
    raise NotImplemented()

def _solucao_padrao():
    insta = 0
    qtdDemandaInsta = dados_plantas['capacidade'][0]
    for i in range(0, len(dados_clientes['demanda'])):
        if qtdDemandaInsta >= dados_clientes['demanda'][i]:
            qtdDemandaInsta -= dados_clientes['demanda'][i]
            solucao.append(insta)
        else:
            insta += 1
            qtdDemandaInsta = dados_plantas['capacidade'][insta] - \
                              dados_clientes['demanda'][i]
            solucao.append(insta)

    for i in range(0, len(dados_clientes['demanda'])):
        print("Cliente %d" % (solucao[i]))

def otimizaSolucao():
    maior = 0

1