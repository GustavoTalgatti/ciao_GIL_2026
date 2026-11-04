import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class MLTuningProblem(ElementwiseProblem):
    def __init__(self):
        # x1: Profundidade da Árvore (1 a 30), x2: Número de Estimadores (10 a 200)
        super().__init__(n_var=2, n_obj=2, xl=np.array([1.0, 10.0]), xu=np.array([30.0, 200.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        depth, n_trees = x[0], x[1]
        f1_erro = 0.5 / (depth * np.log10(n_trees))   # Erro cai com mais árvores/profundidade
        f2_latencia_ms = (depth * 0.2) + (n_trees * 0.5) # Latência sobe
        out["F"] = [f1_erro, f2_latencia_ms]

res5 = minimize(MLTuningProblem(), NSGA2(pop_size=30), termination=('n_gen', 40), seed=7)

plt.figure(figsize=(7, 4))
plt.scatter(res5.F[:, 0], res5.F[:, 1], color='purple', s=45)
plt.title("Exercício 5 — Erro vs. Tempo de Inferência (ML)")
plt.xlabel("Erro do Modelo [Minimizar]")
plt.ylabel("Tempo de Resposta (ms) [Minimizar]")
plt.grid(True)
plt.savefig("imagens/exercicio_5.png", dpi=120, bbox_inches="tight")
plt.show()

# Resultados no console
print("Soluções não dominadas:", len(res5.F))
idx = np.argsort(res5.F[:, 0])
for i in idx[:10]:
    print(f"Profundidade: {res5.X[i][0]:5.2f} | Árvores: {res5.X[i][1]:6.2f} | Erro: {res5.F[i][0]:.4f} | Latência: {res5.F[i][1]:7.2f} ms")
