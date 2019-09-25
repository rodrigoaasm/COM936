import sys
import traceback

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



def calcula_cxb(dados_plantas):
    dados_plantas['cxb'] = []
    for i in range(0, len(dados_plantas['custo'])):
        dados_plantas['cxb'].append(dados_plantas['capacidade'][i] /
                                  dados_plantas['custo'][i])

def cria_vetor_solucao(unform_sol,dados_plantas):
    listFormat =[ [] for i in range(0,len(dados_plantas['custo'])) ]
    
    for i in range(0,len(unform_sol['instalacao'])):
        listFormat[unform_sol['instalacao'][i]].append(i)
    return (listFormat)


def compara_vetor(a,b):
    try:
        for i in range(0,len(a)):            
            if(sum(a[i])!= sum(b[i])):
                return False
        return True
    except:
        return False


def zera_vetores():
    dados_clientes = {
        'custo': [],
        'demanda': [],
        'disponivel': [],
        'posicao': []
    }

    dados_plantas = {
        'custo': [],
        'capacidade': [],
        'posicao': [],
    }

    solucao = {
        'instalacao': [],
        'custo': [],
        'flag_uso': [],
        'em_restricao': bool,
        'total': int
    }

    return dados_clientes, dados_plantas, solucao

def print_error():
    traceback_template = '''Traceback (most recent call last):
      File "%(filename)s", line %(lineno)s, in %(name)s
    %(type)s: %(message)s\n'''

    exc_type, exc_value, exc_traceback = sys.exc_info()  # most recent (if any) by default

    traceback_details = {
        'filename': exc_traceback.tb_frame.f_code.co_filename,
        'lineno': exc_traceback.tb_lineno,
        'name': exc_traceback.tb_frame.f_code.co_name,
        'type': exc_type.__name__,
        'message': exc_value,  # or see traceback._some_str()
    }

    del (exc_type, exc_value, exc_traceback)

    print(traceback.format_exc())
    print(traceback_template % traceback_details)

