from config import *
from refinamentos import*
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
def calcula_funcao_objetivo(solucao, dados_plantas):
    valor = 0
    insta = [] #vetor que guardará as instalações já somadas aos custos, para que não se repitam
    for i in range(0, len(solucao['instalacao'])):
        if not insta.__contains__(solucao['instalacao'][i]):#verifica se a instalação já foi atribuida, senao considera seu valor
            valor += dados_plantas['custo'][solucao['instalacao'][i]]  # atribui ao valor, o custo de abertura de cada instalação
            insta.append(solucao['instalacao'][i]) # e a insere no vetor de instalações, para que seu valor não seja contado novamente 
        valor += abs(solucao['custo'][i]) #considera o custo de alocacao de cada cliente para cada instalação

    return valor

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

def sol_min(dados_clientes, solucao):
    for i in range(0, len(dados_clientes['demanda'])):
        indice = dados_clientes['custo'][i].index(min(dados_clientes['custo'][i]))
        solucao['instalacao'][i] = indice
        solucao['custo'][i] = dados_clientes['custo'][i][indice]
        dados_clientes['disponivel'][i] = 0

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
def _iniSolucao(solucao, dados_clientes):
    for i in range(0, len(dados_clientes['demanda'])):
        solucao['instalacao'].append(0)
        solucao['custo'].append(0)

#Metodo construtivo guloso
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


def _cliente_cabe(demanda_cliente, capacidade_planta, utilizado_plantas, planta_pos):

    total_c_cliente = utilizado_plantas[planta_pos] + demanda_cliente

    if total_c_cliente > capacidade_planta:
        return False

    utilizado_plantas[planta_pos] += demanda_cliente
    return True

#metodo construtivo aleatório
def _solucao_aleatoria(dados_clientes, dados_plantas, solucao):
    capacidade_plantas = copy.deepcopy(dados_plantas['capacidade'])
    demanda_clientes = copy.deepcopy(dados_clientes['demanda'])
    clientes_planta = [[] for item in range(0, len(capacidade_plantas))]
    random.seed('semente3')

    clientes = [pos for pos in range(0, len(demanda_clientes))]
    plantas = [pos for pos in range(0, len(capacidade_plantas))]
    utilizado_plantas = [0 for pos in range(0, len(capacidade_plantas))]
    random.shuffle(clientes)
    random.shuffle(plantas)

    for cliente_pos in clientes:
        idx_planta = 0
        planta_pos = plantas[idx_planta]
        while not _cliente_cabe(demanda_clientes[cliente_pos],
                                capacidade_plantas[planta_pos],
                                utilizado_plantas,
                                planta_pos):
            idx_planta += 1
            planta_pos = plantas[idx_planta]
        clientes_planta[planta_pos].append(cliente_pos)

    custo_total = 0
    for planta_pos in range(0, len(clientes_planta)):
        custo_planta = sum([dados_clientes['custo'][i][planta_pos] for i in clientes_planta[planta_pos]])
        custo_total += custo_planta
        if clientes_planta[planta_pos]:
            custo_total += dados_plantas['custo'][planta_pos]

        for cliente in clientes_planta[planta_pos]:
            solucao['instalacao'][cliente] = planta_pos
            solucao['custo'][cliente] = dados_clientes['custo'][cliente][planta_pos]

    print('CUSTO TOTAL ALEATORIO: {}'.format(custo_total))

    return solucao

def avalia_restricao(vetor_demandas_atendidas,dados_plantas):
   ret = True
   for i in range(0,len(vetor_demandas_atendidas)):
      if(dados_plantas['capacidade'][i] < vetor_demandas_atendidas[i]):
         ret = False
   return ret

def busca_maior(solucao_inicial):
   ind_maior = -1
   maior_valor = -1
   for i in range(0,len(solucao_inicial['instalacao'])):
      if(solucao_inicial['custo'][i] > maior_valor):  #and solucao_inicial['flag_uso'][i] != 1):
         ind_maior = i
         maior_valor = solucao_inicial['custo'][i]
   return ind_maior  
    
