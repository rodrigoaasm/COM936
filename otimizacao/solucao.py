    qtdDemandaInsta = dados_plantas['capacidade'][0] #atribui a demanda a qtdDemandaInsta, pois ela sera utilizada para testar se uma instalação tem capacidade para atender determinado cliente
    copiaDadosClientes = copy.deepcopy(dict(dados_clientes))
    i = 0 #contador que guardará a quantia de clientes inseridos na solução
    qtdClientes = len(dados_clientes['demanda']) #recebe a quantia de clientes armazenadas no dictionary

    while i < qtdClientes: #enquanto todos os clientes não forem inseridos não irá parar
        quickSort(dados_plantas['posicao'][instalacao], 0, qtdClientes-1) #ordena os clientes em função do custo com relação a instalação analisada

        clienteAnalisado = 0 #inicia o contador que guardara a posição do cliente analisado
        #Se a instalação não tiver capacidade suficiente para atender o cliente ou o cliente já estiver alocado irá passar para o próximo cliente
        while qtdDemandaInsta < dados_clientes['demanda'][clienteAnalisado] or dados_clientes['disponivel'][clienteAnalisado] == 0:
            clienteAnalisado += 1 #incrementa o cliente e verifica se ele já é igual a quantia de clientes analisados, se sim para o loop
            if clienteAnalisado >= qtdClientes:
                break

        #Se o id de cliente for menor que a quantia de clientes significa que existe uma pessoa para colocar na instalação analisada
        if clienteAnalisado < qtdClientes: #Insere na posição real do cliente, a posição real da instalação, diz real pois como os vetores foram ordenados
            solucao['instalacao'][dados_clientes['posicao'][clienteAnalisado]] = dados_plantas['posicao'][instalacao] # Devido a ordenacao seus indices originais seriam perdidos se nao fossem armazenados em posicao
            solucao['custo'][dados_clientes['posicao'][clienteAnalisado]] = dados_clientes['custo'][clienteAnalisado][dados_plantas['posicao'][instalacao]]
            dados_clientes['disponivel'][clienteAnalisado] = 0 #Depois marca que o cliente não está mais disponivel
            qtdDemandaInsta -= dados_clientes['demanda'][clienteAnalisado] #para a variavel que guardava a demanda tem seu valor subtraido pela demanda do cliente
            i += 1 #marca que mais um cliente foi inserido
        else: #caso a instalação não seja capaz de atender mais nenhum cliente
            instalacao += 1 #uma nova instalação deverá ser aberta

            if instalacao == len(dados_plantas['capacidade']):
                instalacao = 0

            qtdDemandaInsta = dados_plantas['capacidade'][instalacao] #quantia das demandas é atualizado pela quantia dessa nova instalação

    dados_clientes['custo'] = copiaDadosClientes['custo']
    dados_clientes['posicao'] = copiaDadosClientes['posicao']
    dados_clientes['demanda'] = copiaDadosClientes['demanda']

    return solucao

'''
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
'''
def otimizaSolucao():
    maior = 0
