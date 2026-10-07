# Resultados — Aula 09 — CIAO
*Grupo:* _Gabriela Camarço de Sousa_, _Igor Ferreira Alves_ e _Luis Gustavo dos Santos Talgatti._
---

## 1. Justificativa dos limites do universo e dos formatos das funções de pertinência

### 1.1 Limites do universo do discurso

O universo de discurso é a faixa de valores que cada variável pode assumir. Os limites foram escolhidos de acordo com o significado de cada variável na prática:

| Laboratório | Variável | Universo | Justificativa |
|---|---|---|---|
| Lab 01 | temperatura | 0 a 40 °C | Cobre desde um dia frio até um dia bem quente, que é onde um ventilador é usado. Valores fora disso não fazem sentido para o problema. |
| Lab 01 | velocidade | 0 a 100 % | Velocidade do ventilador em porcentagem da potência máxima (0 = parado, 100 = máximo). |
| Lab 02 | serviço e comida | 0 a 10 (passo 0,1) | É a escala de nota que as pessoas já usam. O passo de 0,1 deixa o gráfico e o cálculo mais precisos. |
| Lab 02 | gorjeta | 0 a 25 % (passo 0,5) | A aula define a gorjeta máxima como 25 % da conta. |
| Lab 03 | frequência | 0 a 100 % | Porcentagem de presença do aluno nas aulas. |
| Lab 03 | desempenho | 0 a 10 | Média das notas, que é a escala usada na faculdade. |
| Lab 03 | risco de evasão | 0 a 100 pontos | Escala de pontos, onde 0 é nenhum risco e 100 é risco máximo. |

Em todos os casos o universo começa e termina nos valores que a variável realmente pode ter. Se o universo fosse maior do que o necessário, sobraria espaço vazio no gráfico. Se fosse menor, ficaria faltando valor possível.

### 1.2 Triangulares vs trapezoidais

- **Triangular (`trimf`):** tem um único ponto com pertinência 1. É usada quando o termo tem um "valor ideal" bem definido. Exemplos: "morno" (25 °C) no lab 01, "média" da gorjeta (13 %) e "regular" do desempenho no lab 03.
- **Trapezoidal (`trapmf`):** tem uma faixa inteira com pertinência 1. É usada nos extremos, porque a partir de certo ponto o valor já é "totalmente" daquele termo. Exemplo: acima de 35 °C já é totalmente "quente", e abaixo de 15 °C já é totalmente "frio".

Em resumo: **triângulo no meio** (um ponto central) e **trapézio nas pontas** (uma faixa que continua valendo 1). O trapézio também dá uma saída mais estável nos extremos, porque a pertinência não muda dentro da faixa plana.

Nos laboratórios 01 e 02 os formatos já estavam definidos no código base. No lab 03 os formatos foram escolhidos pelo critério acima.

---

## 2. O que a lógica fuzzy realiza

Na lógica comum (booleana) uma afirmação é verdadeira ou falsa. Na lógica fuzzy ela pode ser **parcialmente verdadeira**, com grau de 0 a 1. Por exemplo, 20 °C não é "frio" nem "morno" de forma exata: é um pouco frio e um pouco morno ao mesmo tempo.

O sistema segue as seguintes etapas:

1. **Entrada nítida (crisp):** o número medido, por exemplo 20 °C.
2. **Fuzzificação:** transforma o número em graus de pertinência. Para 20 °C: frio = 0,5 e morno = 0,5.
3. **Regras fuzzy:** aplica os SE... ENTÃO. "SE frio ENTÃO velocidade baixa" ativa a regra com força 0,5, e "SE morno ENTÃO velocidade média" também com 0,5.
4. **Inferência:** junta o resultado de todas as regras numa área só (agregação).
5. **Defuzzificação:** transforma essa área em um número. Aqui foi usado o **centroide** (o centro de massa da área).
6. **Saída nítida:** o número final, por exemplo 44 % de velocidade.

Na prática, a lógica fuzzy permite que o computador raciocine de forma "mais ou menos", parecido com uma pessoa, e dá uma resposta **suave e contínua** em vez de pular de um valor para outro.

---

## 3. Lab 01 — Ventilador fuzzy

**Arquivo:** `lab01_aula09.py`

**Saída no terminal:**

