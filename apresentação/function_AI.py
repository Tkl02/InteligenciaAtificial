import random


def funcao_objetivo(x1, x2):
    """Calcular o valor da função objetivo."""
    return (x1**2 + x2 - 11) + (x1 + x2**2 - 7)**2


def decodificar_individuo(cromosomo):
    """Decodifica uma string binária (cromosomo) para valores reais."""
    x1 = int(cromosomo[:10], 2) / 1023 * 6
    x2 = int(cromosomo[10:], 2) / 1023 * 6
    return x1, x2


def funcao_adaptacao(individuo):
    """Calcula a adaptação do indivíduo baseado no valor da função objetivo."""
    x1, x2 = decodificar_individuo(individuo)
    return 1 / (1 + funcao_objetivo(x1, x2))


def selecionar(populacao, adaptacoes):
    """Seleciona indivíduos para reprodução baseado em amostra estocástica sem substituição."""
    adaptacoes = [ad + 1e-6 for ad in adaptacoes]  # Soma um valor pequeno para evitar divisão por zero.
    ads_sum = sum(adaptacoes)
    probabilidades = [ad / ads_sum for ad in adaptacoes]
    selecionados = random.choices(populacao, probabilidades, k=len(populacao))
    return selecionados


def cruzar(individuo1, individuo2):
    """Cruza 2 (dois) indivíduos de acordo com uma probabilidade."""
    if random.random() < 0.8:  # 80% de chance.
        ponto_cruzamento = random.randint(1, len(individuo1) - 1)
        filho1 = individuo1[:ponto_cruzamento] + individuo2[ponto_cruzamento:]
        filho2 = individuo2[:ponto_cruzamento] + individuo1[ponto_cruzamento:]
        return filho1, filho2
    else:
        return individuo1, individuo2


def mutar(individuo):
    """Muta um indivíduo de acordo com uma probabilidade."""
    individuo_mutado = list(individuo)
    for i in range(len(individuo)):
        if random.random() < 0.05:  # 5% de chance.
            individuo_mutado[i] = '1' if individuo[i] == '0' else '0'
    return "".join(individuo_mutado)


def algoritmo_genetico(tamanho_populacao=20, geracoes=1000):
    """Implementa o algorítmo genético utilizando as funções acima."""
    print('-' * 130)
    while True:
        populacao = ["".join(random.choices(['0', '1'], k=20)) for _ in range(tamanho_populacao)]
        melhor_individuo, melhor_adaptacao, geracao = None, None, 1
        for g in range(geracoes):
            adaptacoes = [funcao_adaptacao(individuo) for individuo in populacao]
            populacao_selecionada = selecionar(populacao, adaptacoes)
            filhos = []
            for i in range(0, len(populacao_selecionada), 2):
                pai1, pai2 = populacao_selecionada[i], populacao_selecionada[i+1]
                filho1, filho2 = cruzar(pai1, pai2)
                filhos.extend([mutar(filho1), mutar(filho2)])
            populacao_elitismo = [populacao[i] for i in range(2)]  # Elitismo com os 2 (dois) melhores indivíduos.
            populacao = populacao_elitismo + filhos[:max(tamanho_populacao - 2, 0)]
            individuo = max(populacao, key=funcao_adaptacao)
            adaptacao = funcao_adaptacao(individuo)
            if melhor_individuo is None:
                melhor_individuo = individuo
                melhor_adaptacao = adaptacao
                geracao += 1
            elif adaptacao < melhor_adaptacao:
                melhor_individuo = individuo
                melhor_adaptacao = adaptacao
                geracao += 1
        tupla_decodificada = decodificar_individuo(melhor_individuo)
        print(f'Geração {geracao}\nMelhor solução: {melhor_individuo}\nAdaptação: {melhor_adaptacao}\nIndivíduo Decodificado: {tupla_decodificada}\nValor da Função: {funcao_objetivo(tupla_decodificada[0], tupla_decodificada[1])}')
        print('-' * 130)
        try:
            res = input('Proceed? [y/n] ')
            print('-' * 150)
        except:
            break
        else:
            if 'n' in res.lower():
                break


if __name__ == '__main__':
    algoritmo_genetico()