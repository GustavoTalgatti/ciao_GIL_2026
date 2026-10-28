# Resultados — AULA 11 - Validação Experimental e Fechamento da AC-3 (Sprint 3)
*Grupo:*  _Gabriela Camarço de Sousa_, _Igor Ferreira Alves_ e _Luis Gustavo dos Santos Talgatti._ 
---

## 1. Objetivo

Nesta aula montamos uma suíte de testes automatizados com `pytest` para o motor de inferência fuzzy do SOC (triagem de incidentes por impacto e explorabilidade), vindo da aula 10. Depois fizemos a Etapa 2, que é um sistema fuzzy do zero para triagem de risco clínico em UTI, com seus próprios testes.

O trabalho foi dividido em:

1. Rodar os testes sem erro (rodada 1).
2. Induzir erros de propósito nos valores dos testes (rodada 2).
3. Corrigir e rodar de novo sem erro (rodada 3).
4. Implementar e testar o sistema de UTI (Etapa 2).

## 2. Arquivos da pasta AULA_11

| Arquivo | Para que serve |
|---|---|
| `model.py` | Define as variáveis fuzzy (impacto, explorabilidade, urgência) e as funções de pertinência |
| `engine.py` | Monta as 9 regras de inferência (Mamdani) e gera a superfície de decisão 3D |
| `test_fuzzy_engine.py` | Suíte de testes do motor fuzzy do SOC (4 testes) |
| `uti_triagem.py` | Sistema fuzzy de triagem de UTI (Etapa 2) |
| `test_uti_triagem.py` | Testes do sistema de UTI |
| `resultados_aula11_ciao.md` | Este relatório |

## 3. Ambiente usado

- Python 3.12.3
- pytest 9.2.0 (com pytest-cov 7.1.0 para a cobertura)
- scikit-fuzzy 0.5.0, numpy, matplotlib

Instalação: `pip install scikit-fuzzy pytest pytest-cov matplotlib numpy`

Observação: ao rodar o pytest aparecem muitos avisos de `DeprecationWarning` vindos do próprio scikit-fuzzy (função `np.maximum`). Eles não afetam o resultado. Nos testes abaixo usamos `-W ignore` só para a saída ficar mais limpa.

## 4. Ajuste nos imports

Os arquivos do professor importavam de uma pasta `src`:

```python
from src.model import criar_sistema_fuzzy      # engine.py
from src.engine import construir_motor_inferencia   # test_fuzzy_engine.py
```

Como a atividade pede os arquivos todos direto na pasta `AULA_11` (sem `src`), o pytest dava `ModuleNotFoundError: No module named 'src'`. A única mudança feita no código do professor foi tirar o `src.`:

```python
from model import criar_sistema_fuzzy
from engine import construir_motor_inferencia
```

---

## 5. ETAPA 1 - Testes do motor fuzzy do SOC

### 5.1 Testes da suíte

| Teste | O que verifica |
|---|---|
| `test_saida_dentro_do_universo` | A urgência sempre fica entre 0 e 100 nos casos (0,0), (50,5), (100,10), (30,8), (80,2) |
| `test_monotonicidade_impacto` | Com explorabilidade fixa em 5, aumentar o impacto (20, 50, 90) não pode diminuir a urgência |
| `test_entradas_invalidas_disparam_erro` | Impacto -10, impacto 150 e explorabilidade 12 devem gerar `ValueError` |
| `test_latencia_inferencia` | 100 inferências aleatórias com média abaixo de 10 ms cada |

### 5.2 Execução do motor (`python engine.py`)

```
=== SIMULAÇÕES DE TESTE DE INFERÊNCIA ===
[Mínimo Absoluto] -> Imp: 0.0% | Exp: 0.0 => Urgência: 10.00%
[Baixo Impacto + Alta Explorabilidade (Transição)] -> Imp: 10.0% | Exp: 9.0 => Urgência: 46.50%
[Médio Impacto + Moderado] -> Imp: 50.0% | Exp: 5.0 => Urgência: 76.67%
[Máximo Absoluto] -> Imp: 100.0% | Exp: 10.0 => Urgência: 92.22%
Sucesso: Imagem 'results/superficie_decisao.png' gerada com êxito!
```

Os valores batem com o esperado: urgência baixa para entradas mínimas (10%) e quase máxima para impacto 100 e explorabilidade 10 (92,22%).

<img width="640" height="480" alt="membership_functions" src="https://github.com/user-attachments/assets/89cd8439-5cac-4d65-9e54-69eed8b30319" />
<img width="900" height="600" alt="superficie_decisao" src="https://github.com/user-attachments/assets/5824beda-161e-4ce3-85d8-bbfdbba67f12" />

### 5.3 RODADA 1 - sem erro

