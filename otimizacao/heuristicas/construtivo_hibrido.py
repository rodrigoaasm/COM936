import copy
import random

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

def _retira_instalacao_aleatoria(qtd_instalacoes, qtd_instalacoes_removidas, instalacoes_removidas):
    instalacoes_escolhidas = [] #função que seleciona as instalações a ser removida de uma particula de forma aleatória
    while(len(instalacoes_escolhidas) != qtd_instalacoes_removidas):
        insta = random.randint(0, qtd_instalacoes-1)
        if(not instalacoes_removidas.__contains__(insta)):#verifica se a instalação escolhida já foi selecionada anteriormente
            instalacoes_escolhidas.append(insta)
            instalacoes_removidas.append(insta)

    return instalacoes_escolhidas


def solucao_gulosa_2_aleatoria(dados_clientes, dados_plantas, solucao, seed, num_insta, instalacoes_removidas):
    print('----------CONSTRUTIVA HIBRÍDA----------')
    state = 0
    i = 0
    random.seed(seed)
    instalacoes_escolhidas = _retira_instalacao_aleatoria(len(dados_plantas["capacidade"]), num_insta,instalacoes_removidas)

    while(state == 0 ):
        state = solucao_gulosa_2(dados_clientes, dados_plantas, solucao, instalacoes_escolhidas)
        i += 1
        num_insta -= 1#caso a particula não tenha sido viável, tentará cria-la novamente mas com uma instalação a menos
        if (i > 15 or num_insta < 0):
            break

        instalacoes_escolhidas.remove(instalacoes_escolhidas[num_insta])


def solucao_gulosa_2_automatica(dados_clientes, dados_plantas, solucao):
    print('----------SOLUÇÃO GULOSA----------')
    state = 0
    i = 0
    multiplicador = 1

    while(state == 0):
        instalacoes_escolhidas = _gera_solucao_minima(dados_clientes, dados_plantas, multiplicador, -3)
        multiplicador += 0.05
        state = solucao_gulosa_2(dados_clientes, dados_plantas, solucao, instalacoes_escolhidas)
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
def solucao_gulosa_2(dados_clientes, dados_plantas, solucao, plantas_escolhidas):
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
