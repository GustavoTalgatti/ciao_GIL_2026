# Resultados — Aula 12 — Otimização Multiobjetivo e NSGA-II (AC-4 Sprint 1) — CIAO
*Grupo:*  _Gabriela Camarço de Sousa_, _Igor Ferreira Alves_ e _Luis Gustavo dos Santos Talgatti._ 
---

Neste trabalho executamos os 7 exercícios do laboratório usando Python e a biblioteca pymoo. Em todos os problemas existem objetivos que brigam entre si (melhorar um piora o outro), então o NSGA-II não devolve uma única resposta e sim um conjunto de soluções não dominadas, que é a aproximação da Fronteira de Pareto. Os códigos dos exercícios 1 a 6 são os mesmos do professor. Só completamos os TODOs e acrescentamos algumas linhas de `print` e `savefig` no final para mostrar os resultados e salvar os gráficos.

**Como rodar:** `pip install pymoo matplotlib` e depois `python exercicio_1.py` (e assim por diante).

---

## Exercício 1 — Compra de Servidores Cloud

**Objetivo:** Mostrar uma Fronteira de Pareto simples com dois objetivos opostos: custo e latência.

**Como resolvemos:** Usamos o código do professor sem alterar a lógica. O custo é 15 reais por vCPU e a latência é 300/vCPUs. Só adicionamos o `savefig` e o print dos resultados.

### Código

```python
import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class CloudProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(n_var=1, n_obj=2, xl=np.array([1.0]), xu=np.array([32.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        vcpus = x[0]
        f1_custo = vcpus * 15.0         # R$ 15 por vCPU
        f2_latencia = 300.0 / vcpus     # Latência cai com mais vCPUs
        out["F"] = [f1_custo, f2_latencia]

res1 = minimize(CloudProblem(), NSGA2(pop_size=20), termination=('n_gen', 30), seed=1)

# Visualização
plt.figure(figsize=(7, 4))
plt.scatter(res1.F[:, 0], res1.F[:, 1], color='blue', s=50)
plt.title("Exercício 1 — Fronteira de Pareto: Cloud")
plt.xlabel("Custo (R$) [Minimizar]")
plt.ylabel("Latência (ms) [Minimizar]")
plt.grid(True)
plt.savefig("imagens/exercicio_1.png", dpi=120, bbox_inches="tight")
plt.show()

# Resultados no console
print("Soluções não dominadas:", len(res1.F))
idx = np.argsort(res1.F[:, 0])
for i in idx:
    print(f"vCPUs: {res1.X[i][0]:6.2f} | Custo: R$ {res1.F[i][0]:7.2f} | Latência: {res1.F[i][1]:6.2f} ms")
```

### Resultado no console

```
Soluções não dominadas: 20
vCPUs:   1.00 | Custo: R$   15.00 | Latência: 300.00 ms
vCPUs:   1.06 | Custo: R$   15.93 | Latência: 282.45 ms
vCPUs:   1.23 | Custo: R$   18.41 | Latência: 244.37 ms
vCPUs:   1.37 | Custo: R$   20.60 | Latência: 218.47 ms
vCPUs:   1.41 | Custo: R$   21.10 | Latência: 213.25 ms
vCPUs:   1.65 | Custo: R$   24.73 | Latência: 181.99 ms
vCPUs:   1.88 | Custo: R$   28.22 | Latência: 159.48 ms
vCPUs:   3.65 | Custo: R$   54.70 | Latência:  82.27 ms
vCPUs:   5.00 | Custo: R$   74.99 | Latência:  60.01 ms
vCPUs:   5.50 | Custo: R$   82.53 | Latência:  54.52 ms
vCPUs:   7.19 | Custo: R$  107.78 | Latência:  41.75 ms
vCPUs:   9.29 | Custo: R$  139.32 | Latência:  32.30 ms
vCPUs:  14.68 | Custo: R$  220.24 | Latência:  20.43 ms
vCPUs:  17.51 | Custo: R$  262.67 | Latência:  17.13 ms
vCPUs:  18.68 | Custo: R$  280.27 | Latência:  16.06 ms
vCPUs:  21.00 | Custo: R$  315.04 | Latência:  14.28 ms
vCPUs:  22.63 | Custo: R$  339.52 | Latência:  13.25 ms
vCPUs:  25.51 | Custo: R$  382.64 | Latência:  11.76 ms
vCPUs:  29.49 | Custo: R$  442.42 | Latência:  10.17 ms
vCPUs:  32.00 | Custo: R$  480.00 | Latência:   9.38 ms
```

