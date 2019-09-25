from config import*
from funcoes_auxiliares import*


def sol_min(dados_clientes, solucao):
    for i in range(0, len(dados_clientes['demanda'])):
        indice = dados_clientes['custo'][i].index(min(dados_clientes['custo'][i]))
        solucao['instalacao'][i] = indice
        solucao['custo'][i] = dados_clientes['custo'][i][indice]
        dados_clientes['disponivel'][i] = 0


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