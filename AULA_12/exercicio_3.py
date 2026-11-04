import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class DroneProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=3, xl=np.array([10.0, 1.0]), xu=np.array([80.0, 5.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        velocidade, carga = x[0], x[1]
        f1_tempo = 1000.0 / velocidade
        f2_custo = (velocidade ** 2) * 0.1 + (carga * 50)
        f3_co2 = (velocidade * 1.5) / carga
        out["F"] = [f1_tempo, f2_custo, f3_co2]

res3 = minimize(DroneProblem(), NSGA2(pop_size=40), termination=('n_gen', 50), seed=42)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(res3.F[:, 0], res3.F[:, 1], res3.F[:, 2], color='green', s=40)
ax.set_xlabel("Tempo")
ax.set_ylabel("Custo")
ax.set_zlabel("CO2")
plt.title("Exercício 3 — Pareto 3D: Drones")
plt.savefig("imagens/exercicio_3.png", dpi=120, bbox_inches="tight")
plt.show()

# Resultados no console
F = res3.F; X = res3.X
print("Soluções não dominadas:", len(F))
print("Menor tempo  :", f"vel={X[np.argmin(F[:,0])][0]:.2f} carga={X[np.argmin(F[:,0])][1]:.2f}", np.round(F[np.argmin(F[:,0])],2))
print("Menor custo  :", f"vel={X[np.argmin(F[:,1])][0]:.2f} carga={X[np.argmin(F[:,1])][1]:.2f}", np.round(F[np.argmin(F[:,1])],2))
print("Menor CO2    :", f"vel={X[np.argmin(F[:,2])][0]:.2f} carga={X[np.argmin(F[:,2])][1]:.2f}", np.round(F[np.argmin(F[:,2])],2))
