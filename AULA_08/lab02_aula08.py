# Lab 02 - AG binario para selecao de microsservicos em Edge
# Aula 08 - Computational Intelligence & Algorithm Optimization

import os
import itertools
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PASTA = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# Dados do problema
# O enunciado nao traz a tabela dos 15 servicos, entao montamos uma
# (fixa, sempre a mesma). Se o professor passar a tabela oficial,
# e so trocar as tres listas abaixo.
# ----------------------------------------------------------------------
NOMES = ["Autenticacao", "Cache", "Telemetria", "Pagamentos", "Catalogo",
         "Busca", "Notificacoes", "Recomendacao", "Logs", "API Gateway",
         "Chat", "Analytics", "Video", "Backup", "Monitoramento"]
VALOR = np.array([80, 60, 40, 95, 70, 65, 35, 85, 30, 90, 50, 55, 75, 25, 45])
RAM = np.array([2.0, 3.5, 1.5, 4.0, 3.0, 2.5, 1.0, 5.0, 2.0, 2.5, 2.0, 3.5, 4.5, 3.0, 1.5])
CPU = np.array([1.0, 0.5, 0.5, 1.5, 1.0, 1.0, 0.5, 2.0, 0.5, 1.0, 1.0, 1.5, 2.0, 1.0, 0.5])

N_SERV = len(VALOR)
RAM_MAX = 16.0
CPU_MAX = 8.0

# Parametros do AG
TAM_POP = 50
N_GER = 100
K_TORNEIO = 3
TX_CROSSOVER = 0.8
TX_MUTACAO = 0.02  # por bit
PENALIDADE_B = 80.0  # pontos perdidos por GB ou core excedido
N_EXECUCOES = 20


# ----------------------------------------------------------------------
# Funcoes auxiliares
# ----------------------------------------------------------------------
def totais(ind):
    return np.sum(ind * VALOR), np.sum(ind * RAM), np.sum(ind * CPU)


def viavel(ind):
    _, ram, cpu = totais(ind)
    return ram <= RAM_MAX and cpu <= CPU_MAX


def fitness_A(ind):
    # Estrategia A: penalidade rigida, se violar qualquer limite o fitness e 0
    valor, ram, cpu = totais(ind)
    if ram > RAM_MAX or cpu > CPU_MAX:
        return 0.0
    return float(valor)


def fitness_B(ind):
    # Estrategia B: penalidade proporcional ao que passou do limite
    valor, ram, cpu = totais(ind)
    exc_ram = max(0.0, ram - RAM_MAX)
    exc_cpu = max(0.0, cpu - CPU_MAX)
    f = valor - PENALIDADE_B * (exc_ram + exc_cpu)
    return float(max(0.0, f))


def diversidade(pop):
    # distancia de Hamming media entre todos os pares, dividida por N_SERV
    # (0 = todo mundo igual, perto de 0.5 = populacao bem variada)
    n = len(pop)
    dist = (pop[:, None, :] != pop[None, :, :]).sum(axis=2)
    return dist.sum() / (n * (n - 1)) / N_SERV


# ----------------------------------------------------------------------
# Operadores do AG
# ----------------------------------------------------------------------
def torneio(pop, fits, rng):
    idx = rng.integers(0, len(pop), K_TORNEIO)
    melhor = idx[np.argmax(fits[idx])]
    return pop[melhor].copy()


def crossover_ponto_unico(p1, p2, rng):
    if rng.random() < TX_CROSSOVER:
        ponto = rng.integers(1, N_SERV)  # ponto de corte entre 1 e N-1
        f1 = np.concatenate([p1[:ponto], p2[ponto:]])
        f2 = np.concatenate([p2[:ponto], p1[ponto:]])
        return f1, f2
    return p1.copy(), p2.copy()


def mutacao_binaria(ind, rng):
    mascara = rng.random(N_SERV) < TX_MUTACAO
    ind[mascara] = 1 - ind[mascara]
    return ind


