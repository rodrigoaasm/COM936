import numpy as np
from config import *

def entrada_dados():
    with open(caminho, 'r') as f:
        data = f.readlines()
        header = data.pop(0)
        n_clientes, n_plantas = header.split()
        n_clientes = int(n_clientes)
        n_plantas = int(n_plantas)
        for i in range(0, n_clientes):
            cliente = data.pop(0)
            dados_clientes['custo'].append(
                [int(float(cli)) for cli in cliente.split()])
            [dados_clientes['posicao'].append(i)]
            [dados_clientes['disponivel'].append(1)]
        n_linhas_array_clientes = int(n_clientes / n_plantas)
        for i in range(0, n_linhas_array_clientes):
            demanda = data.pop(0)
            [dados_clientes['demanda'].append(
                int(float(dem))) for dem in demanda.split()]
        for i in range(0, n_plantas):
            [dados_plantas['posicao'].append(i)]

        dados_plantas['custo'] = [
            int(float(cus)) for cus in data.pop(0).split()]
        dados_plantas['capacidade'] = [
            int(float(cap)) for cap in data.pop(0).split()]


def saida_dados(text, tipo):
    np.savetxt('result_%s.txt' % tipo, text, fmt="%s")
    return

def calcula_cxb():
    dados_plantas['cxb'] = []
    for i in range(0, len(dados_plantas['custo'])):
        dados_plantas['cxb'].append(dados_plantas['capacidade'][i] /
                                  dados_plantas['custo'][i])

def saida_dados_format(result):
    file = open("saidas/result_solucoes","w")
    for i in range(0,len(result)):
        file.write("%d : %s \n" %(i, result[i] ))
    file.close()
    return

def formataSaida(unform_sol):
    listFormat = []
    for i in range(0,len(unform_sol)):
        try:
            listFormat[unform_sol[i]].append(i)
        except:
            listFormat.append([])
            listFormat[unform_sol[i]].append(i)

    return (listFormat)