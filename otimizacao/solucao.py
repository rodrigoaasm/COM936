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
def calcula_funcao_objetivo(solucao):
    valor = 0
    insta = [] #vetor que guardará as instalações já somadas aos custos, para que não se repitam
    for i in range(0, len(solucao['instalacao'])):
        if not insta.__contains__(solucao['instalacao'][i]):#verifica se a instalação já foi atribuida, senao considera seu valor
            valor += dados_plantas['custo'][solucao['instalacao'][i]]  # atribui ao valor, o custo de abertura de cada instalação
            insta.append(solucao['instalacao'][i]) # e a insere no vetor de instalações, para que seu valor não seja contado novamente

        print(' Cliente %d- custo %d - instalacao %d' %(i, dados_clientes['custo'][i][solucao['instalacao'][i]], solucao['instalacao'][i]))
        valor += solucao['custo'][i] #considera o custo de alocacao de cada cliente para cada instalação

    return valor

def criaSolInicial(dados_clientes, dados_plantas, solucao):
    _iniSolucao(solucao) #inicia o array de solucao
    if estrategias:
        for estrat in estrategias:
         #   metodo_construtivo = globals()['_solucao_%s' % estrat]
            hora_inicio = time()
            _solucao_gulosa(dados_clientes, dados_plantas, solucao)
            hora_fim = time()
            tempo_execucao = hora_fim - hora_inicio
            hr, resto = divmod(tempo_execucao, 3600)
            min, seg = divmod(resto, 60)

            print('Tempo de execução da estratégia {}: {}ms'.format(estrat, seg * 1000))
    #else:
     #   _solucao_padrao()


#Função de partição do quicksort
def partition(dados_clientes, dados_plantas, tipo, ini, fim):
    pos = ini
    pivot = getValor(dados_clientes, dados_plantas, tipo, ini) #recebe qual posição sera o pivo

    for i in range(ini+1, fim+1):
        if getValor(dados_clientes, dados_plantas, tipo, i) < pivot:
            pos = pos + 1
            if i != pos:
                trocaValores(dados_clientes, dados_plantas, pos, i, tipo)

    trocaValores(dados_clientes, dados_plantas, pos, ini, tipo)
    return pos #retorna pivo


#Chamada da função quick que permite as subdivisõs
#Tipo simbolizará se quick é para ordenar clientes ou instalações
#caso esteja menor do que 0 será para instalações, e se for maior será para clientes
#Sendo que tipo também fará a função de ser o indice da instalação para ordenar os clientes
def quickSort(dados_clientes, dados_plantas, tipo, ini, fim):
    if ini < fim:
        pi = partition(dados_clientes, dados_plantas, tipo, ini, fim)
        quickSort(dados_clientes, dados_plantas, tipo, ini, pi - 1)
        quickSort(dados_clientes, dados_plantas, tipo, pi + 1, fim)

#Pega um valor expecifico de qualquer dicionario, de forma a ser genérico
def getValor(dados_clientes, dados_plantas, tipo, pos):#tipo terá duas funcionalidades, 1- dizer se é para cliente ou para instalacoes
    if tipo == -1: #caso seja para clientes, ele guardará a posição do cliente que está sendo manipulado
        return dados_plantas['custo'][pos]
    else:
        return dados_clientes['custo'][pos][tipo]

def trocaValores(dados_clientes, dados_plantas, oldPos, newPos, tipo):
    if tipo == -1: #Troca valores do dictionary de plantas, sendo que eles deveram estar em oldPos e newPos
        dados_plantas['custo'][oldPos], dados_plantas['custo'][newPos] = dados_plantas['custo'][newPos], dados_plantas['custo'][oldPos]
        dados_plantas['posicao'][oldPos], dados_plantas['posicao'][newPos] = dados_plantas['posicao'][newPos], dados_plantas['posicao'][oldPos]
        dados_plantas['capacidade'][oldPos], dados_plantas['capacidade'][newPos] = dados_plantas['capacidade'][newPos], dados_plantas['capacidade'][oldPos]
    else: #Troca valores do dictionary de clientes, seguindo o mesmo principio do anterior, mas com a diferença que tipo é a posição da instalação para ordenar os custos dos clientes
        dados_clientes['demanda'][oldPos], dados_clientes['demanda'][newPos] = dados_clientes['demanda'][newPos], dados_clientes['demanda'][oldPos]
        dados_clientes['posicao'][oldPos], dados_clientes['posicao'][newPos] = dados_clientes['posicao'][newPos],dados_clientes['posicao'][oldPos]
        dados_clientes['disponivel'][oldPos], dados_clientes['disponivel'][newPos] = dados_clientes['disponivel'][newPos], dados_clientes['disponivel'][oldPos]
        #print(" Cliente old: %d - custo: %d, Cliente new: %d - custo: %d"%(oldPos, dados_clientes['custo'][oldPos][tipo], newPos,dados_clientes['custo'][newPos][tipo]))
        dados_clientes['custo'][oldPos], dados_clientes['custo'][newPos] = \
            dados_clientes['custo'][newPos], dados_clientes['custo'][oldPos]

#Função que inicia o vetor que conterá a solução
def _iniSolucao(solucao):
    for i in range(0, len(dados_clientes['demanda'])):
        solucao['instalacao'].append(0)
        solucao['custo'].append(0)

