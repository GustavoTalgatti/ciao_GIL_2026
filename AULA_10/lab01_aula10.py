# AULA 10 - Motor de Inferência Mamdani e Superfície 3D (Sprint 2 da AC-3)
# Disciplina: Inteligência Computacional
# Problema: definir a urgência de resposta a um incidente de segurança
# a partir do Impacto (0-100 %) e da Explorabilidade (0-10).

#Fuzzificação
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Criando as variáveis do problema
impacto = ctrl.Antecedent(np.arange(0, 101, 1), 'impacto')
explorabilidade = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'explorabilidade')
urgencia = ctrl.Consequent(np.arange(0, 101, 1), 'urgencia', defuzzify_method='centroid')

# Criando as funções de pertinência para o impacto
impacto['baixo'] = fuzz.trimf(impacto.universe, [0, 0, 40])
impacto['médio'] = fuzz.trimf(impacto.universe, [20, 50, 80])
impacto['alto'] = fuzz.trimf(impacto.universe, [60, 100, 100])

# Criando as funções de pertinência para a explorabilidade
explorabilidade['baixa'] = fuzz.trimf(explorabilidade.universe, [0, 0, 4])
explorabilidade['moderada'] = fuzz.trimf(explorabilidade.universe, [2, 5, 8])
explorabilidade['alta'] = fuzz.trimf(explorabilidade.universe, [6, 10, 10])

# Criando as funções de pertinência para a urgência (todas triangulares)
urgencia['baixa'] = fuzz.trimf(urgencia.universe, [0, 0, 13])
urgencia['média'] = fuzz.trimf(urgencia.universe, [10, 30, 50])
urgencia['alta'] = fuzz.trimf(urgencia.universe, [30, 60, 90])
urgencia['crítica'] = fuzz.trimf(urgencia.universe, [62.5, 100, 100])

# Visualizando as funções de pertinência para cada variável
impacto.view()
explorabilidade.view()
urgencia.view()


# Inferência Fuzzy
# Matriz de Regras 3x3 (9 regras)
rule1 = ctrl.Rule(impacto['baixo'] & explorabilidade['baixa'], urgencia['baixa'])
rule2 = ctrl.Rule(impacto['baixo'] & explorabilidade['moderada'], urgencia['baixa'])
rule3 = ctrl.Rule(impacto['baixo'] & explorabilidade['alta'], urgencia['média'])
rule4 = ctrl.Rule(impacto['médio'] & explorabilidade['baixa'], urgencia['média'])
rule5 = ctrl.Rule(impacto['médio'] & explorabilidade['moderada'], urgencia['alta'])
rule6 = ctrl.Rule(impacto['médio'] & explorabilidade['alta'], urgencia['alta'])
rule7 = ctrl.Rule(impacto['alto'] & explorabilidade['baixa'], urgencia['crítica'])
rule8 = ctrl.Rule(impacto['alto'] & explorabilidade['moderada'], urgencia['crítica'])
rule9 = ctrl.Rule(impacto['alto'] & explorabilidade['alta'], urgencia['crítica'])

# Sistema Fuzzy e Simulação
regras = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9]
urgencia_ctrl = ctrl.ControlSystem(regras)
urgencia_simulador = ctrl.ControlSystemSimulation(urgencia_ctrl)

# Defuzzificação - testando os extremos com o Centroide
urgencia_simulador.input['impacto'] = 0
urgencia_simulador.input['explorabilidade'] = 0
urgencia_simulador.compute()
print('Entrada (0, 0)   -> urgência = %.2f %%' % urgencia_simulador.output['urgencia'])

urgencia_simulador.input['impacto'] = 100
urgencia_simulador.input['explorabilidade'] = 10
urgencia_simulador.compute()
print('Entrada (100, 10) -> urgência = %.2f %%' % urgencia_simulador.output['urgencia'])

# Gráfico da saída (região resultante) para o caso (100, 10)
urgencia.view(sim=urgencia_simulador)
plt.savefig('saida_centroide.png', dpi=150, bbox_inches='tight')