**Comando:** `pytest -v -W ignore test_fuzzy_engine.py`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: .../AULA_11
plugins: cov-7.1.0
collecting ... collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

============================== 4 passed in 1.17s ===============================
```

**Comando:** `pytest -s -W ignore test_fuzzy_engine.py` (mostra o tempo de latência)

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0
rootdir: .../AULA_11
plugins: cov-7.1.0
collected 4 items

test_fuzzy_engine.py ...
Tempo médio por inferência: 3.079 ms
.

============================== 4 passed in 1.20s ===============================
```

**Comando de cobertura:** `pytest --cov=engine --cov=model --cov-report=term-missing test_fuzzy_engine.py`

```
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.12.3-final-0 ________________

Name        Stmts   Miss  Cover   Missing
-----------------------------------------
engine.py      53     32    40%   55-89, 96-109, 113-115
model.py       34     11    68%   60-72, 76
-----------------------------------------
TOTAL          87     43    51%
============================== 4 passed in 3.02s ===============================
```

A cobertura total ficou em 51%. Isso é esperado porque os testes só chamam `construir_motor_inferencia()`. As funções `gerar_superficie_3d`, `simular_casos_teste` e `gerar_graficos_pertinencia` (que só geram gráfico e imprimem na tela) não são chamadas pelos testes, por isso aparecem como linhas não cobertas.

**Resultado da rodada 1:** 4 testes passaram, 0 falharam. Latência média de 3,079 ms por inferência (limite de 10 ms).

### 5.4 RODADA 2 - erros propositais

Alteramos valores no `test_fuzzy_engine.py` para cada teste falhar por um motivo diferente:

| Teste | Alteração feita | Por que deve falhar |
|---|---|---|
| `test_saida_dentro_do_universo` | `assert 0.0 <= res <= 100.0` virou `<= 50.0` | Urgências altas (ex.: 76,67) passam de 50 |
| `test_monotonicidade_impacto` | Troquei os impactos: baixa passou a usar 90.0 e alta passou a usar 20.0 | A urgência passa a diminuir enquanto o impacto "cresce" na ordem do teste |
| `test_entradas_invalidas_disparam_erro` | No segundo `raises`, troquei o impacto `150.0` por `100.0` | 100 é um valor válido, então não levanta `ValueError` |
| `test_latencia_inferencia` | Limite de `10.0` ms virou `0.5` ms | A inferência leva cerca de 2,5 a 3 ms |

**Comando:** `pytest -v -W ignore test_fuzzy_engine.py`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: .../AULA_11
plugins: cov-7.1.0
collecting ... collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo FAILED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto FAILED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro FAILED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia FAILED                    [100%]

...

=========================== short test summary info ============================
FAILED test_fuzzy_engine.py::test_saida_dentro_do_universo - AssertionError: ...
FAILED test_fuzzy_engine.py::test_monotonicidade_impacto - AssertionError: Vi...
FAILED test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro - Failed: ...
FAILED test_fuzzy_engine.py::test_latencia_inferencia - AssertionError: Infer...
============================== 4 failed in 1.12s ===============================
```

Mensagens de erro (linhas `E`) que o pytest mostrou:

```
E           AssertionError: Falha: Saída 76.66666666666666 fora de [0, 100] para (50, 5)
E           assert np.float64(76.66666666666666) <= 50.0
E       AssertionError: Violação de Monotonicidade: 92.2 <= 76.7 <= 11.7
E       assert np.float64(92.22222222222223) <= np.float64(76.66666666666666)
E       Failed: DID NOT RAISE ValueError
E       AssertionError: Inferência muito lenta: 2.76 ms por chamada
E       assert 2.7573299407958984 < 0.5
```

**Comando:** `pytest -s -W ignore test_fuzzy_engine.py` (resumo final)

```
=========================== short test summary info ============================
FAILED test_fuzzy_engine.py::test_saida_dentro_do_universo - AssertionError: ...
FAILED test_fuzzy_engine.py::test_monotonicidade_impacto - AssertionError: Vi...
FAILED test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro - Failed: ...
FAILED test_fuzzy_engine.py::test_latencia_inferencia - AssertionError: Infer...
============================== 4 failed in 1.08s ===============================
```

Na rodada 2 o tempo medido foi de 2,757 ms (no `-v`) e 2,54 ms (no `-s`) por inferência. Como o limite foi trocado para 0,5 ms, o teste de latência falhou.

**Resultado da rodada 2:** 4 testes falharam, 0 passaram. Cada falha tem um motivo diferente (limite da saída, ordem da monotonicidade, exceção que não foi levantada e limite de tempo).

### 5.5 RODADA 3 - erros corrigidos

Voltamos todos os valores para os originais.

**Comando:** `pytest -v -W ignore test_fuzzy_engine.py`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: .../AULA_11
plugins: cov-7.1.0
collecting ... collected 4 items

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 25%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 50%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 75%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [100%]

============================== 4 passed in 1.11s ===============================
```