```
10°C -> ventilador a 17%
20°C -> ventilador a 44%
25°C -> ventilador a 50%
30°C -> ventilador a 56%
38°C -> ventilador a 83%
```

**Funções de pertinência geradas:**

<img width="576" height="434" alt="Funções de pertinência da temperatura" src="https://github.com/user-attachments/assets/facd7ff5-eb5c-4a50-b00f-843beed5eb47" />
<img width="580" height="434" alt="Funções de pertinência da velocidade do ventilador" src="https://github.com/user-attachments/assets/d52a37eb-bb60-4bd3-be69-f485484916fc" />

**Análise dos resultados:**

- **10 °C → 17 %:** a temperatura é totalmente "frio" (pertinência 1). Só a regra "frio → baixa" é ativada, e o centroide do triângulo "baixa" fica em torno de 17 %. Por isso o ventilador não vai a 0 %, e sim a um valor baixo.
- **20 °C → 44 %:** é meio "frio" (0,5) e meio "morno" (0,5). As duas regras ativam, e a saída fica entre baixa e média, um pouco abaixo de 50 %.
- **25 °C → 50 %:** é totalmente "morno". Só a regra da velocidade média dispara e o centroide cai no meio (50 %).
- **30 °C → 56 %:** é meio "morno" e meio "quente", então a saída fica um pouco acima de 50 %.
- **38 °C → 83 %:** é totalmente "quente", e o centroide do triângulo "alta" fica em torno de 83 %.

A velocidade sobe aos poucos conforme a temperatura aumenta, sem saltos. Essa é a diferença da lógica fuzzy para um `if temperatura > 30`.

---

## 4. Lab 02 — Gorjeta com scikit-fuzzy

**Arquivo:** `lab02_aula09.py`

O código pede as notas no terminal. Foram usados os valores padrão do próprio código (serviço = 7 e comida = 3).

**Saída no terminal:**

```
Nota do serviço (0-10) [7]:
Nota da comida (0-10) [3]:

=> Gorjeta sugerida: 12.5%
```

**Gráficos gerados:**

<img width="576" height="434" alt="Funções de pertinência do serviço" src="https://github.com/user-attachments/assets/062ba2da-f267-4609-bd0d-ef32e7607178" />

<img width="576" height="434" alt="Funções de pertinência da comida" src="https://github.com/user-attachments/assets/4fe8e5bc-4696-4330-8579-f0b1c2278227" />

<img width="576" height="434" alt="Gorjeta: área agregada e centroide" src="https://github.com/user-attachments/assets/dc8fd6cd-9bfa-4e8c-acb4-1b00b29ace33" />

**Como o resultado foi calculado para (serviço 7, comida 3):**

- Serviço 7: "médio" = 0,6 e "bom" = 0,4.
- Comida 3: "ruim" = 0,6.
- Regra 1 (serviço ruim OU comida ruim → baixa): força 0,6.
- Regra 2 (serviço médio → média): força 0,6.
- Regra 3 (serviço bom OU comida boa → alta): força 0,4.
- As três áreas são juntadas e o centroide dá **12,5 %**.

O serviço foi razoável e a comida ruim, então uma gorjeta média/baixa faz sentido.

### Experimentos

Os experimentos foram feitos no arquivo `experimentos_lab02.py`.

#### Experimento 1: trocar a regra 2 por `servico["medio"] & comida["medio"]`

| Caso | Regra original | Regra com E |
|---|---|---|
| (7, 3) | 12,55 % | 12,55 % |
| (7, 1) — teste extra | 11,20 % | 10,55 % |

Para (7, 3) **nada mudou**, porque serviço "médio" e comida "média" valem os dois 0,6, e o E usa o mínimo (min(0,6; 0,6) = 0,6), igual ao valor de antes. No teste extra com (7, 1), a comida "média" vale só 0,2, então o E reduz a força da regra 2 e a gorjeta cai para 10,55 %. Ou seja, com o E a regra fica mais exigente.

#### Experimento 2: trocar a forma das curvas do serviço (para 7, 3)

| Forma | Gorjeta |
|---|---|
| Triangular | 12,55 % |
| Trapezoidal | 13,59 % |
| Gaussiana | 12,28 % |

A mudança foi pequena. A gaussiana tem curvas arredondadas e a transição entre os termos fica mais suave. O trapézio deu a maior gorjeta porque a faixa plana mantém a pertinência alta por mais tempo.