### Gráfico

<img width="756" height="481" alt="exercicio_1" src="https://github.com/user-attachments/assets/3e2dc748-34ca-45a7-b7ce-2ce229ae7144" />

### Análise

Os 20 pontos formam uma curva descendente. Com 1 vCPU o custo é o menor (R$ 15,00), mas a latência é a maior (300 ms). Com 32 vCPUs a latência cai para 9,38 ms, mas o custo sobe para R$ 480,00. Nenhum ponto é melhor que outro nos dois objetivos ao mesmo tempo, por isso todos fazem parte da fronteira. A escolha final depende do que a empresa prioriza.

---

## Exercício 2 — Triagem de Incidentes SOC

**Objetivo:** Completar a classe do problema e os objetivos do SOC Autônomo.

**Como resolvemos:** Preenchemos os TODOs: custo = analistas × 100 + regimento × 50 e tempo de resposta = 200 / analistas + 50 / regimento. Depois criamos o NSGA2 com `pop_size=30` e rodamos 40 gerações. As variáveis (TODO 1 e 2) já estavam configuradas no esqueleto: 2 variáveis e 2 objetivos.

### Código

```python
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
```

### Resultado no console

```
Soluções não dominadas: 30
Analistas:  1.01 | Regimento:  1.01 | Custo: R$   151.60 | Tempo: 247.16 min
Analistas:  1.10 | Regimento:  1.03 | Custo: R$   161.15 | Tempo: 230.88 min
Analistas:  1.16 | Regimento:  1.16 | Custo: R$   174.25 | Tempo: 215.12 min
Analistas:  1.16 | Regimento:  1.40 | Custo: R$   185.74 | Tempo: 208.45 min
Analistas:  1.35 | Regimento:  1.03 | Custo: R$   185.97 | Tempo: 197.27 min
Analistas:  1.29 | Regimento:  1.61 | Custo: R$   209.08 | Tempo: 186.48 min
Analistas:  1.61 | Regimento:  1.02 | Custo: R$   211.78 | Tempo: 173.37 min
Analistas:  1.78 | Regimento:  1.16 | Custo: R$   235.68 | Tempo: 155.66 min
Analistas:  1.76 | Regimento:  1.75 | Custo: R$   263.19 | Tempo: 142.43 min
Analistas:  2.22 | Regimento:  1.34 | Custo: R$   289.01 | Tempo: 127.40 min
Analistas:  3.36 | Regimento:  1.16 | Custo: R$   394.28 | Tempo: 102.68 min
Analistas:  2.95 | Regimento:  2.31 | Custo: R$   410.35 | Tempo:  89.48 min
Analistas:  4.84 | Regimento:  1.41 | Custo: R$   554.81 | Tempo:  76.78 min
Analistas:  5.54 | Regimento:  2.52 | Custo: R$   680.52 | Tempo:  55.89 min
Analistas:  7.23 | Regimento:  2.14 | Custo: R$   830.47 | Tempo:  51.00 min
Analistas:  6.52 | Regimento:  9.17 | Custo: R$  1110.67 | Tempo:  36.11 min
Analistas:  6.91 | Regimento:  9.57 | Custo: R$  1169.22 | Tempo:  34.18 min
Analistas: 10.39 | Regimento:  9.70 | Custo: R$  1523.90 | Tempo:  24.41 min
Analistas: 14.93 | Regimento:  9.82 | Custo: R$  1984.33 | Tempo:  18.48 min
Analistas: 18.56 | Regimento:  8.77 | Custo: R$  2294.29 | Tempo:  16.48 min
Analistas: 22.22 | Regimento:  9.94 | Custo: R$  2718.76 | Tempo:  14.03 min
Analistas: 26.31 | Regimento:  9.81 | Custo: R$  3122.05 | Tempo:  12.70 min
Analistas: 29.16 | Regimento:  9.99 | Custo: R$  3415.14 | Tempo:  11.87 min
Analistas: 31.29 | Regimento:  9.55 | Custo: R$  3606.25 | Tempo:  11.63 min
Analistas: 36.39 | Regimento:  9.54 | Custo: R$  4116.50 | Tempo:  10.74 min
Analistas: 39.76 | Regimento:  9.97 | Custo: R$  4474.64 | Tempo:  10.05 min
Analistas: 43.78 | Regimento:  9.36 | Custo: R$  4845.57 | Tempo:   9.91 min
Analistas: 43.78 | Regimento:  9.77 | Custo: R$  4866.37 | Tempo:   9.69 min
Analistas: 48.65 | Regimento:  9.97 | Custo: R$  5363.33 | Tempo:   9.12 min
Analistas: 49.99 | Regimento: 10.00 | Custo: R$  5499.11 | Tempo:   9.00 min
```

