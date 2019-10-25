import copy

# from filecmp import cmp

from config import*
from auxiliares.funcoes_auxiliares import *

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