# ------------------------------------------------------------------
# DESAFIO DOS EXTREMOS - Abordagem A x Abordagem B
# ------------------------------------------------------------------
def montar_sistema(critica_trapezio=None, metodo='centroid'):
    # Recria o sistema inteiro mudando só a Urgência Crítica e/ou o método
    imp = ctrl.Antecedent(np.arange(0, 101, 1), 'impacto')
    exp = ctrl.Antecedent(np.arange(0, 10.1, 0.1), 'explorabilidade')
    urg = ctrl.Consequent(np.arange(0, 101, 1), 'urgencia', defuzzify_method=metodo)

    imp['baixo'] = fuzz.trimf(imp.universe, [0, 0, 40])
    imp['médio'] = fuzz.trimf(imp.universe, [20, 50, 80])
    imp['alto'] = fuzz.trimf(imp.universe, [60, 100, 100])

    exp['baixa'] = fuzz.trimf(exp.universe, [0, 0, 4])
    exp['moderada'] = fuzz.trimf(exp.universe, [2, 5, 8])
    exp['alta'] = fuzz.trimf(exp.universe, [6, 10, 10])

    urg['baixa'] = fuzz.trimf(urg.universe, [0, 0, 13])
    urg['média'] = fuzz.trimf(urg.universe, [10, 30, 50])
    urg['alta'] = fuzz.trimf(urg.universe, [30, 60, 90])
    if critica_trapezio is not None:
        urg['crítica'] = fuzz.trapmf(urg.universe, critica_trapezio)
    else:
        urg['crítica'] = fuzz.trimf(urg.universe, [62.5, 100, 100])

    r1 = ctrl.Rule(imp['baixo'] & exp['baixa'], urg['baixa'])
    r2 = ctrl.Rule(imp['baixo'] & exp['moderada'], urg['baixa'])
    r3 = ctrl.Rule(imp['baixo'] & exp['alta'], urg['média'])
    r4 = ctrl.Rule(imp['médio'] & exp['baixa'], urg['média'])
    r5 = ctrl.Rule(imp['médio'] & exp['moderada'], urg['alta'])
    r6 = ctrl.Rule(imp['médio'] & exp['alta'], urg['alta'])
    r7 = ctrl.Rule(imp['alto'] & exp['baixa'], urg['crítica'])
    r8 = ctrl.Rule(imp['alto'] & exp['moderada'], urg['crítica'])
    r9 = ctrl.Rule(imp['alto'] & exp['alta'], urg['crítica'])

    return ctrl.ControlSystemSimulation(ctrl.ControlSystem([r1, r2, r3, r4, r5, r6, r7, r8, r9]))

def calcular(sim, i, e):
    sim.input['impacto'] = i
    sim.input['explorabilidade'] = e
    sim.compute()
    return sim.output['urgencia']

sistemas = {
    'Original (triângulo + centroide)': montar_sistema(None, 'centroid'),
    'A1 (trapézio [62.5,90,100,100] + centroide)': montar_sistema([62.5, 90, 100, 100], 'centroid'),
    'A2 (trapézio [80,95,100,100] + centroide)': montar_sistema([80, 95, 100, 100], 'centroid'),
    'Abordagem B (triângulo + MOM)': montar_sistema(None, 'mom'),
}

print('\nComparação nos extremos:')
for nome, sim in sistemas.items():
    print('%-46s (0,0) = %6.2f | (100,10) = %6.2f' % (nome, calcular(sim, 0, 0), calcular(sim, 100, 10)))

# Suavidade no meio da escala: varrendo o impacto com explorabilidade fixa em 5
impactos = np.arange(0, 101, 1)
plt.figure(figsize=(9, 5))
print('\nSuavidade (maior salto entre dois pontos vizinhos, explorabilidade = 5):')
for nome, sim in sistemas.items():
    saidas = np.array([calcular(sim, i, 5) for i in impactos])
    print('%-46s maior salto = %.2f' % (nome, np.max(np.abs(np.diff(saidas)))))
    plt.plot(impactos, saidas, label=nome)
plt.xlabel('Impacto (%)')
plt.ylabel('Urgência (%)')
plt.title('Suavidade da saída com Explorabilidade = 5')
plt.legend()
plt.grid(True)
plt.savefig('comparacao_abordagens.png', dpi=150, bbox_inches='tight')


# ------------------------------------------------------------------
# SUPERFÍCIE DE DECISÃO 3D (usando a Abordagem A2)
# ------------------------------------------------------------------
sim3d = sistemas['A2 (trapézio [80,95,100,100] + centroide)']
x = np.arange(0, 101, 4)
y = np.arange(0, 10.1, 0.4)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X, dtype=float)
for a in range(X.shape[0]):
    for b in range(X.shape[1]):
        Z[a, b] = calcular(sim3d, X[a, b], Y[a, b])

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
ax.set_xlabel('Impacto (%)')
ax.set_ylabel('Explorabilidade (0-10)')
ax.set_zlabel('Urgência (%)', labelpad=8)
ax.set_title('Superfície de Decisão - Urgência do Incidente')
fig.colorbar(surf, shrink=0.5, aspect=10)
ax.view_init(30, 225)
plt.savefig('superficie_decisao.png', dpi=150, bbox_inches='tight', pad_inches=0.5)
plt.show()