### Análise

Foram encontradas 30 soluções não dominadas. A mais barata usa cerca de 1 analista e 1 regimento (R$ 151,60), mas leva 247 minutos para responder. A mais rápida usa 50 analistas e 10 regimentos (R$ 5.499,11) e responde em 9 minutos. Dá para notar que no começo da fronteira um pequeno aumento de custo reduz muito o tempo, e no final gastar bastante mais traz pouca melhora. Um ponto intermediário, como 7,23 analistas (R$ 830,47 e 51 min), parece um bom equilíbrio.

---

## Exercício 3 — Logística de Drones

**Objetivo:** Otimizar 3 objetivos ao mesmo tempo: tempo de entrega, custo e pegada de carbono.

**Como resolvemos:** Usamos o código do professor. O gráfico é 3D, com um eixo para cada objetivo. Adicionamos o print dos pontos extremos para facilitar a leitura.

### Código

```python
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
```

### Resultado no console

```
Soluções não dominadas: 40
Menor tempo  : vel=80.00 carga=1.24 [ 12.5  702.02  96.74]
Menor custo  : vel=10.00 carga=1.00 [100.  60.  15.]
Menor CO2    : vel=10.00 carga=5.00 [100. 260.   3.]
```

### Gráfico

<img width="632" height="615" alt="exercicio_3" src="https://github.com/user-attachments/assets/54321640-18dd-418a-9151-b3c4e3d126c1" />

### Análise

Com três objetivos a fronteira vira uma superfície e todos os 40 pontos ficaram não dominados. O menor tempo (12,5) acontece com velocidade máxima de 80, mas o custo sobe para 702 e o CO2 para 96,74. O menor custo e o menor CO2 acontecem com velocidade baixa (10). A diferença entre os dois é a carga: carga 1 dá o menor custo (60) e carga 5 dá o menor CO2 (3,0) com custo maior (260). Ou seja, não existe configuração que seja a melhor nos três critérios.

---

## Exercício 4 — Seleção de Portfólio de Investimentos

**Objetivo:** Implementar os objetivos de risco e retorno de um portfólio.

**Como resolvemos:** No TODO 1 o retorno foi multiplicado por -1, porque o pymoo só minimiza (assim, minimizar o retorno negativo equivale a maximizar o retorno). No TODO 2 usamos a fórmula do risco. No gráfico, revertemos o sinal para mostrar o retorno real no eixo Y e o risco no eixo X.

### Código

```python
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
```

### Resultado no console

```
Soluções não dominadas: 40
Renda Fixa:   0.01% | Ações:   0.00% | Risco:    0.00 | Retorno:    0.00
Renda Fixa:   1.40% | Ações:   0.00% | Risco:    0.03 | Retorno:    0.11
Renda Fixa:  19.52% | Ações:   0.01% | Risco:    0.39 | Retorno:    1.56
Renda Fixa:  22.28% | Ações:   1.38% | Risco:    0.79 | Retorno:    2.03
Renda Fixa:  51.91% | Ações:   0.02% | Risco:    1.04 | Retorno:    4.16
Renda Fixa:  55.11% | Ações:   0.47% | Risco:    1.22 | Retorno:    4.49
Renda Fixa:  69.37% | Ações:   0.00% | Risco:    1.39 | Retorno:    5.55
Renda Fixa:  70.87% | Ações:   0.00% | Risco:    1.42 | Retorno:    5.67
Renda Fixa:  85.45% | Ações:   0.09% | Risco:    1.73 | Retorno:    6.85
Renda Fixa:  91.72% | Ações:   0.09% | Risco:    1.86 | Retorno:    7.35
```