#### Experimento 3: métodos de defuzzificação (para 7, 3)

| Método | Gorjeta |
|---|---|
| centroid | 12,55 % |
| bisector | 12,58 % |
| mom (média dos máximos) | 12,75 % |
| som (menor dos máximos) | 7,80 % |
| lom (maior dos máximos) | 17,80 % |

Centroide, bisector e mom ficaram parecidos. Já `som` e `lom` dão valores bem diferentes, porque olham só para o ponto máximo da área e ignoram o resto do formato. O centroide considera a área toda, por isso é o mais usado.

#### Experimento 4: adicionar o conjunto "excelente" ao serviço

Foi criado o termo `excelente` (triângulo [7, 10, 10]), o "bom" foi ajustado para [4, 7, 9] e a regra nova foi escrita:

```python
ctrl.Rule(servico["excelente"], gorjeta["alta"])
```

Para (serviço 9, comida 5): sem "excelente" a gorjeta foi 16,81 % e com "excelente" foi 16,45 %. A diferença é pequena, porque o "bom" já levava a gorjeta para alta. O novo termo só refina a divisão no topo da escala.

#### Experimento 5: testar (0, 0), (10, 10) e (5, 5)

| Serviço | Comida | Gorjeta |
|---|---|---|
| 0 | 0 | 4,33 % |
| 10 | 10 | 21,00 % |
| 5 | 5 | 12,67 % |

O comportamento foi o esperado: notas péssimas dão gorjeta baixa, notas máximas dão gorjeta alta e notas medianas dão gorjeta média. Porém, (0, 0) não dá 0 % e (10, 10) não dá 25 %. Isso acontece porque o centroide é a média da área inteira, que nunca chega exatamente ao extremo do universo.

---

## 5. Lab 03 — Projeto próprio: risco de evasão de um aluno

**Arquivo:** `lab03_aula09.py`

### Etapa 1 — Definição do problema

O problema escolhido foi estimar o **risco de evasão de um aluno** a partir da frequência e do desempenho. Hoje quem decide isso é o coordenador ou o professor, olhando as faltas e as notas e usando a experiência para perceber quem está em perigo de abandonar o curso. As entradas são a **frequência** (% de presença, 0 a 100) e o **desempenho** (média das notas, 0 a 10). A saída é o **risco de evasão** (0 a 100 pontos). O fuzzy é adequado porque não existe uma fronteira exata: um aluno com 74 % de presença não é muito diferente de um com 76 %, e uma média 5,9 não é muito diferente de 6,1. Termos como "frequência baixa" e "desempenho regular" são naturalmente vagos, e um simples `if frequencia < 75` trataria os dois alunos de forma completamente diferente. Também há casos em que um fator compensa o outro, por exemplo um aluno com notas ótimas e frequência baixa.

### Etapa 2 — Modelagem

**Universos de discurso:**

| Variável | Tipo | Universo | Unidade |
|---|---|---|---|
| frequencia | entrada | 0 a 100 | % de presença |
| desempenho | entrada | 0 a 10 | média das notas |
| risco | saída | 0 a 100 | pontos |

**Termos linguísticos e funções de pertinência:**

| Variável | Termo | Forma | Parâmetros |
|---|---|---|---|
| frequencia | baixa | trapezoidal | [0, 0, 55, 70] |
| frequencia | media | triangular | [60, 75, 90] |
| frequencia | alta | trapezoidal | [80, 90, 100, 100] |
| desempenho | ruim | trapezoidal | [0, 0, 3, 5] |
| desempenho | regular | triangular | [4, 6, 8] |
| desempenho | bom | trapezoidal | [7, 8.5, 10, 10] |
| risco | baixo | trapezoidal | [0, 0, 20, 40] |
| risco | medio | triangular | [30, 50, 70] |
| risco | alto | trapezoidal | [60, 80, 100, 100] |

Os trapézios ficam nas pontas e os triângulos no meio, como explicado na seção 1.2. O ponto central da frequência "média" é 75 %, que é a presença mínima exigida para aprovação nas faculdades.

**Base de regras (8 regras):**