# ----------------------------------------------------------------------
# AG completo
# ----------------------------------------------------------------------
def roda_ag(funcao_fitness, seed):
    rng = np.random.default_rng(seed)
    pop = rng.integers(0, 2, (TAM_POP, N_SERV))

    hist = {"media": [], "desvio": [], "diversidade": [], "distintos": [], "inviaveis": [], "melhor_viavel": []}
    melhor_ind = None
    melhor_valor = -1

    for g in range(N_GER):
        fits = np.array([funcao_fitness(ind) for ind in pop])

        hist["media"].append(fits.mean())
        hist["desvio"].append(fits.std())
        hist["diversidade"].append(diversidade(pop))
        hist["distintos"].append(len(set(map(tuple, pop))))  # genomas diferentes na populacao
        hist["inviaveis"].append(np.mean([not viavel(ind) for ind in pop]) * 100)

        # guarda o melhor individuo VIAVEL (valor real de negocio)
        for ind in pop:
            if viavel(ind):
                v = np.sum(ind * VALOR)
                if v > melhor_valor:
                    melhor_valor = v
                    melhor_ind = ind.copy()
        hist["melhor_viavel"].append(melhor_valor)

        # nova geracao (com elitismo de 1 individuo)
        nova = [pop[np.argmax(fits)].copy()]
        while len(nova) < TAM_POP:
            p1 = torneio(pop, fits, rng)
            p2 = torneio(pop, fits, rng)
            f1, f2 = crossover_ponto_unico(p1, p2, rng)
            nova.append(mutacao_binaria(f1, rng))
            if len(nova) < TAM_POP:
                nova.append(mutacao_binaria(f2, rng))
        pop = np.array(nova)

    return hist, melhor_ind, melhor_valor


def forca_bruta():
    # testa as 2^15 combinacoes so para saber qual e a resposta certa
    melhor_v, melhor_ind = -1, None
    for combo in itertools.product([0, 1], repeat=N_SERV):
        ind = np.array(combo)
        if viavel(ind):
            v = np.sum(ind * VALOR)
            if v > melhor_v:
                melhor_v, melhor_ind = v, ind
    return melhor_v, melhor_ind


def descreve(ind):
    valor, ram, cpu = totais(ind)
    nomes = [NOMES[i] for i in range(N_SERV) if ind[i] == 1]
    return valor, ram, cpu, nomes