def busca_tabu_solucao(solucao_inicial_dim_cliente,dados_clientes,dados_plantas):  

    #calcula função objetivo 
    solucao_inicial_dim_cliente['total'] = calcula_funcao_objetivo(solucao_inicial_dim_cliente, dados_plantas)
    #guarda solucao inicial como a melhor 
    melhor_solucao = solucao_inicial_dim_cliente
    solucao_inicial_dim_cliente['em_restricao'] = True
    #cria vetor de demanda usadas
    vetor_uso_demanda_insta = calcula_uso_demanda(solucao_inicial_dim_cliente,dados_plantas,dados_clientes)  
    tabu = dict() 
    
    #busca maior cliente alocado no momento
    ind_maior_cliente_alocado = busca_maior(solucao_inicial_dim_cliente)
            
    #se achar um maior que possa ser movimentado
    if(ind_maior_cliente_alocado >= 0):
        
        (solucao_inicial_dim_cliente, vetor_uso_demanda_insta,tabu) = gera_vizinhos(solucao_inicial_dim_cliente,
                                                                                    dados_plantas,
                                                                                    dados_clientes,
                                                                                    vetor_uso_demanda_insta,
                                                                                    ind_maior_cliente_alocado,
                                                                                    tabu)  
        print(tabu)
        print(solucao_inicial_dim_cliente['total'])

        if(solucao_inicial_dim_cliente['total'] < melhor_solucao['total'] and solucao_inicial_dim_cliente['em_restricao']):            
            melhor_solucao = solucao_inicial_dim_cliente                                                 

    return melhor_solucao 

#retorna o indice da instalação ideal para determinado clinte
def gera_vizinhos(solucao_inicial_dim_cliente,dados_plantas,dados_clientes,vetor_uso_demanda,ind_cliente,tabu):

    _tabu = tabu
    solucao_temp = solucao_inicial_dim_cliente
    vetor_uso_demanda_temp = vetor_uso_demanda
   #retorna instalação que aloca o maior cliente alocado
    ind_insta_maior_cliente = solucao_inicial_dim_cliente['instalacao'][ind_cliente]

   #percorre o vetor de instalações por cliente fazendo troca entre o cliente iterado e com maior
    for i in range(0,len(solucao_inicial_dim_cliente['instalacao'])):

        copia_solucao = copy.deepcopy(dict(solucao_inicial_dim_cliente))
        
        #Evita gerar o mesmo estado que já esta, chegar em um estado tabu e fazer trocas entre clientes atendidos pela mesma instalação
        if( i != ind_cliente 
            and (str(ind_cliente) + "(" + str(copia_solucao['instalacao'][i]) + ")-" + str(i) + "(" + str(copia_solucao['instalacao'][ind_cliente]) + ")") not in tabu
            and copia_solucao['instalacao'][i] != copia_solucao['instalacao'][ind_cliente] ):           
            
            #gera vizinho 
            copia_tabu = copy.deepcopy(tabu)
            copia_vetor_uso_demanda = copy.deepcopy(vetor_uso_demanda)
            #possivel atualização para o tabu       
            copia_tabu[ str(ind_cliente) + "(" + str(copia_solucao['instalacao'][i]) + ")-" + str(i) + "(" + str(copia_solucao['instalacao'][ind_cliente]) + ")"] = 1
            print(str(ind_cliente) + "(" + str(copia_solucao['instalacao'][i]) + ")-" + str(i) + "(" + str(copia_solucao['instalacao'][ind_cliente]) + ")")
            #realiza a troca entre as instalações
            antiga_insta = copia_solucao['instalacao'][ind_cliente]
            copia_vetor_uso_demanda[antiga_insta] -= dados_clientes['demanda'][ind_cliente]

            copia_solucao['instalacao'][ind_cliente] = copia_solucao['instalacao'][i] 
            copia_vetor_uso_demanda[copia_solucao['instalacao'][i]] -= dados_clientes['demanda'][i]
            copia_vetor_uso_demanda[copia_solucao['instalacao'][i]] += dados_clientes['demanda'][ind_cliente]           
            copia_solucao['custo'][ind_cliente] = dados_clientes['custo'][ind_cliente][copia_solucao['instalacao'][ind_cliente]]  
            
            copia_solucao['instalacao'][i] = antiga_insta
            copia_solucao['custo'][i] = dados_clientes['custo'][i][copia_solucao['instalacao'][i]]
            copia_vetor_uso_demanda[antiga_insta] += dados_clientes['demanda'][i]

            #realiza os calculos de restrição e objetivo
            copia_solucao['em_restricao'] = avalia_restricao(copia_vetor_uso_demanda,dados_plantas)
            copia_solucao['total'] = calcula_funcao_objetivo(copia_solucao, dados_plantas)

            print(copia_solucao['instalacao'])
            print(copia_solucao['total'])
            print(copia_solucao['em_restricao'])
            print('---------------------------')

            #Escolhe como a melhor solucao, se o vizinho for o menor e as duas não tiverem tag de restricao ou as duas tiverem
            if( (copia_solucao['total'] < solucao_temp['total']  and copia_solucao['em_restricao'] == solucao_temp['em_restricao'])
                    or ( copia_solucao['total'] and not(solucao_temp['total'])) or solucao_temp == None ):
                #atualiza informações do melhor
                solucao_temp = copia_solucao
                vetor_uso_demanda_temp = copia_vetor_uso_demanda
                _tabu = copia_tabu

    return (solucao_temp, copia_vetor_uso_demanda,_tabu)
