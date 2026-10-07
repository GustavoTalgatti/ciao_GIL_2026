"""
LAB 03 - Projeto próprio: risco de evasão de um aluno (lógica fuzzy)

Entradas : frequencia (% de presença, 0 a 100) e desempenho (média das notas, 0 a 10)
Saída    : risco de evasão (pontos, 0 a 100)

Instalação:  pip install numpy matplotlib scikit-fuzzy
Execução:    python lab03_aula09.py
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ---------- 1) Variáveis linguísticas (universos de discurso) ----------
frequencia = ctrl.Antecedent(np.arange(0, 100.1, 0.5), "frequencia")   # % de presença
desempenho = ctrl.Antecedent(np.arange(0, 10.01, 0.1), "desempenho")   # média 0-10
risco = ctrl.Consequent(np.arange(0, 100.1, 0.5), "risco")             # pontos 0-100

# ---------- 2) Conjuntos fuzzy (funções de pertinência) ----------
# Trapézios nas pontas (onde a pertinência fica em 1 por uma faixa) e triângulo no meio
frequencia["baixa"] = fuzz.trapmf(frequencia.universe, [0, 0, 55, 70])
frequencia["media"] = fuzz.trimf(frequencia.universe, [60, 75, 90])
frequencia["alta"] = fuzz.trapmf(frequencia.universe, [80, 90, 100, 100])

desempenho["ruim"] = fuzz.trapmf(desempenho.universe, [0, 0, 3, 5])
desempenho["regular"] = fuzz.trimf(desempenho.universe, [4, 6, 8])
desempenho["bom"] = fuzz.trapmf(desempenho.universe, [7, 8.5, 10, 10])

risco["baixo"] = fuzz.trapmf(risco.universe, [0, 0, 20, 40])
risco["medio"] = fuzz.trimf(risco.universe, [30, 50, 70])
risco["alto"] = fuzz.trapmf(risco.universe, [60, 80, 100, 100])

# ---------- 3) Base de regras  (| = OU, & = E) ----------
regras = [
    ctrl.Rule(frequencia["baixa"] & desempenho["ruim"], risco["alto"]),                         # R1
    ctrl.Rule(frequencia["baixa"] & desempenho["regular"], risco["alto"]),                      # R2
    ctrl.Rule(frequencia["media"] & desempenho["ruim"], risco["alto"]),                         # R3
    ctrl.Rule(frequencia["media"] & desempenho["regular"], risco["medio"]),                     # R4
    ctrl.Rule(frequencia["baixa"] & desempenho["bom"], risco["medio"]),                         # R5
    ctrl.Rule(frequencia["alta"] & desempenho["ruim"], risco["medio"]),                         # R6
    ctrl.Rule(frequencia["media"] & desempenho["bom"], risco["baixo"]),                         # R7
    ctrl.Rule(frequencia["alta"] & (desempenho["regular"] | desempenho["bom"]), risco["baixo"]),  # R8 (E + OU)
]

# ---------- 4) Simulação ----------
sistema = ctrl.ControlSystem(regras)
sim = ctrl.ControlSystemSimulation(sistema)


def calcula_risco(freq, nota):
    sim.input["frequencia"] = freq
    sim.input["desempenho"] = nota
    sim.compute()
    return sim.output["risco"]


# ---------- 5) Testes (entrada, saída do sistema e resposta esperada) ----------
testes = [
    # (frequencia, desempenho, resposta esperada)
    (95, 9.0, "baixo"),
    (50, 2.0, "alto"),
    (75, 6.0, "medio"),
    (95, 2.0, "medio"),
    (50, 9.0, "medio"),
    (75, 9.0, "baixo"),
]


def classifica(valor):
    """Só para facilitar a leitura: converte o número em baixo / medio / alto."""
    if valor < 35:
        return "baixo"
    if valor <= 65:
        return "medio"
    return "alto"


print("Frequencia | Desempenho | Risco (sistema) | Classe | Esperado | OK?")
for freq, nota, esperado in testes:
    r = calcula_risco(freq, nota)
    ok = "sim" if classifica(r) == esperado else "nao"
    print(f"{freq:>10} | {nota:>10} | {r:>15.1f} | {classifica(r):>6} | {esperado:>8} | {ok}")

# ---------- 6) Gráficos ----------
os.makedirs("imagens", exist_ok=True)

frequencia.view()
plt.savefig("imagens/lab03_frequencia.png", dpi=110, bbox_inches="tight")
desempenho.view()
plt.savefig("imagens/lab03_desempenho.png", dpi=110, bbox_inches="tight")
risco.view()
plt.savefig("imagens/lab03_risco.png", dpi=110, bbox_inches="tight")

# resultado de um caso (frequência 95 e média 2.0) com a área agregada e o centroide
calcula_risco(95, 2.0)
risco.view(sim=sim)
plt.savefig("imagens/lab03_resultado_95_2.png", dpi=110, bbox_inches="tight")

plt.show()
