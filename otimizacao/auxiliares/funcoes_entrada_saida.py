from auxiliares.funcoes_auxiliares import formata_solucao, _formata_linha

def entrada_dados(dados_clientes, dados_plantas, caminho):
    with open(caminho, 'r') as f:
        data = f.readlines()
        header = data.pop(0)
        header_1, header_2 = header.split()

        if float(header_1) > float(header_2):
            le_formato_1(
                dados_clientes, dados_plantas, data, header_1, header_2)
        else:
            test_data = [i.split() for i in data]
            if len(test_data[-1]) <= 1:
                test_data.pop(-1)
            if len(test_data[-1]) == 10:
                le_formato_2(
                    dados_clientes, dados_plantas, data, header_1, header_2)
            else:
                le_formato_3(
                    dados_clientes, dados_plantas, data, header_1, header_2)

        # print('DADOS CLIENTE (posicao): ', dados_clientes['posicao'])
        # print('DADOS PLANTA (posicao): ', dados_plantas['posicao'])


def le_formato_1(dados_clientes, dados_plantas, data, header_1, header_2):
    custo = []
    n_clientes = int(header_1)
    n_plantas = int(header_2)
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


def le_formato_2(dados_clientes, dados_plantas, data, header_1, header_2):
    n_clientes = int(header_2)
    n_plantas = int(header_1)
    custo = []
    for i in range(0, n_plantas):
        planta = data.pop(0)
        capacidade, custo = planta.split()
        dados_plantas['capacidade'].append(float(capacidade))
        dados_plantas['custo'].append(float(custo))
        dados_plantas['posicao'].append(i)

    n_linhas_array_clientes = int(n_clientes / 10)
    n_linhas_array_clientes += 1 if divmod(n_clientes, 10)[1] else 0

    n_linhas_array_plantas = int(n_plantas / 10)
    n_linhas_array_plantas += 1 if divmod(n_plantas, 10)[1] else 0

    custo_clientes = [[False for plan in range(0, n_plantas)] for
                      cli in range(0, n_clientes)]

    for linha in range(0, n_linhas_array_clientes):
        demanda_clientes = data.pop(0)
        demanda_clientes = _formata_linha(demanda_clientes)
        for i in range(0, len(demanda_clientes)):
            dados_clientes['demanda'].append(float(demanda_clientes[i]))
            dados_clientes['posicao'].append(linha * 10 + i)
            dados_clientes['disponivel'].append(1)

    for i in range(0, n_plantas):
        for j in range(0, n_linhas_array_clientes):
            cliente = data.pop(0)
            cliente = _formata_linha(cliente)
            for pos, planta in enumerate(cliente, 10 * j):
                custo_clientes[pos][i] = float(planta)

    dados_clientes['custo'] = custo_clientes
    


def le_formato_3(dados_clientes, dados_plantas, data, header_1, header_2):
    n_clientes = int(header_2)
    n_plantas = int(header_1)
    custo = []
    for i in range(0, n_plantas):
        planta = data.pop(0)
        capacidade, custo = planta.split()
        dados_plantas['capacidade'].append(float(capacidade))
        dados_plantas['custo'].append(float(custo))
        dados_plantas['posicao'].append(i)

    demanda_clientes = data.pop(0)

    demanda_clientes = demanda_clientes.split()
    for i in range(0, len(demanda_clientes)):
        dados_clientes['demanda'].append(float(demanda_clientes[i]))

    custo_clientes = [[False for plan in range(0,n_plantas)] for
                      cli in range(0,n_clientes)]

    for i in range(0, n_plantas):
        cliente = data.pop(0)
        cliente = cliente.split()
        for j in range(0, n_clientes):
            custo_clientes[j][i] = float(cliente[j])

    dados_clientes['custo'] = custo_clientes

    for i in range(0, n_clientes):
        dados_clientes['disponivel'].append(1)
        dados_clientes['posicao'].append(i)


def saida_dados_format(solucao,dados_plantas,inst,seed):
    result = formata_solucao(solucao,dados_plantas)
    file = open("saidas/result_"+inst+"-seed_"+seed+".txt","w")
    file.write("Instalações : Clientes \n")
    for i in range(0,len(result)):
        file.write("%d : %s \n" %(i, result[i] ))
    file.write("fitness : %d \n" %(solucao['total']))
    file.close()
    return
