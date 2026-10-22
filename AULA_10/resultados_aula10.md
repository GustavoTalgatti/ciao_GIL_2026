# Resultados — Aula 10 — CIAO
*Grupo:*  _Gabriela Camarço de Sousa_, _Igor Ferreira Alves_ e _Luis Gustavo dos Santos Talgatti._ 
---

## 1. Como montamos o sistema

O sistema recebe dois valores de um incidente de segurança e devolve a urgência de resposta.

| Variável | Tipo | Universo | Conjuntos (função) |
|---|---|---|---|
| Impacto | Entrada | 0 a 100 % | baixo `[0,0,40]`, médio `[20,50,80]`, alto `[60,100,100]` |
| Explorabilidade | Entrada | 0 a 10 | baixa `[0,0,4]`, moderada `[2,5,8]`, alta `[6,10,10]` |
| Urgência | Saída | 0 a 100 % | baixa `[0,0,13]`, média `[10,30,50]`, alta `[30,60,90]`, crítica `[62.5,100,100]` |

Todas as funções são triangulares (`trimf`). Usamos o operador E (mínimo) nas regras e o método de Mamdani.

Observação: os limites da urgência baixa (13) e da crítica (62.5) foram ajustados para o código reproduzir os mesmos valores do enunciado (4.33 % e 87.5 %). Assim conseguimos estudar o problema na prática.

---

## 2. Desafio dos Extremos

### Resultado da execução com o Centroide

| Entrada (Impacto, Explorabilidade) | Esperado | Saída do sistema |
|---|---|---|
| (0, 0) | 0 % | **4.33 %** |
| (100, 10) | 100 % | **87.50 %** |

O gráfico da saída está em `saida_centroide.png`.

### Pergunta 1 - Por que o Centroide com triângulos não chega em 0 % nem em 100 %?

O centroide calcula o **centro de massa da área** que sobrou depois da inferência, e não o ponto onde a pertinência é máxima. Em (0, 0) só a regra 1 dispara, com força 1, e a saída é o triângulo inteiro de "Urgência Baixa". Esse triângulo vai de 0 a 13, mas tem área espalhada para a direita. O centro de massa de um triângulo `[0,0,13]` é (0+0+13)/3 = **4.33**.

Em (100, 10) acontece o mesmo do outro lado. Só a regra 9 dispara e a saída é o triângulo de "Urgência Crítica" `[62.5,100,100]`. A área dele fica espalhada para a esquerda, então o centro de massa é (62.5+100+100)/3 ≈ **87.5**.

Resumindo: como o conjunto tem largura, o centro de massa sempre fica "para dentro" da escala. Ele só chegaria exatamente em 0 ou 100 se o conjunto fosse um único ponto, sem área. Por isso o centroide nunca cobre as pontas da escala.

### Pergunta 2 - O que acontece se a Urgência Crítica virar trapézio (`trapmf`)?

Testamos duas versões, sempre com centroide:

| Versão | (0, 0) | (100, 10) |
|---|---|---|
| Original (triângulo `[62.5,100,100]`) | 4.33 | 87.50 |
| A1 - trapézio `[62.5, 90, 100, 100]` | 4.33 | 86.79 |
| A2 - trapézio `[80, 95, 100, 100]` | 4.33 | 93.00 |

Na A1 o resultado até **piorou** (86.79). Ficou um "ombro" plano entre 90 e 100, mas a base continuou larga e puxou o centro de massa para a esquerda. Na A2 estreitamos a base e o resultado subiu para 93. Mesmo assim **não chegou em 100**, porque o conjunto ainda tem área.

Conclusão: o trapézio melhora o valor na borda superior quando a base é estreita, mas não resolve o problema por completo. Também não mexe na borda inferior (continua 4.33), porque só trocamos a função da Urgência Crítica.

### Pergunta 3 - O que acontece com o método MOM (Mean of Maximum)?

O MOM não olha a área. Ele pega a média dos pontos onde a pertinência é máxima. Como os triângulos de "baixa" e "crítica" têm pico exatamente em 0 e em 100, o resultado fica cravado.

| Método | (0, 0) | (100, 10) |
|---|---|---|
| Centroide (original) | 4.33 | 87.50 |
| MOM (Abordagem B) | **0.00** | **100.00** |

O custo aparece no meio da escala. No gráfico `comparacao_abordagens.png` (Explorabilidade fixa em 5), o maior salto entre dois valores vizinhos de impacto foi:

