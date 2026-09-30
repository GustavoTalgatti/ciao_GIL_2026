# Lab 03 - ACO para projeto de topologia de rede de baixa latencia
# Aula 08 - Computational Intelligence & Algorithm Optimization

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PASTA = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# Matriz de latencias D (10x10, simetrica, em ms)
# O enunciado nao traz a matriz, entao geramos uma uma vez (valores entre 3 e 40)
# e deixamos fixa aqui. Se o professor passar a matriz oficial, e so trocar.
# ----------------------------------------------------------------------
D = np.array([
    [ 0, 12, 28,  6, 11, 15, 14, 37, 33, 37],
    [12,  0, 40,  5,  8, 35,  5,  9,  9, 37],
    [28, 40,  0, 16, 13,  9, 20, 25, 33, 26],
    [ 6,  5, 16,  0, 40,  7, 21, 24, 29,  3],
    [11,  8, 13, 40,  0, 10, 20,  5, 40, 27],
    [15, 35,  9,  7, 10,  0, 33, 22, 25, 16],
    [14,  5, 20, 21, 20, 33,  0, 15,  7, 10],
    [37,  9, 25, 24,  5, 22, 15,  0, 32, 19],
    [33,  9, 33, 29, 40, 25,  7, 32,  0, 34],
    [37, 37, 26,  3, 27, 16, 10, 19, 34,  0],
])
N = len(D)
ARESTAS = [(i, j) for i in range(N) for j in range(i + 1, N)]  # 45 arestas possiveis

# Parametros do ACO
N_FORMIGAS = 20
N_ITER = 100
ALFA = 1.0     # peso do feromonio
BETA = 3.0     # peso da heuristica (1/latencia)
RHO = 0.2      # taxa de evaporacao (pedida no enunciado)
Q = 100.0      # constante do deposito de feromonio
TOP_K = 3      # quantas formigas (melhores da iteracao) atualizam o feromonio
TAU_0 = 1.0    # feromonio inicial


# ----------------------------------------------------------------------
# Verificacao de ciclos / conectividade (Union-Find)
# ----------------------------------------------------------------------
def acha(pai, x):
    while pai[x] != x:
        pai[x] = pai[pai[x]]
        x = pai[x]
    return x


def une(pai, a, b):
    pai[acha(pai, a)] = acha(pai, b)


def arvore_valida(arestas):
    # uma arvore geradora de N nos tem exatamente N-1 arestas, sem ciclo e conectada
    if len(arestas) != N - 1:
        return False
    pai = list(range(N))
    for (i, j) in arestas:
        if acha(pai, i) == acha(pai, j):  # fechou um ciclo
            return False
        une(pai, i, j)
    raiz = acha(pai, 0)
    return all(acha(pai, k) == raiz for k in range(N))  # todos conectados


def custo(arestas):
    return sum(D[i][j] for (i, j) in arestas)


# ----------------------------------------------------------------------
# Construcao da arvore por uma formiga
# ----------------------------------------------------------------------
def constroi_arvore(tau, rng):
    pai = list(range(N))
    escolhidas = []

    while len(escolhidas) < N - 1:
        # so pode escolher arestas que ligam componentes diferentes
        # (assim nao forma ciclo e no fim tudo fica conectado)
        candidatas = [(i, j) for (i, j) in ARESTAS if acha(pai, i) != acha(pai, j)]

        pesos = np.array([(tau[i][j] ** ALFA) * ((1.0 / D[i][j]) ** BETA) for (i, j) in candidatas])
        probs = pesos / pesos.sum()

        k = rng.choice(len(candidatas), p=probs)
        i, j = candidatas[k]
        escolhidas.append((i, j))
        une(pai, i, j)

    return escolhidas


# ----------------------------------------------------------------------
# ACO completo
# ----------------------------------------------------------------------
def roda_aco(seed=0):
    rng = np.random.default_rng(seed)
    tau = np.full((N, N), TAU_0)

    melhor_global = None
    custo_global = np.inf
    hist_melhor_iter = []
    hist_global = []
    hist_media = []

    for it in range(N_ITER):
        formigas = []
        for _ in range(N_FORMIGAS):
            arv = constroi_arvore(tau, rng)
            assert arvore_valida(arv), "arvore invalida!"
            formigas.append((custo(arv), arv))

        formigas.sort(key=lambda x: x[0])

        if formigas[0][0] < custo_global:
            custo_global = formigas[0][0]
            melhor_global = formigas[0][1]

        # atualizacao do feromonio: so as melhores topologias da iteracao
        melhores = formigas[:TOP_K]

        # evapora (rho = 0.2) apenas nas arestas que aparecem nas melhores topologias
        arestas_das_melhores = set()
        for _, arv in melhores:
            arestas_das_melhores.update(arv)
        for (i, j) in arestas_das_melhores:
            tau[i][j] *= (1 - RHO)
            tau[j][i] = tau[i][j]

        # deposita feromonio (quanto menor o custo, mais deposita)
        for c, arv in melhores:
            for (i, j) in arv:
                tau[i][j] += Q / c
                tau[j][i] = tau[i][j]

        hist_melhor_iter.append(formigas[0][0])
        hist_global.append(custo_global)
        hist_media.append(np.mean([f[0] for f in formigas]))

    return melhor_global, custo_global, hist_melhor_iter, hist_global, hist_media