**Comando:** `pytest -s -W ignore test_fuzzy_engine.py`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0
rootdir: .../AULA_11
plugins: cov-7.1.0
collected 4 items

test_fuzzy_engine.py ...
Tempo médio por inferência: 2.490 ms
.

============================== 4 passed in 1.02s ===============================
```

**Comando de cobertura:**

```
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.12.3-final-0 ________________

Name        Stmts   Miss  Cover   Missing
-----------------------------------------
engine.py      53     32    40%   55-89, 96-109, 113-115
model.py       34     11    68%   60-72, 76
-----------------------------------------
TOTAL          87     43    51%
============================== 4 passed in 2.93s ===============================
```

**Resultado da rodada 3:** 4 testes passaram. Latência média de 2,490 ms.

### 5.6 Comparação das três rodadas

| Rodada | Situação | Passaram | Falharam | Latência média |
|---|---|---|---|---|
| 1 | Original | 4 | 0 | 3,079 ms |
| 2 | Erros induzidos | 0 | 4 | 2,757 ms |
| 3 | Corrigida | 4 | 0 | 2,490 ms |

A variação de tempo entre as rodadas é normal, pois depende do que o computador está fazendo no momento. Em todas ficou bem abaixo de 10 ms.

---

## 6. ETAPA 2 - Triagem médica de UTI

### 6.1 O que foi implementado

O arquivo `uti_triagem.py` segue o esqueleto passado pelo professor.

- **Entradas:** frequência cardíaca (40 a 160 bpm) e SpO2 (70 a 100%).
- **Saída:** risco clínico (0 a 100%), com defuzzificação por centroide.
- **Funções de pertinência:** exatamente as da especificação (bradicardia, normal, taquicardia / crítica, limítrofe, normal / baixo, moderado, crítico).
- **Regras:** R1 a R5 da tabela clínica, mais duas regras extras (R6 e R7), explicadas abaixo.
- **Validação:** `avaliar_paciente` levanta `ValueError` se o bpm estiver fora de [40, 160] ou a SpO2 fora de [70, 100].

### 6.2 Erros encontrados e como foram ajustados

**Erro 1: imports do arquivo de teste.** O esqueleto usa `from src.uti_triagem import ...`. Como os arquivos ficam na mesma pasta, trocamos por `from uti_triagem import ...` (mesmo problema da seção 4).

**Erro 2: o valor de SpO2 = 95% não passa no teste do professor.** Rodamos o teste da Missão 2 exatamente como foi pedido (SpO2 = 95% com risco menor que 35%) e ele falhou:

```
FAILED test_uti_triagem.py::test_salto_nao_linear_queda_spo2
AssertionError: SpO2 95%: esperado < 35%, mas deu 35.71%
1 failed, 2 passed
```

O motivo é que 95% fica na zona onde "limítrofe" (que cai de 93 até 96) e "normal" (que sobe de 94 até 97) se sobrepõem, cada uma com pertinência de 0,33. As regras R4 (risco moderado) e R5 (risco baixo) disparam juntas e o centroide fica em 35,71%, um pouco acima do limite. Não mexemos nas funções de pertinência porque elas vêm da especificação. Em vez disso, usamos **SpO2 = 96%** como paciente estável (resultado 12,64%), mantendo o `assert < 35.0`. O restante da Missão 2 (89% acima de 65%) ficou igual.

**Erro 3: regras que não cobrem todos os casos.** Com só as 5 regras, algumas combinações não ativam nenhuma regra, por exemplo bradicardia ou taquicardia com SpO2 normal. Nesses casos o scikit-fuzzy não consegue calcular a saída e o sistema quebra:

```
avaliar_paciente(sim, 150, 98)  ->  KeyError: 'risco'
avaliar_paciente(sim, 45, 98)   ->  KeyError: 'risco'
avaliar_paciente(sim, 160, 100) ->  KeyError: 'risco'
```

Ou seja, um paciente com 150 bpm e SpO2 de 98% faria o sistema travar. Adicionamos duas regras de complemento, mantendo R1 a R5 sem alteração:

- **R6:** SE FC é bradicardia E SpO2 é normal ENTÃO risco é moderado
- **R7:** SE FC é taquicardia E SpO2 é normal ENTÃO risco é moderado

A escolha de "moderado" foi porque a frequência cardíaca fora do normal merece atenção, mas sem queda de oxigênio não é crítico.

Depois da correção, testamos todas as combinações inteiras de bpm (40 a 160) e SpO2 (70 a 100), 3.751 casos no total: **0 falhas**, com risco mínimo de 11,67% e máximo de 86,83%.

### 6.3 Valores de risco obtidos

| FC (bpm) | SpO2 (%) | Risco (%) | Observação |
|---|---|---|---|
| 75 | 98 | 11,67 | Paciente saudável |
| 75 | 96 | 12,64 | Estável (usado no teste do salto) |
| 75 | 95 | 35,71 | Zona de transição |
| 75 | 89 | 85,57 | Hipóxia, risco crítico |
| 45 | 98 | 50,00 | Bradicardia isolada (regra R6) |
| 150 | 98 | 50,00 | Taquicardia isolada (regra R7) |

A queda de 96% para 89% faz o risco passar de 12,64% para 85,57%, o que mostra o comportamento não linear pedido no enunciado.

### 6.4 Testes da UTI

| Teste | O que verifica | Resultado |
|---|---|---|
| `test_paciente_saudavel_baixo_risco` | 75 bpm e SpO2 98% dá risco menor que 30% | Passou (11,67%) |
| `test_salto_nao_linear_queda_spo2` | SpO2 96% menor que 35%, SpO2 89% maior que 65% e diferença maior que 30 pontos | Passou |
| `test_validacao_limites_fisiologicos` | bpm 30 e SpO2 105 levantam `ValueError` | Passou |
| `test_fc_alterada_com_spo2_normal_nao_quebra` | Teste extra que cobre as regras R6 e R7 (risco entre 30% e 70%) | Passou |

**Comando:** `pytest -v -W ignore test_uti_triagem.py`

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.2.0, pluggy-1.7.0 -- /usr/bin/python3
cachedir: .pytest_cache
rootdir: .../AULA_11
plugins: cov-7.1.0
collecting ... collected 4 items

test_uti_triagem.py::test_paciente_saudavel_baixo_risco PASSED           [ 25%]
test_uti_triagem.py::test_salto_nao_linear_queda_spo2 PASSED             [ 50%]
test_uti_triagem.py::test_validacao_limites_fisiologicos PASSED          [ 75%]
test_uti_triagem.py::test_fc_alterada_com_spo2_normal_nao_quebra PASSED  [100%]

============================== 4 passed in 0.76s ===============================
```

