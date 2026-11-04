import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class SOCAllocationProblem(ElementwiseProblem):
    def __init__(self):
        # TODO 1: Defina 2 variáveis (x1: 1 a 50 analistas, x2: 1 a 10 regimento de segurança)
        # TODO 2: Defina 2 objetivos a serem minimizados
        super().__init__(
            n_var=2,
            n_obj=2,
            xl=np.array([1.0, 1.0]),
            xu=np.array([50.0, 10.0])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        analistas, regimento = x[0], x[1]
        
        # TODO 3: Implemente a fórmula do Custo (R$ 100 por analista + R$ 50 por regimento)
        f1_custo = analistas * 100.0 + regimento * 50.0
        
        # TODO 4: Implemente o Tempo de Resposta em minutos (200 / analistas + 50 / regimento)
        f2_tempo = 200.0 / analistas + 50.0 / regimento

        out["F"] = [f1_custo, f2_tempo]

# TODO 5: Instancie o algoritmo NSGA2 com pop_size=30 e execute a minimização com 40 gerações
algorithm = NSGA2(pop_size=30)
res2 = minimize(SOCAllocationProblem(), algorithm, termination=('n_gen', 40), seed=1)

print("Soluções não dominadas:", len(res2.F))
idx = np.argsort(res2.F[:, 0])
for i in idx:
    print(f"Analistas: {res2.X[i][0]:5.2f} | Regimento: {res2.X[i][1]:5.2f} | Custo: R$ {res2.F[i][0]:8.2f} | Tempo: {res2.F[i][1]:6.2f} min")
