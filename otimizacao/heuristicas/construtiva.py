from filecmp import cmp

from Tools.demo.sortvisu import quicksort
from config import*
from auxiliares.funcoes_auxiliares import *

def sol_min(dados_clientes, solucao):
    for i in range(0, len(dados_clientes['demanda'])):
        indice = dados_clientes['custo'][i].index(min(dados_clientes['custo'][i]))
        solucao['instalacao'][i] = indice
        solucao['custo'][i] = dados_clientes['custo'][i][indice]
        dados_clientes['disponivel'][i] = 0

def _gera_solucao_minima(dados_clientes, dados_instalacoes, multiplicador, escolha_tipo_ordenacao):
    total_demanda_cliente = sum(dados_clientes['demanda'])
    total_demanda_instalacoes = 0
    copia_instalacoes_ordenadas = copy.deepcopy(dict(dados_instalacoes))
    quickSort(dados_clientes, copia_instalacoes_ordenadas, dados_instalacoes, escolha_tipo_ordenacao, 0, len(dados_instalacoes['capacidade'])-1)#ordena o dicionário pelo valor

    total_demanda_cliente *= multiplicador #Sendo que a demanda pode ser escolhida desde o limite da capacidade até um multiplicador escolhido
    instalacoes_escolhidas = []
    i = 0

    while(total_demanda_instalacoes < total_demanda_cliente and i < len(copia_instalacoes_ordenadas['capacidade'])):#enquanto não obter a quantida desejada irá continuar a "abrir" instalações
        total_demanda_instalacoes += copia_instalacoes_ordenadas['capacidade'][i]
        i += 1

    for j in range(i, len(copia_instalacoes_ordenadas['capacidade'])):
        instalacoes_escolhidas.append(copia_instalacoes_ordenadas['posicao'][j])

    return instalacoes_escolhidas

def _solucao_gulosa_delimitada_demanda(dados_clientes, dados_plantas, solucao):
    state = 0
    i = 0
    multiplicador = 1

    while(state == 0):
        instalacoes_escolhidas = _gera_solucao_minima(dados_clientes, dados_plantas, multiplicador, -3)
        multiplicador += 0.05
        state = _solucao_gulosa_2(dados_clientes, dados_plantas, solucao, instalacoes_escolhidas)
        i += 1
        if(i > 10):
            break

    if(i>15):
        print("Solução não encontrada")

#Se a instalação não couber mais clientes, a remove e adiciona para cada cliente na posição dessa instalação um valor que a torne inviável
def _ajusta_insta_clientes(instalacoes, clientes_plantas, insta, pos_insta_cliente, menor_demanda): 
    if (instalacoes['capacidade'][insta] - menor_demanda < 0):
        del (instalacoes['capacidade'][insta])
        del (instalacoes['posicao'][insta])
        del (instalacoes['custo'][insta])
        for i in range(0, len(clientes_plantas['demanda'])):
            clientes_plantas['custo'][i][pos_insta_cliente] = 100000

#Para as instalações escolhidas para não fazer parte atribui 10.000 como valor de alocação
def _retira_instalacoes(clientes_plantas, plantas_esolhidas):

    for j in range(0, len(plantas_esolhidas)):
            for i in range(0, len(clientes_plantas['demanda'])):
                clientes_plantas['custo'][i][plantas_esolhidas[j]] = 100000

#caso ele chegue num ponto de ter passado por todas as instalações, vai ser necessário recolocar os valores
def _adiciona_instalacoes(copia_dados_clientes, dados_clientes, instalacoes): 

    for j in range(0, len(instalacoes['capacidade'])):
        for i in range(0, len(copia_dados_clientes['demanda'])):
            copia_dados_clientes['custo'][i][instalacoes['posicao'][j]] = dados_clientes['custo'][i][instalacoes['posicao'][j]]

def _atualiza_instalacoes_clientes(clientes_plantas, copia_dados_clientes, dados_clientes, instalacoes, pos_insta_cliente, i):
    copia_dados_clientes['custo'][clientes_plantas['posicao'][i]][
        pos_insta_cliente] = 100000  # Para não considerar a instalação atual, atribui o valor de 10.000 para que ela não entre na conta
    indice = copia_dados_clientes['custo'][clientes_plantas['posicao'][i]].index(
        min(copia_dados_clientes['custo'][clientes_plantas['posicao'][i]]))
    if copia_dados_clientes['custo'][clientes_plantas['posicao'][i]][indice] == 100000:
        _adiciona_instalacoes(copia_dados_clientes, dados_clientes, instalacoes)

    indice = copia_dados_clientes['custo'][clientes_plantas['posicao'][i]].index(
        min(copia_dados_clientes['custo'][clientes_plantas['posicao'][i]]))
    clientes_plantas['custo'][i] = copia_dados_clientes['custo'][clientes_plantas['posicao'][i]][indice]
    clientes_plantas['instalacao'][i] = indice