### Gráfico

<img width="734" height="481" alt="exercicio_4" src="https://github.com/user-attachments/assets/a630b761-3281-4f74-90b7-db2e4dce636d" />

### Análise

O gráfico mostra que quanto maior o retorno, maior o risco. Os pontos encontrados usam quase só renda fixa e ações perto de 0%. Isso acontece por causa das fórmulas do exercício: a renda fixa dá 0,08 de retorno para 0,02 de risco, enquanto as ações dão 0,18 de retorno para 0,25 de risco, então a renda fixa tem uma relação retorno/risco bem melhor neste modelo. Como não há restrição de soma (por exemplo, 100% investido), o algoritmo também aceita soluções com pouco investimento (retorno e risco próximos de zero). Em um caso real seria preciso incluir essa restrição.

---

## Exercício 5 — Trade-off de Modelos de Machine Learning

**Objetivo:** Escolher hiperparâmetros minimizando o erro de predição e o tempo de inferência.

**Como resolvemos:** Usamos o código do professor sem alterações na lógica, apenas com `savefig` e print.

### Código

```python
import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class MLTuningProblem(ElementwiseProblem):
    def __init__(self):
        # x1: Profundidade da Árvore (1 a 30), x2: Número de Estimadores (10 a 200)
        super().__init__(n_var=2, n_obj=2, xl=np.array([1.0, 10.0]), xu=np.array([30.0, 200.0]))

    def _evaluate(self, x, out, *args, **kwargs):
        depth, n_trees = x[0], x[1]
        f1_erro = 0.5 / (depth * np.log10(n_trees))   # Erro cai com mais árvores/profundidade
        f2_latencia_ms = (depth * 0.2) + (n_trees * 0.5) # Latência sobe
        out["F"] = [f1_erro, f2_latencia_ms]

res5 = minimize(MLTuningProblem(), NSGA2(pop_size=30), termination=('n_gen', 40), seed=7)

plt.figure(figsize=(7, 4))
plt.scatter(res5.F[:, 0], res5.F[:, 1], color='purple', s=45)
plt.title("Exercício 5 — Erro vs. Tempo de Inferência (ML)")
plt.xlabel("Erro do Modelo [Minimizar]")
plt.ylabel("Tempo de Resposta (ms) [Minimizar]")
plt.grid(True)
plt.savefig("imagens/exercicio_5.png", dpi=120, bbox_inches="tight")
plt.show()

# Resultados no console
print("Soluções não dominadas:", len(res5.F))
idx = np.argsort(res5.F[:, 0])
for i in idx[:10]:
    print(f"Profundidade: {res5.X[i][0]:5.2f} | Árvores: {res5.X[i][1]:6.2f} | Erro: {res5.F[i][0]:.4f} | Latência: {res5.F[i][1]:7.2f} ms")
```

### Resultado no console

```
Soluções não dominadas: 30
Profundidade: 30.00 | Árvores: 199.90 | Erro: 0.0072 | Latência:  105.95 ms
Profundidade: 30.00 | Árvores: 186.15 | Erro: 0.0073 | Latência:   99.08 ms
Profundidade: 30.00 | Árvores: 173.20 | Erro: 0.0074 | Latência:   92.60 ms
Profundidade: 29.35 | Árvores: 169.01 | Erro: 0.0076 | Latência:   90.38 ms
Profundidade: 30.00 | Árvores: 151.23 | Erro: 0.0076 | Latência:   81.61 ms
Profundidade: 29.99 | Árvores: 135.73 | Erro: 0.0078 | Latência:   73.86 ms
Profundidade: 29.99 | Árvores: 129.52 | Erro: 0.0079 | Latência:   70.76 ms
Profundidade: 29.81 | Árvores: 115.28 | Erro: 0.0081 | Latência:   63.60 ms
Profundidade: 30.00 | Árvores: 107.85 | Erro: 0.0082 | Latência:   59.93 ms
Profundidade: 30.00 | Árvores:  99.35 | Erro: 0.0083 | Latência:   55.68 ms
```

### Gráfico

<img width="741" height="481" alt="exercicio_5" src="https://github.com/user-attachments/assets/c7ba8087-f984-446e-ab8a-713bfbd01853" />

