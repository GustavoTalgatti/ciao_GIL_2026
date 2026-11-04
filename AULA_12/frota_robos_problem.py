import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize


class FrotaRobosProblem(ElementwiseProblem):
    def __init__(self):
        # x1: número de robôs [5, 50] | x2: velocidade média [1.0, 4.0] m/s
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.array([5.0, 1.0]),
            xu=np.array([50.0, 4.0])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        x1, x2 = x[0], x[1]

        # Objetivo 1: custo total (R$ mil)
        f1 = (x1 * 25.0) + (x2 ** 2 * 8.0)

        # Objetivo 2: tempo médio de ciclo (minutos)
        f2 = 120.0 / x1 + 40.0 / x2

        # Restrição: consumo de energia C(x1, x2) = x1 * x2^1.5 <= 120
        consumo = x1 * (x2 ** 1.5)
        g1 = consumo - 120.0

        out["F"] = [f1, f2]
        out["G"] = [g1]


if __name__ == "__main__":
    problema = FrotaRobosProblem()
    algoritmo = NSGA2(pop_size=40)
    res = minimize(problema, algoritmo, termination=('n_gen', 60), seed=1)

    X = np.atleast_2d(res.X)
    F = np.atleast_2d(res.F)
    print("Soluções não dominadas:", len(F))

    # Escolha das 3 soluções de trade-off
    i_custo = np.argmin(F[:, 0])     # menor custo
    i_tempo = np.argmin(F[:, 1])     # menor tempo
    # intermediária: ponto mais próximo do meio (valores normalizados)
    Fn = (F - F.min(axis=0)) / (F.max(axis=0) - F.min(axis=0))
    i_meio = np.argmin(np.abs(Fn[:, 0] - 0.5) + np.abs(Fn[:, 1] - 0.5))

    nomes = [("Menor custo", i_custo), ("Menor tempo", i_tempo), ("Intermediária", i_meio)]
    for nome, i in nomes:
        consumo = X[i][0] * X[i][1] ** 1.5
        print(f"\n{nome}")
        print(f"  Robôs: {X[i][0]:.2f} | Velocidade: {X[i][1]:.2f} m/s")
        print(f"  Custo: R$ {F[i][0]:.2f} mil | Tempo de ciclo: {F[i][1]:.2f} min | Consumo: {consumo:.2f}")

    plt.figure(figsize=(8, 5))
    plt.scatter(F[:, 0], F[:, 1], color='teal', s=40, label="Soluções não dominadas")
    for (nome, i), cor in zip(nomes, ["red", "blue", "black"]):
        plt.scatter(F[i, 0], F[i, 1], color=cor, s=110, marker='*', label=nome, zorder=5)
    plt.title("Exercício 7 — Fronteira de Pareto: Frota de Robôs")
    plt.xlabel("Custo total (R$ mil) [Minimizar]")
    plt.ylabel("Tempo médio de ciclo (min) [Minimizar]")
    plt.grid(True)
    plt.legend()
    plt.savefig("imagens/exercicio_7.png", dpi=120, bbox_inches="tight")
    plt.show()