#Método construtivo guloso versão 2.0
def _solucao_gulosa_2(dados_clientes, dados_plantas, solucao, plantas_escolhidas):
    copia_dados_clientes = copy.deepcopy(dict(dados_clientes))
    instalacoes = copy.deepcopy(dict(dados_plantas))

    for i in range(0, len(plantas_escolhidas)): #remove as instalações que não serão abertas, isso visa reduzir o espaço de busca
        indice = instalacoes['posicao'].index(plantas_escolhidas[i])
        del(instalacoes['posicao'][indice])
        del(instalacoes['custo'][indice])
        del(instalacoes['capacidade'][indice])

    _retira_instalacoes(copia_dados_clientes, plantas_escolhidas)#Para as instalações que foram removidas, substitui o valor delas por 10.000 para que não sejam consideradas

    qtd_clientes = len(copia_dados_clientes['demanda'])
    state = 1
    clientes_plantas = { #Cria um dicionário para facilitar o manuseio
        'instalacao': [],
        'custo': [],
        'posicao': [],
        'demanda': []
    }

    for i in range(0, qtd_clientes):#Preenche o dicionário acima com os dados dos clientes
        indice = copia_dados_clientes['custo'][i].index(min(copia_dados_clientes['custo'][i]))
        clientes_plantas['instalacao'].append(indice)
        clientes_plantas['custo'].append(copia_dados_clientes['custo'][i][indice])
        clientes_plantas['demanda'].append(copia_dados_clientes['demanda'][i])
        clientes_plantas['posicao'].append(i)

    quickSort(copia_dados_clientes, dados_plantas, clientes_plantas, -2, 0, len(clientes_plantas['instalacao'])-1)#ordena o dicionário pelo valor
    i = 0
    j = 0

    while j < qtd_clientes: #Enquanto houver clientes que não foram atendidos, continuará a tentar inseri-los

        pos_insta_cliente = clientes_plantas['instalacao'][i]
        if instalacoes['posicao'].__contains__(pos_insta_cliente):#Se a instalação analisada do cliente, consta no dicionário das instalações disponíveis irá prosseguir
            insta = instalacoes['posicao'].index(pos_insta_cliente)

            if(instalacoes['capacidade'][insta] - clientes_plantas['demanda'][i] >= 0): #Verifica se cabe o cliente na instalação
                instalacoes['capacidade'][insta] -= clientes_plantas['demanda'][i]
                solucao['instalacao'][clientes_plantas['posicao'][i]] = instalacoes['posicao'][insta] #Se couber, insere na solução e atualiza a capacidade das instalações
                solucao['custo'][clientes_plantas['posicao'][i]] = clientes_plantas['custo'][i]

                del(clientes_plantas['posicao'][i])#Visto que esse cliente já foi alocado, o remove
                del(clientes_plantas['instalacao'][i])
                del(clientes_plantas['custo'][i])
                del(clientes_plantas['demanda'][i])
                j += 1
                i -= 1 #visto que se retirou assim volta uma posição para não se perder
            else: #Caso não tenha espaço para ele, irá pegar a segunda instalação de menor custo
                _atualiza_instalacoes_clientes(clientes_plantas, copia_dados_clientes, dados_clientes, instalacoes, pos_insta_cliente, i)

            if(j < qtd_clientes): #Se houver clientes no vetor, irá verificar se a instalação observada tem espaço para mais clientes
                _ajusta_insta_clientes(instalacoes, copia_dados_clientes, insta, pos_insta_cliente, min(clientes_plantas['demanda']))#Se não houver remove a instalação

        else:#Se a instalação observada do cliente não constar em Instalações, repete o procedimento de atualizar a instalação atual
            _atualiza_instalacoes_clientes(clientes_plantas, copia_dados_clientes, dados_clientes, instalacoes, pos_insta_cliente, i)

        if (len(instalacoes['capacidade']) == 0):#Se não houver mais instalações disponíveis, para o laço de repetição
            break

        i += 1 #incrementa o cliente analisado

        if (i == len(clientes_plantas['posicao'])): #se o valor do cliente for o total de clientes disponível, atribui 0 visto que se chegou ao limite de clientes, assim é necessário reiniciar a busca
            i = 0

    if(j != qtd_clientes): #Se houve clientes não alocados, devolverá falso
        state = 0

    return state

#Metodo construtivo guloso
def solucao_gulosa(dados_clientes, dados_plantas, solucao):
    print('----------SOLUÇÃO GULOSA----------')

    instalacao = 0 #ira pegar a instalação da posição inicial
    copia_dados_instalacoes = copy.deepcopy(dict(dados_plantas)) #copia os dicionários para não retorna-los em sua ordem original
    copia_dados_clientes = copy.deepcopy(dict(dados_clientes))

    quickSort(dados_clientes, dados_plantas,solucao, -1, 0, len(dados_plantas['capacidade'])-1) #ordena o instalações pelo custo
    qtd_demanda_insta = dados_plantas['capacidade'][0] #atribui a demanda a qtdDemandaInsta, pois ela sera utilizada para testar se uma instalação tem capacidade para atender determinado cliente
    i = 0 #contador que guardará a quantia de clientes inseridos na solução
    qtd_clientes = len(dados_clientes['demanda']) #recebe a quantia de clientes armazenadas no dictionary

    while i < qtd_clientes: #enquanto todos os clientes não forem inseridos não irá parar
        quickSort(dados_clientes, dados_plantas, solucao, dados_plantas['posicao'][instalacao], 0, qtd_clientes-1) #ordena os clientes em função do custo com relação a instalação analisada

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
def solucao_aleatoria(dados_clientes,solucao, dados_plantas):    
    capacidade_plantas = copy.deepcopy(dados_plantas['capacidade'])
    demanda_clientes = copy.deepcopy(dados_clientes['demanda'])
    clientes_planta = [[] for item in range(0, len(capacidade_plantas))]

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

    return solucao