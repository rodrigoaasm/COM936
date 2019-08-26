import numpy as np

dados_clientes = {
    'custo': [],
    'demanda': [],
}
dados_plantas = {
    'custo': [],
    'capacidade': []
}


def entrada_dados(inst):
    caminho = "dataset/" + inst + ".txt"
    with open(caminho, 'r') as f:
        data = f.readlines()
        header = data.pop(0)
        n_clientes, n_plantas = header.split()
        n_clientes = int(n_clientes)
        n_plantas = int(n_plantas)
        for i in range(0, n_clientes):
            cliente = data.pop(0)
            dados_clientes['custo'].append([int(float(cli)) for cli in cliente.split()])
        n_linhas_array_clientes = int(n_clientes / n_plantas)
        for i in range(0, n_linhas_array_clientes):
            demanda = data.pop(0)
            [dados_clientes['demanda'].append(int(float(dem))) for dem in demanda.split()]
        dados_plantas['custo'] = [int(float(cus)) for cus in data.pop(0).split()]
        dados_plantas['capacidade'] = [int(float(cap)) for cap in data.pop(0).split()]


def encontra_menor_demanda():
    menor = 0
    for i in range(0, len(dados_clientes['demanda'])):
        if dados_clientes['demanda'][i] < dados_clientes['demanda'][menor]:
            menor = i
    print('Menor demanda - Cliente: %s / Valor: %s'
          % (menor + 1, dados_clientes['demanda'][menor]))


def saida_dados(text, tipo):
    np.savetxt('result_%s.txt' % tipo, text, fmt="%s")
    return


if __name__ == '__main__':
    entrada_dados("p3")
    encontra_menor_demanda()
    saida_dados([dados_clientes], 'clientes')
    saida_dados([dados_plantas], 'plantas')