def _solucao_gulosa(dados_clientes, dados_plantas, solucao):
    print('----------SOLUÇÃO GULOSA----------')

    instalacao = 0 #ira pegar a instalação da posição inicial
    copia_dados_instalacoes = copy.deepcopy(dict(dados_plantas)) #copia os dicionários para não retorna-los em sua ordem original
    copia_dados_clientes = copy.deepcopy(dict(dados_clientes))

    quickSort(dados_clientes, dados_plantas, -1, 0, len(dados_plantas['capacidade'])-1) #ordena o instalações pelo custo
    qtd_demanda_insta = dados_plantas['capacidade'][0] #atribui a demanda a qtdDemandaInsta, pois ela sera utilizada para testar se uma instalação tem capacidade para atender determinado cliente
    i = 0 #contador que guardará a quantia de clientes inseridos na solução
    qtd_clientes = len(dados_clientes['demanda']) #recebe a quantia de clientes armazenadas no dictionary

    while i < qtd_clientes: #enquanto todos os clientes não forem inseridos não irá parar
        quickSort(dados_clientes, dados_plantas, dados_plantas['posicao'][instalacao], 0, qtd_clientes-1) #ordena os clientes em função do custo com relação a instalação analisada

        clienteAnalisado = 0 #inicia o contador que guardara a posição do cliente analisado
        #Se a instalação não tiver capacidade suficiente para atender o cliente ou o cliente já estiver alocado irá passar para o próximo cliente
        while qtd_demanda_insta < dados_clientes['demanda'][clienteAnalisado] or dados_clientes['disponivel'][clienteAnalisado] == 0:
            clienteAnalisado += 1 #incrementa o cliente e verifica se ele já é igual a quantia de clientes analisados, se sim para o loop
            if clienteAnalisado >= qtd_clientes:
                break

        #Se o id de cliente for menor que a quantia de clientes significa que existe uma pessoa para colocar na instalação analisada
        if clienteAnalisado < qtd_clientes: #Insere na posição real do cliente, a posição real da instalação, diz real pois como os vetores foram ordenados
            solucao['instalacao'][dados_clientes['posicao'][clienteAnalisado]] = dados_plantas['posicao'][instalacao] # Devido a ordenacao seus indices originais seriam perdidos se nao fossem armazenados em posicao
            solucao['custo'][dados_clientes['posicao'][clienteAnalisado]] = dados_clientes['custo'][clienteAnalisado][dados_plantas['posicao'][instalacao]]
            dados_clientes['disponivel'][clienteAnalisado] = 0 #Depois marca que o cliente não está mais disponivel
            qtd_demanda_insta -= dados_clientes['demanda'][clienteAnalisado] #para a variavel que guardava a demanda tem seu valor subtraido pela demanda do cliente
            i += 1 #marca que mais um cliente foi inserido
        else: #caso a instalação não seja capaz de atender mais nenhum cliente
            instalacao += 1 #uma nova instalação deverá ser aberta

            if instalacao == len(dados_plantas['capacidade']):
                instalacao = 0

            qtd_demanda_insta = dados_plantas['capacidade'][instalacao] #quantia das demandas é atualizado pela quantia dessa nova instalação

    dados_clientes['custo'] = copia_dados_clientes['custo'] #retorna os valores a ordem original
    dados_clientes['posicao'] = copia_dados_clientes['posicao']
    dados_clientes['demanda'] = copia_dados_clientes['demanda']

    dados_plantas['capacidade'] = copia_dados_instalacoes['capacidade'] #retorna os valores a ordem original
    dados_plantas['posicao'] = copia_dados_instalacoes['posicao']
    dados_plantas['custo'] = copia_dados_instalacoes['custo']

    return solucao


def _cliente_cabe(clientes_planta, demanda_cliente, capacidade_planta):
    demanda_clientes_planta = [dados_clientes['demanda'][cliente_pos] for
                               cliente_pos in clientes_planta]
    total_planta = sum(demanda_clientes_planta)
    total_c_cliente = total_planta + demanda_cliente
    if total_c_cliente > capacidade_planta:
        return False
    return True

def _solucao_aleatoria(dados_clientes, dados_plantas, solucao):
    print('----------SOLUÇÃO ALEATÓRIA----------')
    capacidade_plantas = copy.deepcopy(dados_plantas['capacidade'])
    demanda_clientes = copy.deepcopy(dados_clientes['demanda'])
    clientes_planta = [[] for item in range(0, len(capacidade_plantas))]
    random.seed('semente3')

    clientes = [pos for pos in range(0, len(demanda_clientes))]
    plantas = [pos for pos in range(0, len(capacidade_plantas))]
    random.shuffle(clientes)
    random.shuffle(plantas)

    for cliente_pos in clientes:
        idx_planta = 0
        planta_pos = plantas[idx_planta]
        while not _cliente_cabe(clientes_planta[planta_pos],
                                demanda_clientes[cliente_pos],
                                capacidade_plantas[planta_pos]
                                ):
            idx_planta += 1
            planta_pos = plantas[idx_planta]
        clientes_planta[planta_pos].append(cliente_pos)

    custo_total = 0
    for planta_pos in range(0, len(clientes_planta)):
        custo_planta = sum([dados_clientes['custo'][i][planta_pos] for i in clientes_planta[planta_pos]])
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

        for cliente in clientes_planta[planta_pos]:
            solucao['instalacao'][cliente] = planta_pos
            solucao['custo'][cliente] = dados_clientes['custo'][cliente][planta_pos]

    print('CUSTO TOTAL ALEATORIO: {}'.format(custo_total))

    return solucao

'''
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
'''