| Nº | Regra |
|---|---|
| R1 | SE frequência é baixa **E** desempenho é ruim ENTÃO risco é alto |
| R2 | SE frequência é baixa **E** desempenho é regular ENTÃO risco é alto |
| R3 | SE frequência é média **E** desempenho é ruim ENTÃO risco é alto |
| R4 | SE frequência é média **E** desempenho é regular ENTÃO risco é médio |
| R5 | SE frequência é baixa **E** desempenho é bom ENTÃO risco é médio |
| R6 | SE frequência é alta **E** desempenho é ruim ENTÃO risco é médio |
| R7 | SE frequência é média **E** desempenho é bom ENTÃO risco é baixo |
| R8 | SE frequência é alta **E** (desempenho é regular **OU** desempenho é bom) ENTÃO risco é baixo |

A regra R8 usa E e OU juntos, e as 8 regras cobrem todas as 9 combinações possíveis entre os termos de frequência e de desempenho.

**Gráficos das funções de pertinência:**

<img width="580" height="434" alt="image" src="https://github.com/user-attachments/assets/ad26563f-e251-4631-95fb-3efea808b462" />
<img width="576" height="434" alt="image" src="https://github.com/user-attachments/assets/b8a96f50-955e-4e19-9ec9-5c4ec73a671c" />
<img width="580" height="434" alt="image" src="https://github.com/user-attachments/assets/aef2628b-005b-46af-a8f7-9916be63c398" />


### Etapa 3 — Implementação

O código está em `lab03_aula09.py` e usa NumPy, Matplotlib e scikit-fuzzy. Para rodar:

```
pip install numpy matplotlib scikit-fuzzy
python lab03_aula09.py
```

O código imprime a tabela de testes e salva os gráficos na pasta `imagens/`.

### Etapa 4 — Testes

Para comparar com a resposta esperada, o código converte o número da saída em classe: abaixo de 35 = baixo, de 35 a 65 = médio, acima de 65 = alto.

| Nº | Frequência (%) | Desempenho | Saída do sistema | Classe | Resposta esperada | Acertou? |
|---|---|---|---|---|---|---|
| 1 | 95 | 9,0 | 15,6 | baixo | baixo | sim |
| 2 | 50 | 2,0 | 84,4 | alto | alto | sim |
| 3 | 75 | 6,0 | 50,0 | médio | médio | sim |
| 4 | 95 | 2,0 | 50,0 | médio | médio | sim |
| 5 | 50 | 9,0 | 50,0 | médio | médio | sim |
| 6 | 75 | 9,0 | 15,6 | baixo | baixo | sim |

**Análise dos testes:**

- **Testes 1 e 6:** alunos com boas notas e frequência média ou alta têm risco baixo.
- **Teste 2:** frequência e notas ruins juntas dão o maior risco (84,4).
- **Teste 3:** aluno mediano em tudo fica no meio da escala (50).
- **Testes 4 e 5:** são os casos em que um fator ruim é compensado pelo outro bom. O sistema respondeu risco médio, como esperado.

Nos testes 3, 4 e 5 o resultado deu exatamente 50,0. Isso ocorre porque só a regra com risco "médio" foi ativada, e o centroide de um triângulo simétrico cai no seu ponto central.

**Resultado do teste 4 (frequência 95 e desempenho 2,0), com a área agregada e a linha do centroide:**

<img width="580" height="434" alt="image" src="https://github.com/user-attachments/assets/f663ee72-a21e-464f-9daf-1ce0aaebbcf3" />

---

## 6. Conclusão

Foram montados três sistemas fuzzy: o ventilador, a gorjeta e o risco de evasão. A modelagem (universo, termos e formato das curvas) muda bastante o resultado, e a lógica fuzzy dá respostas graduais em vez de saltos. Os experimentos mostraram que a escolha do operador (E/OU), do formato das curvas e do método de defuzzificação influencia a saída, e que o centroide é o método mais equilibrado.

## 7. Arquivos desta pasta

| Arquivo | Descrição |
|---|---|
| `resultados_aula09.md` | Este relatório |
| `lab01_aula09.py` | Ventilador fuzzy |
| `lab02_aula09.py` | Gorjeta com scikit-fuzzy |
| `experimentos_lab02.py` | Experimentos do lab 02 |
| `lab03_aula09.py` | Projeto próprio: risco de evasão |
| `imagens/` | Gráficos usados neste relatório |