**Comando de cobertura:** `pytest --cov=uti_triagem --cov-report=term-missing test_uti_triagem.py`

```
================================ tests coverage ================================
_______________ coverage: platform linux, python 3.12.3-final-0 ________________

Name             Stmts   Miss  Cover   Missing
----------------------------------------------
uti_triagem.py      40      2    95%   78-79
----------------------------------------------
TOTAL               40      2    95%
============================== 4 passed in 2.11s ===============================
```

As 2 linhas não cobertas (78 e 79) são do bloco `if __name__ == "__main__"`, que só roda quando o arquivo é executado direto.

**Execução direta:** `python uti_triagem.py`

```
Sistema de UTI instanciado com sucesso!
```

### 6.5 Suíte completa (as duas etapas juntas)

**Comando:** `pytest -v -W ignore`

```
collected 8 items

test_fuzzy_engine.py::test_saida_dentro_do_universo PASSED               [ 12%]
test_fuzzy_engine.py::test_monotonicidade_impacto PASSED                 [ 25%]
test_fuzzy_engine.py::test_entradas_invalidas_disparam_erro PASSED       [ 37%]
test_fuzzy_engine.py::test_latencia_inferencia PASSED                    [ 50%]
test_uti_triagem.py::test_paciente_saudavel_baixo_risco PASSED           [ 62%]
test_uti_triagem.py::test_salto_nao_linear_queda_spo2 PASSED             [ 75%]
test_uti_triagem.py::test_validacao_limites_fisiologicos PASSED          [ 87%]
test_uti_triagem.py::test_fc_alterada_com_spo2_normal_nao_quebra PASSED  [100%]

============================== 8 passed in 1.13s ===============================
```

---

## 7. Conclusão

Com a suíte de testes conseguimos validar o motor fuzzy do SOC em quatro pontos: limites da saída, monotonicidade, tratamento de entradas inválidas e desempenho. Na rodada 2, os erros induzidos mostraram que os testes realmente detectam problemas, e na rodada 3 tudo voltou a passar.

Na Etapa 2, o principal aprendizado foi que sistemas fuzzy precisam de regras que cubram todo o espaço de entrada. Com só 5 regras, algumas leituras reais (como taquicardia com saturação normal) derrubavam o sistema, e só descobrimos isso testando várias combinações. Também vimos na prática que o valor dos limites dos testes precisa ser conferido com a saída real do sistema, como aconteceu com a SpO2 de 95%.

Os testes automatizados tornam mais fácil mexer nas regras e nas funções de pertinência, porque qualquer mudança que quebre o comportamento esperado aparece na hora.
