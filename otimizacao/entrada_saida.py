
def entrada_dados(dados_clientes, dados_plantas, caminho):
    with open(caminho, 'r') as f:
        data = f.readlines()
        header = data.pop(0)
        n_clientes, n_plantas = header.split()
        n_clientes = int(n_clientes)
        n_plantas = int(n_plantas)
        custo = []

        n_linhas_array_clientes = int(n_clientes / 10)
        n_linhas_array_clientes += 1 if divmod(n_clientes, 10)[1] else 0
        n_linhas_array_plantas = int(n_plantas / 10)
        n_linhas_array_plantas += 1 if divmod(n_plantas, 10)[1] else 0
        for i in range(0, n_clientes):
            for j in range(0, n_linhas_array_plantas):
                cliente = data.pop(0)
                for cli in cliente.split():
                    custo.append(int(float(cli)))
            dados_clientes['custo'].append(custo)
            custo = []

            [dados_clientes['posicao'].append(i)]
            [dados_clientes['disponivel'].append(1)]

        for i in range(0, n_linhas_array_clientes):
            demanda = data.pop(0)
            [dados_clientes['demanda'].append(
                int(float(dem))) for dem in demanda.split()]

        for i in range(0, n_linhas_array_plantas):
            [dados_plantas['custo'].append(
                int(float(cus))) for cus in data.pop(0).split()]
        for i in range(0, n_linhas_array_plantas):
            [dados_plantas['capacidade'].append(
                int(float(cap))) for cap in data.pop(0).split()]

        for i in range(0, n_plantas):
            [dados_plantas['posicao'].append(i)]


def saida_dados(text, tipo):
    np.savetxt('saidas/result_%s.txt' % tipo, text, fmt="%s")
    return


def saida_dados_format(result):
    file = open("saidas/result_solucoes.txt","w")
    for i in range(0,len(result)):
        file.write("%d : %s \n" %(i, result[i] ))
    file.close()
    return