| Sistema | Maior salto de saída |
|---|---|
| Centroide (triângulo, A1 e A2) | 16.23 |
| MOM | 55.08 |

Com o MOM a curva vira uma escada. Por exemplo, perto de impacto 29 a saída pula de cerca de 5 para 60. Isso acontece porque o MOM só enxerga o conjunto que está "ganhando" e ignora a mistura entre as regras, que é justamente a vantagem da lógica fuzzy.

### Qual abordagem é mais recomendável?

| Critério | A (trapézio + centroide) | B (MOM) |
|---|---|---|
| Crava 0 % e 100 % | Não (4.33 e 93.00) | **Sim** |
| Suavidade no meio da escala | **Sim** (salto de 16.23) | Não (salto de 55.08) |

Nenhuma das duas faz as duas coisas ao mesmo tempo. Escolhemos a **Abordagem A (trapézio + centroide)**, porque o objetivo do sistema é decidir a urgência de forma gradual e contínua, e a superfície 3D precisa ser contínua. Um erro de 7 pontos no topo (93 em vez de 100) ainda classifica o incidente como crítico, enquanto um salto de 55 pontos poderia fazer dois incidentes quase iguais receberem urgências muito diferentes. O MOM só seria melhor se a prioridade fosse exatamente 0 e 100 nas pontas, aceitando a perda de suavidade.

---

## 3. Matriz de Regras 3x3 (9 regras)

| Impacto \ Explorabilidade | Baixa (0-4) | Moderada (2-8) | Alta (6-10) |
|---|---|---|---|
| **Baixo (0-40)** | Urgência Baixa | Urgência Baixa | Urgência Média |
| **Médio (20-80)** | Urgência Média | Urgência Alta | Urgência Alta |
| **Alto (60-100)** | Urgência Crítica | Urgência Crítica | Urgência Crítica |

Codificação no Python (as 9 regras estão no arquivo `lab01_aula10.py`):

| Regra | SE Impacto | E Explorabilidade | ENTÃO Urgência |
|---|---|---|---|
| 1 | baixo | baixa | baixa |
| 2 | baixo | moderada | baixa |
| 3 | baixo | alta | média |
| 4 | médio | baixa | média |
| 5 | médio | moderada | alta |
| 6 | médio | alta | alta |
| 7 | alto | baixa | crítica |
| 8 | alto | moderada | crítica |
| 9 | alto | alta | crítica |

Como são todas as combinações possíveis (3 x 3), não existe entrada sem regra ativada, ou seja, não há lacunas de cobertura.

---

## 4. Análise da Superfície de Decisão 3D

A imagem `superficie_decisao.png` foi gerada com a Abordagem A2 (trapézio + centroide), varrendo o impacto de 0 a 100 e a explorabilidade de 0 a 10.

- **Continuidade:** a superfície não tem buracos nem regiões sem valor. Toda combinação de entrada gera uma saída, o que confirma que as 9 regras cobrem todo o espaço.
- **Região baixa (impacto até uns 20):** com explorabilidade baixa ou moderada a urgência fica perto de 5 %, que é o piso do centroide. Com explorabilidade alta (acima de 6) ela sobe para cerca de 30 %, seguindo a regra 3 (urgência média).
- **Região do meio (impacto entre 30 e 70):** com explorabilidade moderada ou alta forma um patamar em torno de 60 %, que é a urgência "alta" (regras 5 e 6). Com explorabilidade baixa a saída fica menor, entre 25 e 50 %, porque a regra 4 dá só urgência média.
- **Região alta (impacto acima de 80):** a superfície sobe para 91 a 93 % e fica quase plana, qualquer que seja a explorabilidade. Isso mostra que impacto alto domina a decisão, como definido nas regras 7, 8 e 9.
- **Inclinações fortes:** as subidas mais íngremes acontecem em impacto ~20 e ~75. São as zonas em que as regras mudam de conjunto. Mesmo assim a transição é gradual e não um degrau, porque o centroide mistura as regras ativas ao mesmo tempo.
- **Efeito dos dois eixos:** o impacto pesa mais do que a explorabilidade. A explorabilidade só faz diferença nas faixas baixa e média de impacto.

**Conclusão geral:** o sistema Mamdani com 9 regras responde de forma coerente e contínua. O centroide deixa as pontas um pouco "encolhidas" (4.33 e 93), e isso é um efeito conhecido do método, que pode ser reduzido ajustando as funções de pertinência.