### Análise

O erro diminui quando aumentamos a profundidade e o número de árvores, mas a latência aumenta. Nos resultados a profundidade ficou perto de 30 em quase todas as soluções, e o que mais varia é o número de árvores: com ~200 árvores o erro é 0,0072 e a latência é 105,95 ms; com ~99 árvores o erro é 0,0083 e a latência cai para 55,68 ms. Isso mostra que dobrar a quantidade de árvores melhora muito pouco o erro, mas dobra o tempo de resposta.

---

## Exercício 6 — Desafio Integrado com Restrições

**Objetivo:** Aplicar uma restrição de desigualdade (G ≤ 0) em um problema de recarga de bateria de veículo elétrico.

**Como resolvemos:** Mudamos `n_ieq_constr=0` para `n_ieq_constr=1` (TODO 1), criamos `g1 = f2_desgaste_bateria - 1500.0` (TODO 2) e passamos com `out["G"] = [g1]` (TODO 3). No TODO 4 rodamos o NSGA-II e imprimimos só as soluções com G ≤ 0.

### Código

```python
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
```

### Resultado no console

```
Soluções viáveis: 40
Potência: 150.00 kW | Temp: 15.00 °C | Tempo recarga:  20.00 | Desgaste: 1377.85
Potência: 147.50 kW | Temp: 15.00 °C | Tempo recarga:  20.34 | Desgaste: 1343.57
Potência: 144.74 kW | Temp: 15.00 °C | Tempo recarga:  20.73 | Desgaste: 1305.99
Potência: 142.47 kW | Temp: 15.00 °C | Tempo recarga:  21.06 | Desgaste: 1275.45
Potência: 139.02 kW | Temp: 15.00 °C | Tempo recarga:  21.58 | Desgaste: 1229.34
Potência: 136.64 kW | Temp: 15.00 °C | Tempo recarga:  21.96 | Desgaste: 1197.92
Potência: 131.42 kW | Temp: 15.00 °C | Tempo recarga:  22.83 | Desgaste: 1130.02
Potência: 128.70 kW | Temp: 15.00 °C | Tempo recarga:  23.31 | Desgaste: 1095.10
Potência: 123.85 kW | Temp: 15.00 °C | Tempo recarga:  24.22 | Desgaste: 1033.71
Potência: 119.38 kW | Temp: 15.04 °C | Tempo recarga:  25.13 | Desgaste:  981.15
Potência: 117.29 kW | Temp: 15.04 °C | Tempo recarga:  25.58 | Desgaste:  955.58
Potência: 110.67 kW | Temp: 15.06 °C | Tempo recarga:  27.11 | Desgaste:  876.48
Potência: 105.64 kW | Temp: 15.02 °C | Tempo recarga:  28.40 | Desgaste:  815.45
Potência: 100.61 kW | Temp: 15.00 °C | Tempo recarga:  29.82 | Desgaste:  756.88
Potência:  94.18 kW | Temp: 15.01 °C | Tempo recarga:  31.85 | Desgaste:  685.99
Potência:  88.59 kW | Temp: 15.00 °C | Tempo recarga:  33.87 | Desgaste:  625.37
Potência:  86.27 kW | Temp: 15.00 °C | Tempo recarga:  34.78 | Desgaste:  600.96
Potência:  81.04 kW | Temp: 15.02 °C | Tempo recarga:  37.02 | Desgaste:  547.74
Potência:  78.17 kW | Temp: 15.01 °C | Tempo recarga:  38.38 | Desgaste:  518.75
Potência:  66.71 kW | Temp: 15.00 °C | Tempo recarga:  44.97 | Desgaste:  408.61
Potência:  60.40 kW | Temp: 15.00 °C | Tempo recarga:  49.67 | Desgaste:  352.08
Potência:  52.17 kW | Temp: 16.76 °C | Tempo recarga:  57.50 | Desgaste:  315.84
Potência:  49.04 kW | Temp: 15.00 °C | Tempo recarga:  61.17 | Desgaste:  257.56
Potência:  44.54 kW | Temp: 15.00 °C | Tempo recarga:  67.36 | Desgaste:  222.90
Potência:  34.92 kW | Temp: 15.00 °C | Tempo recarga:  85.91 | Desgaste:  154.77
Potência:  30.00 kW | Temp: 15.00 °C | Tempo recarga: 100.00 | Desgaste:  123.23
Potência:  27.33 kW | Temp: 15.63 °C | Tempo recarga: 109.75 | Desgaste:  111.72
Potência:  24.21 kW | Temp: 15.00 °C | Tempo recarga: 123.91 | Desgaste:   89.35
Potência:  22.15 kW | Temp: 15.00 °C | Tempo recarga: 135.44 | Desgaste:   78.18
Potência:  18.54 kW | Temp: 15.00 °C | Tempo recarga: 161.81 | Desgaste:   59.88
Potência:  18.08 kW | Temp: 15.00 °C | Tempo recarga: 165.97 | Desgaste:   57.64
Potência:  16.94 kW | Temp: 15.00 °C | Tempo recarga: 177.11 | Desgaste:   52.29
Potência:  15.88 kW | Temp: 15.00 °C | Tempo recarga: 188.96 | Desgaste:   47.45
Potência:  15.42 kW | Temp: 15.00 °C | Tempo recarga: 194.55 | Desgaste:   45.42
Potência:  14.53 kW | Temp: 15.00 °C | Tempo recarga: 206.54 | Desgaste:   41.52
Potência:  13.81 kW | Temp: 15.00 °C | Tempo recarga: 217.23 | Desgaste:   38.50
Potência:  12.88 kW | Temp: 15.00 °C | Tempo recarga: 232.84 | Desgaste:   34.69
Potência:  12.23 kW | Temp: 15.05 °C | Tempo recarga: 245.27 | Desgaste:   32.18
Potência:  11.07 kW | Temp: 15.00 °C | Tempo recarga: 271.08 | Desgaste:   27.61
Potência:  10.00 kW | Temp: 15.00 °C | Tempo recarga: 300.00 | Desgaste:   23.72
```

