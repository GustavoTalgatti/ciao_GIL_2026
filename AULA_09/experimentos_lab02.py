# Experimentos propostos no final do lab02_aula09.py
# Aqui montamos o sistema por uma função para poder trocar cada item e comparar.
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def monta(forma="tri", regra2="so_servico", metodo="centroid", excelente=False):
    servico = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "servico")
    comida = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "comida")
    gorjeta = ctrl.Consequent(np.arange(0, 25.01, 0.5), "gorjeta", defuzzify_method=metodo)

    comida["ruim"] = fuzz.trimf(comida.universe, [0, 0, 5])
    comida["medio"] = fuzz.trimf(comida.universe, [0, 5, 10])
    comida["bom"] = fuzz.trimf(comida.universe, [5, 10, 10])

    if forma == "tri":
        servico["ruim"] = fuzz.trimf(servico.universe, [0, 0, 5])
        servico["medio"] = fuzz.trimf(servico.universe, [0, 5, 10])
        servico["bom"] = fuzz.trimf(servico.universe, [5, 10, 10])
    elif forma == "trap":
        servico["ruim"] = fuzz.trapmf(servico.universe, [0, 0, 2, 5])
        servico["medio"] = fuzz.trapmf(servico.universe, [2, 4, 6, 8])
        servico["bom"] = fuzz.trapmf(servico.universe, [5, 8, 10, 10])
    elif forma == "gauss":
        servico["ruim"] = fuzz.gaussmf(servico.universe, 0, 2)
        servico["medio"] = fuzz.gaussmf(servico.universe, 5, 2)
        servico["bom"] = fuzz.gaussmf(servico.universe, 10, 2)

    if excelente:
        # 4 conjuntos no serviço: ruim, medio, bom e excelente
        servico["bom"] = fuzz.trimf(servico.universe, [4, 7, 9])
        servico["excelente"] = fuzz.trimf(servico.universe, [7, 10, 10])

    gorjeta["baixa"] = fuzz.trimf(gorjeta.universe, [0, 0, 13])
    gorjeta["media"] = fuzz.trimf(gorjeta.universe, [0, 13, 25])
    gorjeta["alta"] = fuzz.trimf(gorjeta.universe, [13, 25, 25])

    r2 = servico["medio"] if regra2 == "so_servico" else (servico["medio"] & comida["medio"])
    regras = [
        ctrl.Rule(servico["ruim"] | comida["ruim"], gorjeta["baixa"]),
        ctrl.Rule(r2, gorjeta["media"]),
        ctrl.Rule(servico["bom"] | comida["bom"], gorjeta["alta"]),
    ]
    if excelente:
        regras.append(ctrl.Rule(servico["excelente"], gorjeta["alta"]))
    return ctrl.ControlSystemSimulation(ctrl.ControlSystem(regras))


def calcula(sim, s, c):
    sim.input["servico"] = s
    sim.input["comida"] = c
    sim.compute()
    return sim.output["gorjeta"]


print("EXP 1 - regra 2 com E (7, 3)")
print("  original (so servico medio):", round(calcula(monta(), 7, 3), 2))
print("  com E (servico medio & comida medio):", round(calcula(monta(regra2="e"), 7, 3), 2))
print("  (teste extra com (7, 1))")
print("  original:", round(calcula(monta(), 7, 1), 2), "| com E:", round(calcula(monta(regra2="e"), 7, 1), 2))

print("EXP 2 - formato das curvas do servico (7, 3)")
for f in ["tri", "trap", "gauss"]:
    print(" ", f, round(calcula(monta(forma=f), 7, 3), 2))

print("EXP 3 - metodos de defuzzificacao (7, 3)")
for m in ["centroid", "bisector", "mom", "som", "lom"]:
    print(" ", m, round(calcula(monta(metodo=m), 7, 3), 2))

print("EXP 4 - com conjunto 'excelente' no servico (9, 5)")
print("  sem excelente:", round(calcula(monta(), 9, 5), 2))
print("  com excelente:", round(calcula(monta(excelente=True), 9, 5), 2))

print("EXP 5 - pontos pedidos")
for s, c in [(0, 0), (10, 10), (5, 5)]:
    print(f"  ({s}, {c}) ->", round(calcula(monta(), s, c), 2))
