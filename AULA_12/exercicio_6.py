import numpy as np
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class EVBatteryProblem(ElementwiseProblem):
    def __init__(self):
        # x1: Potência de Carga (10 a 150 kW), x2: Temperatura do Ar (15 a 45 °C)
        # TODO 1: Configurar 2 variáveis, 2 objetivos e 1 RESTRIÇÃO de desigualdade (n_ieq_constr=1)
        super().__init__(n_var=2, n_obj=2, n_ieq_constr=1, xl=np.array([10.0, 15.0]), xu=np.array([150.0, 45.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        potencia, temp = x[0], x[1]

        f1_tempo_recarga = 3000.0 / potencia
        f2_desgaste_bateria = (potencia ** 1.5) * (temp / 20.0)

        # TODO 2: Adicione a restrição de segurança: O desgaste (f2) NÃO PODE ultrapassar 1500 unidades.
        # Dica no pymoo: Restrições de desigualdade devem ser escritas na forma G(x) <= 0.
        # Logo: g1 = f2_desgaste_bateria - 1500.0
        g1 = f2_desgaste_bateria - 1500.0
        
        out["F"] = [f1_tempo_recarga, f2_desgaste_bateria]
        # TODO 3: Passe a restrição para a saída: out["G"] = [g1]
        out["G"] = [g1]

# TODO 4: Execute a otimização com o NSGA-II e imprima no console apenas as soluções viáveis!
res6 = minimize(EVBatteryProblem(), NSGA2(pop_size=40), termination=('n_gen', 50), seed=1)

if res6.X is None:
    print("Nenhuma solução viável encontrada.")
else:
    X = np.atleast_2d(res6.X); F = np.atleast_2d(res6.F); G = np.atleast_2d(res6.G)
    viaveis = G[:, 0] <= 0
    print("Soluções viáveis:", int(viaveis.sum()))
    idx = np.argsort(F[:, 0])
    for i in idx:
        if viaveis[i]:
            print(f"Potência: {X[i][0]:6.2f} kW | Temp: {X[i][1]:5.2f} °C | Tempo recarga: {F[i][0]:6.2f} | Desgaste: {F[i][1]:7.2f}")
