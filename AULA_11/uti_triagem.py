import sys
import os
import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

def criar_sistema_triagem_uti():
    """
    Cria o sistema fuzzy de triagem de risco clínico para UTI.
    Entradas: frequência cardíaca (40-160 bpm) e SpO2 (70-100%).
    Saída: risco clínico (0-100%).
    """
    # 1. Antecedentes e consequente (universos do discurso)
    freq_cardiaca = ctrl.Antecedent(np.arange(40, 161, 1), 'freq_cardiaca')
    spo2 = ctrl.Antecedent(np.arange(70, 101, 1), 'spo2')
    risco = ctrl.Consequent(np.arange(0, 101, 1), 'risco')

    # 2. Método de defuzzificação
    risco.defuzzify_method = 'centroid'

    # 3. Funções de pertinência (conforme a especificação)
    # Frequência Cardíaca
    freq_cardiaca['bradicardia'] = fuzzy.trimf(freq_cardiaca.universe, [40, 40, 60])
    freq_cardiaca['normal'] = fuzzy.trimf(freq_cardiaca.universe, [50, 75, 100])
    freq_cardiaca['taquicardia'] = fuzzy.trapmf(freq_cardiaca.universe, [90, 110, 160, 160])

    # Saturação de Oxigênio
    spo2['critica'] = fuzzy.trapmf(spo2.universe, [70, 70, 88, 91])
    spo2['limitrofe'] = fuzzy.trimf(spo2.universe, [89, 93, 96])
    spo2['normal'] = fuzzy.trapmf(spo2.universe, [94, 97, 100, 100])

    # Risco Clínico
    risco['baixo'] = fuzzy.trimf(risco.universe, [0, 0, 35])
    risco['moderado'] = fuzzy.trimf(risco.universe, [25, 50, 75])
    risco['critico'] = fuzzy.trapmf(risco.universe, [65, 85, 100, 100])

    # 4. Regras clínicas
    r1 = ctrl.Rule(spo2['critica'], risco['critico'])
    r2 = ctrl.Rule(freq_cardiaca['bradicardia'] & spo2['limitrofe'], risco['critico'])
    r3 = ctrl.Rule(freq_cardiaca['taquicardia'] & spo2['limitrofe'], risco['critico'])
    r4 = ctrl.Rule(freq_cardiaca['normal'] & spo2['limitrofe'], risco['moderado'])
    r5 = ctrl.Rule(freq_cardiaca['normal'] & spo2['normal'], risco['baixo'])

    # Regras extras (correção): as 5 regras da especificação não cobriam
    # FC alterada com SpO2 normal. Nesses casos nenhuma regra disparava e o
    # sistema dava KeyError. Foi definido risco moderado (FC fora do normal
    # pede atenção, mas sem hipóxia).
    r6 = ctrl.Rule(freq_cardiaca['bradicardia'] & spo2['normal'], risco['moderado'])
    r7 = ctrl.Rule(freq_cardiaca['taquicardia'] & spo2['normal'], risco['moderado'])

    # 5. Sistema de controle e simulador
    sistema = ctrl.ControlSystem([r1, r2, r3, r4, r5, r6, r7])
    return ctrl.ControlSystemSimulation(sistema)


def avaliar_paciente(simulador, bpm, spo2_val):
    """
    Valida as leituras dos sensores, executa a inferência e retorna o risco clínico (%).
    """
    # 1. Validação da frequência cardíaca
    if not (40 <= bpm <= 160):
        raise ValueError(f"Frequência cardíaca fora da faixa [40, 160] bpm: {bpm}")

    # 2. Validação da saturação de oxigênio
    if not (70 <= spo2_val <= 100):
        raise ValueError(f"SpO2 fora da faixa [70, 100]%: {spo2_val}")

    # 3. Entradas e cálculo
    simulador.input['freq_cardiaca'] = bpm
    simulador.input['spo2'] = spo2_val
    simulador.compute()

    # 4. Saída
    return simulador.output['risco']

if __name__ == "__main__":
    # Teste rápido manual em tela
    sim = criar_sistema_triagem_uti()
    print("Sistema de UTI instanciado com sucesso!")
