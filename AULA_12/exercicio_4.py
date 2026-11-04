import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class PortfolioProblem(ElementwiseProblem):
    def __init__(self):
        # x1: % Renda Fixa (0 a 100), x2: % Ações (0 a 100)
        super().__init__(n_var=2, n_obj=2, xl=np.array([0.0, 0.0]), xu=np.array([100.0, 100.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        rf, acoes = x[0], x[1]

        # TODO 1: O Retorno Esperado é (rf * 0.08 + acoes * 0.18). 
        # Como o pymoo MINIMIZA por padrão, inverta o sinal do retorno para maximizá-lo!
        f1_retorno_negativo = -(rf * 0.08 + acoes * 0.18)

        # TODO 2: O Risco é dado por (rf * 0.02 + acoes * 0.25). Queremos MINIMIZAR o risco.
        f2_risco = rf * 0.02 + acoes * 0.25

        out["F"] = [f1_retorno_negativo, f2_risco]

# TODO 3: Execute o NSGA-II e plote o Risco (eixo X) versus Retorno Real (eixo Y - lembre de reverter o sinal!)
res4 = minimize(PortfolioProblem(), NSGA2(pop_size=40), termination=('n_gen', 50), seed=1)

risco = res4.F[:, 1]
retorno_real = -res4.F[:, 0]

plt.figure(figsize=(7, 4))
plt.scatter(risco, retorno_real, color='orange', s=45)
plt.title("Exercício 4 — Risco vs. Retorno: Portfólio")
plt.xlabel("Risco [Minimizar]")
plt.ylabel("Retorno Esperado [Maximizar]")
plt.grid(True)
plt.savefig("imagens/exercicio_4.png", dpi=120, bbox_inches="tight")
plt.show()

print("Soluções não dominadas:", len(risco))
idx = np.argsort(risco)
for i in idx[:10]:
    print(f"Renda Fixa: {res4.X[i][0]:6.2f}% | Ações: {res4.X[i][1]:6.2f}% | Risco: {risco[i]:7.2f} | Retorno: {retorno_real[i]:7.2f}")