# ----------------------------------------------------------------------
# Referencias para comparar
# ----------------------------------------------------------------------
def arvore_aleatoria(rng):
    # sorteia a ordem das arestas e vai colocando as que nao formam ciclo
    ordem = list(range(len(ARESTAS)))
    rng.shuffle(ordem)
    pai = list(range(N))
    arv = []
    for k in ordem:
        i, j = ARESTAS[k]
        if acha(pai, i) != acha(pai, j):
            arv.append((i, j))
            une(pai, i, j)
        if len(arv) == N - 1:
            break
    return arv


def kruskal():
    # solucao exata do problema (so para saber o otimo)
    ordenadas = sorted(ARESTAS, key=lambda e: D[e[0]][e[1]])
    pai = list(range(N))
    arv = []
    for (i, j) in ordenadas:
        if acha(pai, i) != acha(pai, j):
            arv.append((i, j))
            une(pai, i, j)
    return arv


def matriz_adjacencia(arestas):
    A = np.zeros((N, N), dtype=int)
    for (i, j) in arestas:
        A[i][j] = 1
        A[j][i] = 1
    return A


# ----------------------------------------------------------------------
# Execucao principal
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("LAB 03 - ACO para topologia em arvore de 10 switches")
    print("=" * 70)
    print("Matriz de latencias D (ms):")
    print(D)
    print()
    print("Parametros: %d formigas | %d iteracoes | alfa=%.1f | beta=%.1f | rho=%.1f | top_k=%d" % (
        N_FORMIGAS, N_ITER, ALFA, BETA, RHO, TOP_K))
    print()

    # execucao principal (seed 42)
    melhor, c_aco, h_iter, h_glob, h_med = roda_aco(seed=42)
    print("Arvore final do ACO (seed = 42)")
    print("-" * 70)
    print("Valida (sem ciclo e conectada)?", arvore_valida(melhor))
    print("Arestas (switch_a, switch_b, latencia):")
    for (i, j) in sorted(melhor):
        print("   S%d - S%d : %d ms" % (i, j, D[i][j]))
    print("Latencia total = %d ms" % c_aco)
    print()
    print("Matriz de Adjacencia final (10x10):")
    A = matriz_adjacencia(melhor)
    print("     " + " ".join("S%-2d" % k for k in range(N)))
    for k in range(N):
        print("S%-2d  " % k + "  ".join(str(v) for v in A[k]))
    print("Soma de cada linha (grau de cada switch):", A.sum(axis=1))
    print("Numero de arestas:", A.sum() // 2, "(esperado: %d)" % (N - 1))
    print()

    # comparacao com topologia aleatoria
    rng = np.random.default_rng(7)
    arv_rand = arvore_aleatoria(rng)
    c_rand = custo(arv_rand)

    custos_rand = [custo(arvore_aleatoria(np.random.default_rng(s))) for s in range(1000)]
    media_rand = np.mean(custos_rand)

    arv_opt = kruskal()
    c_opt = custo(arv_opt)

    print("Comparacao com topologia aleatoria")
    print("-" * 70)
    print("Latencia da arvore aleatoria (1 sorteio, seed 7): %d ms" % c_rand)
    print("Latencia media de 1000 arvores aleatorias:        %.1f ms" % media_rand)
    print("Latencia do ACO:                                  %d ms" % c_aco)
    print("Latencia otima (Kruskal, so referencia):          %d ms" % c_opt)
    print()
    print("Ganho do ACO sobre o sorteio unico:   %.1f %%" % ((c_rand - c_aco) / c_rand * 100))
    print("Ganho do ACO sobre a media aleatoria: %.1f %%" % ((media_rand - c_aco) / media_rand * 100))
    print()

    # varias execucoes para ver estabilidade
    finais = [roda_aco(seed=s)[1] for s in range(20)]
    finais = np.array(finais)
    print("Estabilidade: 20 execucoes do ACO (seeds 0 a 19)")
    print("-" * 70)
    print("Latencia media=%.1f | desvio=%.2f | melhor=%d | pior=%d" % (
        finais.mean(), finais.std(), finais.min(), finais.max()))
    print("Execucoes que acharam o otimo (%d ms): %d de 20" % (c_opt, int(np.sum(finais == c_opt))))
    print()

    # evolucao
    print("Evolucao do custo (seed = 42)")
    print("-" * 70)
    print("%-10s %16s %16s %16s" % ("Iteracao", "melhor da iter.", "melhor global", "media formigas"))
    for it in [1, 5, 10, 20, 30, 50, 75, 100]:
        print("%-10d %16d %16d %16.1f" % (it, h_iter[it - 1], h_glob[it - 1], h_med[it - 1]))
    print()

    # grafico
    plt.figure(figsize=(8, 4.5))
    plt.plot(h_med, label="media das formigas", color="tab:gray")
    plt.plot(h_iter, label="melhor da iteracao", color="tab:blue")
    plt.plot(h_glob, label="melhor global", color="tab:red", linewidth=2)
    plt.axhline(c_opt, color="green", linestyle="--", label="otimo (Kruskal)")
    plt.axhline(media_rand, color="orange", linestyle=":", label="media aleatoria")
    plt.xlabel("Iteracao")
    plt.ylabel("Latencia total da arvore (ms)")
    plt.title("Evolucao do ACO")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    caminho = os.path.join(PASTA, "lab03_evolucao.png")
    plt.savefig(caminho, dpi=120)
    print("Grafico salvo em:", os.path.basename(caminho))