### Análise

Todas as 40 soluções encontradas são viáveis (desgaste abaixo de 1500). A temperatura ficou quase sempre em 15 °C, que é o limite mínimo, porque temperatura menor reduz o desgaste sem prejudicar o tempo de recarga. A solução mais rápida usa 150 kW e leva 20 minutos, com desgaste de 1377,85, ainda dentro do limite. Já a mais lenta usa 10 kW e leva 300 minutos, com desgaste de apenas 23,72. Observamos que, com essa faixa de variáveis, a restrição não chegou a ser ultrapassada, mas ela continua importante para garantir a segurança do modelo.

---

## Exercício 7 — Dimensionamento de Frota de Robôs de Logística

**Objetivo:** Criar do zero uma classe de otimização multiobjetivo (arquivo `frota_robos_problem.py`) para dimensionar uma frota de robôs.

**Modelagem:**

- Variáveis: x1 = número de robôs [5, 50] e x2 = velocidade média [1,0, 4,0] m/s.
- Objetivo 1 (minimizar): custo f1 = (x1 × 25,0) + (x2² × 8,0).
- Objetivo 2 (minimizar): tempo de ciclo f2 = 120 / x1 + 40 / x2.
- Restrição: consumo C = x1 × x2^1,5 não pode passar de 120, escrita como g1 = C − 120 ≤ 0.
- Algoritmo: NSGA-II com população de 40 e 60 gerações.
- Para escolher as 3 soluções, pegamos o menor custo, o menor tempo e a solução intermediária (a mais próxima do meio da fronteira depois de normalizar os valores entre 0 e 1).

### Código