# ----------------------------------------------------------------------
# Execucao principal
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("LAB 02 - AG binario: selecao de microsservicos no Edge")
    print("=" * 70)
    print("%-3s %-15s %6s %8s %6s" % ("#", "Servico", "Valor", "RAM(GB)", "CPU"))
    for i in range(N_SERV):
        print("%-3d %-15s %6d %8.1f %6.1f" % (i + 1, NOMES[i], VALOR[i], RAM[i], CPU[i]))
    print("Total: valor=%d | RAM=%.1f GB | CPU=%.1f cores" % (VALOR.sum(), RAM.sum(), CPU.sum()))
    print("Limites: RAM <= %.0f GB e CPU <= %.0f cores" % (RAM_MAX, CPU_MAX))
    print()

    # resposta certa por forca bruta
    v_otimo, ind_otimo = forca_bruta()
    v, r, c, nomes = descreve(ind_otimo)
    print("Solucao otima (forca bruta, 2^15 combinacoes):")
    print("  genoma =", "".join(map(str, ind_otimo)))
    print("  valor=%d | RAM=%.1f | CPU=%.1f" % (v, r, c))
    print("  servicos:", ", ".join(nomes))
    print()

    # roda as 20 execucoes de cada estrategia
    estrategias = {"A": fitness_A, "B": fitness_B}
    todos = {}
    for nome, f in estrategias.items():
        execs = []
        for s in range(N_EXECUCOES):
            execs.append(roda_ag(f, seed=s))
        todos[nome] = execs

    # ---- execucao com seed 0 (exemplo detalhado) ----
    print("Melhor combinacao final de uma execucao (seed = 0)")
    print("-" * 70)
    for nome in ["A", "B"]:
        hist, ind, val = todos[nome][0]
        v, r, c, nomes = descreve(ind)
        print("Estrategia %s: genoma=%s | valor=%d | RAM=%.1f | CPU=%.1f" % (
            nome, "".join(map(str, ind)), v, r, c))
        print("   servicos:", ", ".join(nomes))
    print()

    # ---- estatisticas de 20 execucoes ----
    print("Resumo de %d execucoes (seeds 0 a %d)" % (N_EXECUCOES, N_EXECUCOES - 1))
    print("-" * 70)
    for nome in ["A", "B"]:
        valores = np.array([e[2] for e in todos[nome]])
        acertos = int(np.sum(valores == v_otimo))
        print("Estrategia %s: valor final medio=%.1f | desvio=%.1f | pior=%d | melhor=%d | achou o otimo (%d) em %d de %d execucoes" % (
            nome, valores.mean(), valores.std(), valores.min(), valores.max(), v_otimo, acertos, N_EXECUCOES))
    print()

    # medias das curvas (media das 20 execucoes)
    curvas = {}
    for nome in ["A", "B"]:
        curvas[nome] = {}
        for chave in ["media", "desvio", "diversidade", "distintos", "inviaveis", "melhor_viavel"]:
            curvas[nome][chave] = np.mean([e[0][chave] for e in todos[nome]], axis=0)

    print("Fitness medio e desvio-padrao da populacao por geracao (media das 20 execucoes)")
    print("-" * 70)
    print("%-6s | %-26s | %-26s" % ("Ger.", "Estrategia A", "Estrategia B"))
    print("%-6s | %12s %13s | %12s %13s" % ("", "media", "desvio", "media", "desvio"))
    for g in [1, 5, 10, 20, 30, 50, 75, 100]:
        print("%-6d | %12.2f %13.2f | %12.2f %13.2f" % (
            g, curvas["A"]["media"][g - 1], curvas["A"]["desvio"][g - 1],
            curvas["B"]["media"][g - 1], curvas["B"]["desvio"][g - 1]))
    print()

    print("Diversidade genetica e %% de individuos inviaveis (media das %d execucoes)" % N_EXECUCOES)
    print("-" * 70)
    print("%-6s | %-32s | %-32s" % ("Ger.", "Estrategia A", "Estrategia B"))
    print("%-6s | %9s %9s %11s | %9s %9s %11s" % ("", "Hamming", "distintos", "% inviav.", "Hamming", "distintos", "% inviav."))
    for g in [1, 5, 10, 20, 30, 50, 75, 100]:
        print("%-6d | %9.3f %9.1f %11.1f | %9.3f %9.1f %11.1f" % (
            g, curvas["A"]["diversidade"][g - 1], curvas["A"]["distintos"][g - 1], curvas["A"]["inviaveis"][g - 1],
            curvas["B"]["diversidade"][g - 1], curvas["B"]["distintos"][g - 1], curvas["B"]["inviaveis"][g - 1]))
    print("Media ao longo das 100 geracoes:")
    print("  Hamming medio:      A = %.3f | B = %.3f" % (curvas["A"]["diversidade"].mean(), curvas["B"]["diversidade"].mean()))
    print("  Genomas distintos:  A = %.1f | B = %.1f (de %d individuos)" % (
        curvas["A"]["distintos"].mean(), curvas["B"]["distintos"].mean(), TAM_POP))
    print()

    # ---- graficos ----
    ger = np.arange(1, N_GER + 1)
    fig, ax = plt.subplots(2, 2, figsize=(12, 8))

    for nome, cor in [("A", "tab:red"), ("B", "tab:blue")]:
        ax[0][0].plot(ger, curvas[nome]["media"], label="Estrategia " + nome, color=cor)
        ax[0][1].plot(ger, curvas[nome]["desvio"], label="Estrategia " + nome, color=cor)
        ax[1][0].plot(ger, curvas[nome]["diversidade"], label="Estrategia " + nome, color=cor)
        ax[1][1].plot(ger, curvas[nome]["melhor_viavel"], label="Estrategia " + nome, color=cor)

    ax[0][0].set_title("Fitness medio da populacao")
    ax[0][1].set_title("Desvio-padrao do fitness")
    ax[1][0].set_title("Diversidade genetica (Hamming medio)")
    ax[1][1].set_title("Melhor valor viavel encontrado")
    ax[1][1].axhline(v_otimo, color="gray", linestyle="--", label="otimo (forca bruta)")
    for a in ax.flatten():
        a.set_xlabel("Geracao")
        a.grid(alpha=0.3)
        a.legend()
    plt.tight_layout()
    caminho = os.path.join(PASTA, "lab02_comparacao.png")
    plt.savefig(caminho, dpi=120)
    print("Grafico salvo em:", os.path.basename(caminho))
