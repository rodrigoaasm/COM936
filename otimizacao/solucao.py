from config import *


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
    if estrategia:
        solucao = globals()['_solucao_%s' % estrategia]
        solucao()
    else:
        _solucao_padrao()

def _solucao_gulosa():
    print ('solucao gulosa')
    raise NotImplemented()

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

