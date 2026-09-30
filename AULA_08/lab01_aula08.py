# Lab 01 - PSO para balanceamento dinamico de carga em datacenter
# Aula 08 - Computational Intelligence & Algorithm Optimization

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PASTA = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# Dados do enunciado
# ----------------------------------------------------------------------
C = np.array([42.0, 35.0, 58.0, 30.0, 50.0, 65.0])  # coeficiente de aquecimento de cada AZ (°C)
N_AZ = len(C)
LIMITE_CRITICO = 75.0  # temperatura maxima permitida (°C)

# O enunciado nao diz como a temperatura de cada AZ muda com a carga.
# Por isso assumimos que ela sobe junto com o peso recebido:
#     T_i = C_i * (1 + ALFA * w_i)
# Se fosse so sum(w_i * C_i), a resposta seria colocar tudo na AZ4 (a mais fria)
# e o problema nao teria graça.
ALFA = 3.0
PESO_PENALIDADE = 50.0  # quanto custa cada °C acima de 75

# Parametros do PSO
N_ITER = 100
INERCIA = 0.7
C1 = 1.5  # componente cognitivo (P_best)
C2 = 1.5  # componente social (G_best)
V_MAX = 0.2


# ----------------------------------------------------------------------
# Funcoes do problema
# ----------------------------------------------------------------------
def temperaturas(w):
    # temperatura de cada AZ dado o vetor de pesos
    return C * (1 + ALFA * w)


def fitness(w):
    T = temperaturas(w)
    temp_media = np.sum(w * T)  # temperatura media ponderada dos racks
    excesso = np.maximum(0, T - LIMITE_CRITICO)
    penalidade = PESO_PENALIDADE * np.sum(excesso)  # penalidade externa
    return temp_media + penalidade


def normalizar(x):
    # tira valores negativos e divide pela soma, assim sum(w) = 1
    x = np.clip(x, 1e-9, None)
    return x / np.sum(x)


# ----------------------------------------------------------------------
# PSO continuo feito do zero
# ----------------------------------------------------------------------
class PSO:
    def __init__(self, n_particulas, n_dim, funcao, n_iter=N_ITER, seed=None):
        self.n = n_particulas
        self.dim = n_dim
        self.funcao = funcao
        self.n_iter = n_iter
        self.rng = np.random.default_rng(seed)

        # historicos para o relatorio
        self.hist_gbest = []        # melhor fitness global a cada iteracao
        self.hist_pbest_medio = []  # media dos P_best a cada iteracao

    def executar(self):
        rng = self.rng

        # posicoes iniciais aleatorias ja normalizadas
        pos = np.array([normalizar(rng.random(self.dim)) for _ in range(self.n)])
        vel = rng.uniform(-0.05, 0.05, (self.n, self.dim))

        # P_best de cada particula
        pbest_pos = pos.copy()
        pbest_fit = np.array([self.funcao(p) for p in pos])

        # G_best
        i_melhor = np.argmin(pbest_fit)
        gbest_pos = pbest_pos[i_melhor].copy()
        gbest_fit = pbest_fit[i_melhor]

        for it in range(self.n_iter):
            r1 = rng.random((self.n, self.dim))
            r2 = rng.random((self.n, self.dim))

            # atualizacao da velocidade
            vel = (INERCIA * vel
                   + C1 * r1 * (pbest_pos - pos)
                   + C2 * r2 * (gbest_pos - pos))
            vel = np.clip(vel, -V_MAX, V_MAX)

            # atualizacao da posicao
            pos = pos + vel

            # normalizacao a cada iteracao (garante sum(w) = 1)
            pos = np.array([normalizar(p) for p in pos])

            # avalia as particulas
            fit = np.array([self.funcao(p) for p in pos])

            # atualiza P_best
            melhorou = fit < pbest_fit
            pbest_pos[melhorou] = pos[melhorou]
            pbest_fit[melhorou] = fit[melhorou]

            # atualiza G_best
            i_melhor = np.argmin(pbest_fit)
            if pbest_fit[i_melhor] < gbest_fit:
                gbest_fit = pbest_fit[i_melhor]
                gbest_pos = pbest_pos[i_melhor].copy()

            self.hist_gbest.append(gbest_fit)
            self.hist_pbest_medio.append(np.mean(pbest_fit))

        self.gbest_pos = gbest_pos
        self.gbest_fit = gbest_fit
        return gbest_pos, gbest_fit


