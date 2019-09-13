from config import *
import copy
import random
from time import time


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
    insta = [] #vetor que guardará as instalações já somadas aos custos, para que não se repitam
    for i in range(0, len(solucao)):
        posInsta = dados_plantas['posicao'].index(solucao[i])#como o vetor de solucao armazena a posicao original das instalacoes, deve-se buscar sua posicao no array de posicao, visto que a posicao original pode nao ser a atual
        if not insta.__contains__(solucao[i]):#verifica se a instalação já foi atribuida, senao considera seu valor
            valor += dados_plantas['custo'][posInsta]  # atribui ao valor, o custo de abertura de cada instalação
            insta.append(solucao[i]) # e a insere no vetor de instalações, para que seu valor não seja contado novamente

        valor += dados_clientes['custo'][i][solucao[i]] #considera o custo de alocacao de cada cliente para cada instalação
    print("Custo total: %d" %(valor))


def criaSolInicial():
    _iniSolucao()
    if estrategias:
        for estrat in estrategias:
            solucao = globals()['_solucao_%s' % estrat]
            hora_inicio = time()
            solucao()
            hora_fim = time()
            tempo_execucao = hora_fim - hora_inicio
            hr, resto = divmod(tempo_execucao, 3600)
            min, seg = divmod(resto, 60)

            print('Tempo de execução da estratégia {}: {}ms'.format(estrat, seg/1000))
    else:
        _solucao_padrao()


#Função de partição do quicksort
def partition(tipo, ini, fim):
    pos = ini
    pivot = getValor(tipo, ini) #recebe qual posição sera o pivo

    for i in range(ini+1, fim+1):
        if getValor(tipo, i) < pivot:
            pos = pos + 1
            if i != pos:
                trocaValores(pos, i, tipo)

    trocaValores(pos, ini, tipo)
    return pos #retorna pivo


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
    if tipo == -1: #caso seja para clientes, ele guardará a posição do cliente que está sendo manipulado
        return dados_plantas['custo'][pos]
    else:
        return dados_clientes['custo'][pos][tipo]


def trocaValores(oldPos, newPos, tipo):
    if tipo == -1: #Troca valores do dictionary de plantas, sendo que eles deveram estar em oldPos e newPos
        dados_plantas['custo'][oldPos], dados_plantas['custo'][newPos] = dados_plantas['custo'][newPos], dados_plantas['custo'][oldPos]
        dados_plantas['posicao'][oldPos], dados_plantas['posicao'][newPos] = dados_plantas['posicao'][newPos], dados_plantas['posicao'][oldPos]
        dados_plantas['capacidade'][oldPos], dados_plantas['capacidade'][newPos] = dados_plantas['capacidade'][newPos], dados_plantas['capacidade'][oldPos]
    else: #Troca valores do dictionary de clientes, seguindo o mesmo principio do anterior, mas com a diferença que tipo é a posição da instalação para ordenar os custos dos clientes
        dados_clientes['demanda'][oldPos], dados_clientes['demanda'][newPos] = dados_clientes['demanda'][newPos], dados_clientes['demanda'][oldPos]
        dados_clientes['posicao'][oldPos], dados_clientes['posicao'][newPos] = dados_clientes['posicao'][newPos],dados_clientes['posicao'][oldPos]
        dados_clientes['disponivel'][oldPos], dados_clientes['disponivel'][newPos] = dados_clientes['disponivel'][newPos], dados_clientes['disponivel'][oldPos]
        #print(" Cliente old: %d - custo: %d, Cliente new: %d - custo: %d"%(oldPos, dados_clientes['custo'][oldPos][tipo], newPos,dados_clientes['custo'][newPos][tipo]))
        dados_clientes['custo'][oldPos][tipo], dados_clientes['custo'][newPos][tipo] = \
            dados_clientes['custo'][newPos][tipo], dados_clientes['custo'][oldPos][tipo]


#Função que inicia o vetor que conterá a solução
def _iniSolucao():
    for i in range(0, len(dados_clientes['demanda'])):
        solucao.append(0)


def _solucao_gulosa():
    print('----------SOLUÇÃO GULOSA----------')

    instalacao = 0 #ira pegar a instalação da posição inicial
    quickSort(-1, 0, len(dados_plantas['capacidade'])-1) #ordena o instalações pelo custo
    qtdDemandaInsta = dados_plantas['capacidade'][0] #atribui a demanda a qtdDemandaInsta, pois ela sera utilizada para testar se uma instalação tem capacidade para atender determinado cliente
    copiaDadosClientes = copy.deepcopy(dict(dados_clientes))

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
            clienteAnalisado += 1 #incrementa o cliente e verifica se ele já é igual a quantia de clientes analisados, se sim para o loop
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
            qtdDemandaInsta = dados_plantas['capacidade'][instalacao] #quantia das demandas é atualizado pela quantia dessa nova instalação

    dados_clientes['custo'] = copiaDadosClientes['custo']
    dados_clientes['posicao'] = copiaDadosClientes['posicao']
    dados_clientes['demanda'] = copiaDadosClientes['demanda']

    for i in range(0, len(solucao)): #printa a solução obtida
        print(" Clientes: %d - %d"%(i, solucao[i]))

    return solucao


def _cliente_cabe(clientes_planta, demanda_cliente, capacidade_planta):
    demanda_clientes_planta = [dados_clientes['demanda'][cliente_pos] for
                               cliente_pos in clientes_planta]
    total_planta = sum(demanda_clientes_planta)
    total_c_cliente = total_planta + demanda_cliente
    if total_c_cliente > capacidade_planta:
        return False
    return True


def _solucao_aleatoria():
    print('----------SOLUÇÃO ALEATÓRIA----------')
    capacidade_plantas = copy.deepcopy(dados_plantas['capacidade'])
    demanda_clientes = copy.deepcopy(dados_clientes['demanda'])
    clientes_planta = [[] for item in range(0, len(capacidade_plantas))]
    random.seed('semente')

    clientes = [pos for pos in range(0, len(demanda_clientes))]
    plantas = [pos for pos in range(0, len(capacidade_plantas))]
    random.shuffle(clientes)
    random.shuffle(plantas)

    idx_planta = 0
    for cliente_pos in clientes:
        planta_pos = plantas[idx_planta]
        #TODO: Atribuir cliente a planta somente se não exceder a capacidade
        while not _cliente_cabe(clientes_planta[planta_pos],
                                demanda_clientes[cliente_pos],
                                capacidade_plantas[planta_pos]
                                ):
            idx_planta += 1
            planta_pos = plantas[idx_planta]
        clientes_planta[planta_pos].append(cliente_pos)
        custo_total = 0
    for planta_pos in range(0, len(clientes_planta)):
        custo_planta = sum([demanda_clientes[i] for i in clientes_planta[planta_pos]])
        custo_total += custo_planta
        if clientes_planta[planta_pos]:
            custo_total += dados_plantas['custo'][planta_pos]
        print('PLANTA {}: \n   -Capacidade: {}\n   '
              '-Usados: {}\n   -Clientes: {}\n\n'.format(
            planta_pos,
            capacidade_plantas[planta_pos],
            custo_planta,
            clientes_planta[planta_pos])
        )
    print('CUSTO TOTAL ALEATORIO: {}'.format(custo_total))


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