```python
import matplotlib
matplotlib.use("Agg")
import numpy as np
import matplotlib.pyplot as plt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize


class FrotaRobosProblem(ElementwiseProblem):
    def __init__(self):
        # x1: número de robôs [5, 50] | x2: velocidade média [1.0, 4.0] m/s
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=1,
            xl=np.array([5.0, 1.0]),
            xu=np.array([50.0, 4.0])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        x1, x2 = x[0], x[1]

        # Objetivo 1: custo total (R$ mil)
        f1 = (x1 * 25.0) + (x2 ** 2 * 8.0)

        # Objetivo 2: tempo médio de ciclo (minutos)
        f2 = 120.0 / x1 + 40.0 / x2

        # Restrição: consumo de energia C(x1, x2) = x1 * x2^1.5 <= 120
        consumo = x1 * (x2 ** 1.5)
        g1 = consumo - 120.0

        out["F"] = [f1, f2]
        out["G"] = [g1]


if __name__ == "__main__":
    problema = FrotaRobosProblem()
    algoritmo = NSGA2(pop_size=40)
    res = minimize(problema, algoritmo, termination=('n_gen', 60), seed=1)

    X = np.atleast_2d(res.X)
    F = np.atleast_2d(res.F)
    print("Soluções não dominadas:", len(F))

    # Escolha das 3 soluções de trade-off
    i_custo = np.argmin(F[:, 0])     # menor custo
    i_tempo = np.argmin(F[:, 1])     # menor tempo
    # intermediária: ponto mais próximo do meio (valores normalizados)
    Fn = (F - F.min(axis=0)) / (F.max(axis=0) - F.min(axis=0))
    i_meio = np.argmin(np.abs(Fn[:, 0] - 0.5) + np.abs(Fn[:, 1] - 0.5))

    nomes = [("Menor custo", i_custo), ("Menor tempo", i_tempo), ("Intermediária", i_meio)]
    for nome, i in nomes:
        consumo = X[i][0] * X[i][1] ** 1.5
        print(f"\n{nome}")
        print(f"  Robôs: {X[i][0]:.2f} | Velocidade: {X[i][1]:.2f} m/s")
        print(f"  Custo: R$ {F[i][0]:.2f} mil | Tempo de ciclo: {F[i][1]:.2f} min | Consumo: {consumo:.2f}")

    plt.figure(figsize=(8, 5))
    plt.scatter(F[:, 0], F[:, 1], color='teal', s=40, label="Soluções não dominadas")
    for (nome, i), cor in zip(nomes, ["red", "blue", "black"]):
        plt.scatter(F[i, 0], F[i, 1], color=cor, s=110, marker='*', label=nome, zorder=5)
    plt.title("Exercício 7 — Fronteira de Pareto: Frota de Robôs")
    plt.xlabel("Custo total (R$ mil) [Minimizar]")
    plt.ylabel("Tempo médio de ciclo (min) [Minimizar]")
    plt.grid(True)
    plt.legend()
    plt.savefig("imagens/exercicio_7.png", dpi=120, bbox_inches="tight")
    plt.show()
```

### Resultado no console

```
Soluções não dominadas: 40

Menor custo
  Robôs: 5.00 | Velocidade: 1.00 m/s
  Custo: R$ 133.01 mil | Tempo de ciclo: 63.97 min | Consumo: 5.01

Menor tempo
  Robôs: 15.60 | Velocidade: 3.90 m/s
  Custo: R$ 511.29 mil | Tempo de ciclo: 17.96 min | Consumo: 119.91

Intermediária
  Robôs: 9.22 | Velocidade: 3.24 m/s
  Custo: R$ 314.77 mil | Tempo de ciclo: 25.34 min | Consumo: 53.90
```

### Gráfico

<img width="827" height="574" alt="exercicio_7" src="https://github.com/user-attachments/assets/89c24e6d-f79d-471f-9ffc-a9eb5c3c1fbc" />

### Análise

A solução de menor custo usa a frota mínima (5 robôs) na velocidade mínima (1 m/s): custa R$ 133,01 mil, mas cada entrega leva quase 64 minutos. A de menor tempo usa cerca de 15,6 robôs a 3,9 m/s: o ciclo cai para 17,96 minutos, mas o custo vai para R$ 511,29 mil. Nessa solução o consumo de energia ficou em 119,91, quase no limite de 120, o que mostra que a restrição está ativa e é ela que impede o algoritmo de continuar aumentando robôs e velocidade. A solução intermediária (9,22 robôs a 3,24 m/s) custa R$ 314,77 mil com ciclo de 25,34 minutos, e parece um bom equilíbrio entre investimento e eficiência.

---

## Conclusão

Em todos os exercícios vimos que o NSGA-II entrega várias alternativas e não uma única resposta certa. Cada ponto do gráfico é uma configuração que não é dominada por nenhuma outra, e a decisão final depende da prioridade de quem usa (economizar, ganhar velocidade ou buscar equilíbrio). Também aprendemos a transformar maximização em minimização (exercício 4) e a usar restrições no formato G ≤ 0 (exercícios 6 e 7).