# ----------------------------------------------------------------------
# Execucao principal
# ----------------------------------------------------------------------
if __name__ == "__main__":
    populacoes = [10, 30, 50]
    resultados = {}

    print("=" * 70)
    print("LAB 01 - PSO para balanceamento de carga entre 6 AZs")
    print("=" * 70)
    print("C =", C)
    print("Modelo: T_i = C_i * (1 + %.1f * w_i) | limite critico = %.0f °C" % (ALFA, LIMITE_CRITICO))
    print()

    # 1) uma execucao de cada populacao (seed 42) para a tabela e o grafico
    for n_part in populacoes:
        pso = PSO(n_part, N_AZ, fitness, seed=42)
        w_best, f_best = pso.executar()
        resultados[n_part] = (pso, w_best, f_best)

    print("Melhor distribuicao W encontrada (seed = 42)")
    print("-" * 70)
    for n_part in populacoes:
        pso, w_best, f_best = resultados[n_part]
        T = temperaturas(w_best)
        print("Populacao = %d particulas" % n_part)
        print("  W = [" + ", ".join("%.4f" % x for x in w_best) + "]")
        print("  sum(W) = %.10f -> %s" % (np.sum(w_best),
              "OK" if np.isclose(np.sum(w_best), 1.0) else "ERRO"))
        print("  Temperaturas por AZ = [" + ", ".join("%.2f" % t for t in T) + "]")
        print("  Temperatura maxima = %.2f °C (limite %.0f) -> %s" % (
            T.max(), LIMITE_CRITICO, "dentro do limite" if T.max() <= LIMITE_CRITICO + 1e-6 else "PASSOU DO LIMITE"))
        print("  Fitness final (temp. media ponderada) = %.4f" % f_best)
        print()

    # 2) evolucao do fitness em algumas iteracoes
    print("Evolucao do G_best (fitness) ao longo das iteracoes")
    print("-" * 70)
    print("%-10s %12s %12s %12s" % ("Iteracao", "10 part.", "30 part.", "50 part."))
    for it in [1, 5, 10, 20, 30, 50, 75, 100]:
        linha = "%-10d" % it
        for n_part in populacoes:
            linha += " %12.4f" % resultados[n_part][0].hist_gbest[it - 1]
        print(linha)
    print()

    # 3) repete 20 vezes com seeds diferentes para ver se o resultado e estavel
    print("Estabilidade: 20 execucoes com seeds diferentes (100 iteracoes)")
    print("-" * 70)
    print("%-12s %14s %14s %14s %14s" % ("Populacao", "Media final", "Desvio", "Melhor", "Pior"))
    for n_part in populacoes:
        finais = []
        for s in range(20):
            p = PSO(n_part, N_AZ, fitness, seed=s)
            p.executar()
            finais.append(p.gbest_fit)
        finais = np.array(finais)
        print("%-12d %14.5f %14.5f %14.5f %14.5f" % (
            n_part, finais.mean(), finais.std(), finais.min(), finais.max()))
    print()

    # 4) grafico
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    cores = {10: "tab:red", 30: "tab:blue", 50: "tab:green"}
    for n_part in populacoes:
        ax[0].plot(resultados[n_part][0].hist_gbest, label="%d particulas" % n_part, color=cores[n_part])
        ax[1].plot(resultados[n_part][0].hist_gbest, label="%d particulas" % n_part, color=cores[n_part])
    ax[0].set_title("Evolucao do G_best (visao geral)")
    ax[0].set_xlabel("Iteracao")
    ax[0].set_ylabel("Fitness (temp. media ponderada, °C)")
    ax[0].legend()
    ax[0].grid(alpha=0.3)

    melhor_final = min(resultados[n][2] for n in populacoes)
    ax[1].set_ylim(melhor_final - 0.05, melhor_final + 1.5)
    ax[1].set_title("Zoom perto do valor final")
    ax[1].set_xlabel("Iteracao")
    ax[1].set_ylabel("Fitness (°C)")
    ax[1].legend()
    ax[1].grid(alpha=0.3)

    plt.tight_layout()
    caminho = os.path.join(PASTA, "lab01_convergencia.png")
    plt.savefig(caminho, dpi=120)
    print("Grafico salvo em:", os.path.basename(caminho))
