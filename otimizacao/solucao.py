from config import *
from operator import itemgetter
import copy

def encontra_menor_demanda():
    menor = 0
    for i in range(0, len(dados_clientes['demanda'])):
        if dados_clientes['demanda'][i] < dados_clientes['demanda'][menor]:
            menor = i
    print('Menor demanda - Cliente: %s / Valor: %s'
          % (menor + 1, dados_clientes['demanda'][menor]))

#Função que calcula a função objetivo, ou seja, o custo de abertura das instalações mais de alocação de cada cliente
def calcula_funcao_objetivo():
    valor = 0
    insta = []
    for i in range(0, len(solucao)):
        if not insta.__contains__(solucao[i]):#verifica se a instalação já foi atribuida, senao considera seu valor
            valor += dados_plantas['custo'][solucao[i]]  # atribui ao valor, o custo de abertura de cada instalação
            insta.append(solucao[i]) # e a insere no vetor de instalações, para que seu valor não seja contado novamente
        valor += dados_clientes['custo'][i][solucao[i]] #considera o custo de alocacao de cada cliente para cada instalação

    print("Custo total: %d" %(valor))

def criaSolInicial():
    _iniSolucao()
    if estrategia:
        solucao = globals()['_solucao_%s' % estrategia]
        solucao()
    else:
         _solucao_padrao()

#Função de partição do quicksort
def partition(tipo, ini, fim):
    i = (ini - 1)
    pivot = getValor(tipo, fim) #recebe qual posição sera o pivo

    for j in range(ini, fim):
        if getValor(tipo, j) <= pivot:
            i = i + 1
            trocaValores(i, j, tipo)
    trocaValores(i, j, tipo)
    return (i + 1) #retorna pivo

#Chamada da função quick que permite as subdivisõs
#Tipo simbolizará se quick é para ordenar clientes ou instalações
#caso esteja menor do que 0 será para instalações, e se for maior será para clientes
#Sendo que tipo também fará a função de ser o indice da instalação para ordenar os clientes
def quickSort(tipo, ini, fim):
    if ini < fim:
        pi = partition(tipo, ini, fim)
        quickSort(tipo, ini, pi - 1)
        quickSort(tipo, pi + 1, fim)

#Pega um valor expecifico de qualquer dicionario, de forma a ser genérico
def getValor(tipo, pos):#tipo terá duas funcionalidades, 1- dizer se é para cliente ou para instalacoes
    if(tipo == -1):#caso seja para clientes, ele guardará a posição do cliente que está sendo manipulado
        return dados_plantas['custo'][pos]
    else:
        return dados_clientes['custo'][pos][tipo]

def trocaValores(oldPos, newPos, tipo):
    if tipo == -1:#Troca valores do dictionary de plantas, sendo que eles deveram estar em oldPos e newPos
        dados_plantas['custo'][oldPos], dados_plantas['custo'][newPos] = dados_plantas['custo'][newPos], dados_plantas['custo'][oldPos]
        dados_plantas['posicao'][oldPos], dados_plantas['posicao'][newPos] = dados_plantas['posicao'][newPos], dados_plantas['posicao'][oldPos]
        dados_plantas['capacidade'][oldPos], dados_plantas['capacidade'][newPos] = dados_plantas['capacidade'][newPos], dados_plantas['capacidade'][oldPos]
    else: #Troca valores do dictionary de clientes, seguindo o mesmo principio do anterior, mas com a diferença que tipo é a posição da instalação para ordenar os custos dos clientes
        dados_clientes['demanda'][oldPos], dados_clientes['demanda'][newPos] = dados_clientes['demanda'][newPos], dados_clientes['demanda'][oldPos]
        dados_clientes['posicao'][oldPos], dados_clientes['posicao'][newPos] = dados_clientes['posicao'][newPos],dados_clientes['posicao'][oldPos]
        dados_clientes['disponivel'][oldPos], dados_clientes['disponivel'][newPos] = dados_clientes['disponivel'][newPos], dados_clientes['disponivel'][oldPos]
        dados_clientes['custo'][oldPos][tipo], dados_clientes['custo'][newPos][tipo] = dados_clientes['custo'][newPos][tipo], dados_clientes['custo'][oldPos][tipo]

#Função que inicia o vetor que conterá a solução
def _iniSolucao():
    for i in range(0, len(dados_clientes['demanda'])):
        solucao.append(0)

def _solucao_gulosa():
    print ('solucao gulosa')
    instalacao = 0 #ira pegar a instalação da posição inicial
    quickSort(-1, 0, len(dados_plantas['capacidade'])-1) #ordena o instalações pelo custo
    qtdDemandaInsta = dados_plantas['capacidade'][0] #atribui a demanda a qtdDemandaInsta, pois ela sera utilizada para testar se uma instalação tem capacidade para atender determinado cliente

    #for i in range(0, len(dados_plantas['capacidade'])):#apenas demonstra que foi feito a ordenação de forma correta, retirar depois
     #   print(" Instalacao - %d - capacidade %d - custo %d" %(dados_plantas['posicao'][i], dados_plantas['capacidade'][i], dados_plantas['custo'][i]))

    i = 0 #contador que guardará a quantia de clientes inseridos na solução
    qtdClientes = len(dados_clientes['demanda']) #recebe a quantia de clientes armazenadas no dictionary
    while i < qtdClientes: #enquanto todos os clientes não forem inseridos não irá parar
        quickSort(dados_plantas['posicao'][instalacao], 0, qtdClientes-1) #ordena os clientes em função do custo com relação a instalação analisada
        #for k in range(0, qtdClientes):
         #   print(" Instalação: %d - Cliente: %d - Custo: %d - Demanda: %d" %(dados_plantas['posicao'][instalacao], dados_clientes['posicao'][k], dados_clientes['custo'][k][dados_plantas['posicao'][instalacao]], dados_clientes['demanda'][k]))
        clienteAnalisado = 0 #inicia o contador que guardara a posição do cliente analisado
        #Se a instalação não tiver capacidade suficiente para atender o cliente ou o cliente já estiver alocado irá passar para o próximo cliente
        while qtdDemandaInsta < dados_clientes['demanda'][clienteAnalisado] or dados_clientes['disponivel'][clienteAnalisado] == 0:
            clienteAnalisado += 1#incrementa o cliente e verifica se ele já é igual a quantia de clientes analisados, se sim para o loop
            if clienteAnalisado >= qtdClientes:
                break

        #Se o id de cliente for menor que a quantia de clientes significa que existe uma pessoa para colocar na instalação analisada
        if clienteAnalisado < qtdClientes: #Insere na posição real do cliente, a posição real da instalação, diz real pois como os vetores foram ordenados
            solucao[dados_clientes['posicao'][clienteAnalisado]] = dados_plantas['posicao'][instalacao] # Devido a ordenacao seus indices originais seriam perdidos se nao fossem armazenados em posicao
            dados_clientes['disponivel'][clienteAnalisado] = 0 #Depois marca que o cliente não está mais disponivel
            qtdDemandaInsta -= dados_clientes['demanda'][clienteAnalisado] #para a variavel que guardava a demanda tem seu valor subtraido pela demanda do cliente
            i += 1 #marca que mais um cliente foi inserido
        else: #caso a instalação não seja capaz de atender mais nenhum cliente
            instalacao += 1 #uma nova instalação deverá ser aberta
            qtdDemandaInsta = dados_plantas['capacidade'][dados_plantas['posicao'][instalacao]] #quantia das demandas é atualizado pela quantia dessa nova instalação

    print(" qtd %d" %len(dados_clientes['demanda'])) #printa a solução, retirar depois
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