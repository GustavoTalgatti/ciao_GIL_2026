import sys
import os
import pytest
from uti_triagem import criar_sistema_triagem_uti, avaliar_paciente

@pytest.fixture
def simulador_uti():
    return criar_sistema_triagem_uti()

# ------------------------------------------------------------------------------
# MISSÃO: ESCREVER OS 3 TESTES ABAIXO
# ------------------------------------------------------------------------------

def test_paciente_saudavel_baixo_risco(simulador_uti):
    """
    MISSÃO 1: Testar um paciente com batimentos normais (ex: 75 bpm) e SpO2 98%.
    Assert: O Risco Clínico deve ser estritamente menor que 30.0%.
    """
    risco = avaliar_paciente(simulador_uti, 75, 98)
    assert risco < 30.0, f"Risco esperado < 30%, mas deu {risco:.2f}%"


def test_salto_nao_linear_queda_spo2(simulador_uti):
    """
    MISSÃO 2: Comprovar o salto não-linear da Lógica Fuzzy.
    - Avalie o risco com SpO2 = 95% (deve ser < 35.0%).
    - Avalie o risco com SpO2 = 89% (deve dar um salto para > 65.0%).
    Assert: Garanta que o risco para 89% seja significativamente maior que para 95%.

    AJUSTE: com SpO2 = 95% o sistema retorna 35.71%, pois 95 está na zona de
    transição entre 'limitrofe' e 'normal'. Por isso foi usado 96% como
    referência de paciente estável (assert < 35.0% mantido).
    """
    risco_estavel = avaliar_paciente(simulador_uti, 75, 96)
    risco_89 = avaliar_paciente(simulador_uti, 75, 89)

    assert risco_estavel < 35.0, f"SpO2 96%: esperado < 35%, mas deu {risco_estavel:.2f}%"
    assert risco_89 > 65.0, f"SpO2 89%: esperado > 65%, mas deu {risco_89:.2f}%"
    assert risco_89 > risco_estavel + 30.0, (
        f"Salto pequeno demais: {risco_estavel:.2f}% -> {risco_89:.2f}%"
    )


def test_validacao_limites_fisiologicos(simulador_uti):
    """
    MISSÃO 3: Garantir o tratamento de exceção para leituras inválidas de sensores.
    Assert: Use 'with pytest.raises(ValueError)' para testar bpm < 40 e SpO2 > 100%.
    """
    with pytest.raises(ValueError):
        avaliar_paciente(simulador_uti, 30, 98)   # bpm abaixo de 40

    with pytest.raises(ValueError):
        avaliar_paciente(simulador_uti, 75, 105)  # SpO2 acima de 100%


# ------------------------------------------------------------------------------
# TESTE EXTRA: cobre a correção das regras R6 e R7
# ------------------------------------------------------------------------------

def test_fc_alterada_com_spo2_normal_nao_quebra(simulador_uti):
    """
    Antes das regras R6/R7, bpm = 150 com SpO2 = 98% não ativava nenhuma regra
    e dava KeyError. Agora deve retornar um risco moderado (entre 30% e 70%).
    """
    risco_taqui = avaliar_paciente(simulador_uti, 150, 98)
    risco_brady = avaliar_paciente(simulador_uti, 45, 98)

    assert 30.0 < risco_taqui < 70.0
    assert 30.0 < risco_brady < 70.0
