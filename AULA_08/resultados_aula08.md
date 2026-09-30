# Resultados — Aula 08 — CIAO
*Grupo:*  _Gabriela Camarço de Sousa_, _Igor Ferreira Alves_ e _Luis Gustavo dos Santos Talgatti._ 
---

## Lab 01 - PSO para balanceamento dinâmico de carga

### O que foi feito

Temos 6 zonas de disponibilidade (AZs) e precisamos achar os pesos W = [w1, ..., w6], com soma igual a 1, que deixem a temperatura média dos racks a menor possível. Os coeficientes de aquecimento são C = [42, 35, 58, 30, 50, 65].

O enunciado não explica como a temperatura de cada AZ muda com a carga. Se a temperatura fosse só `w_i * C_i`, o melhor seria mandar todo o tráfego para a AZ4 (a mais fria, 30 °C) e o problema ficaria sem sentido. Então assumimos que quanto mais tráfego a AZ recebe, mais quente ela fica:

```
T_i = C_i * (1 + 3 * w_i)
fitness = soma(w_i * T_i) + penalidade
```

A penalidade externa é de 50 pontos para cada °C que alguma AZ passar de 75 °C.

### Como o código funciona

- Classe `PSO` feita do zero, com velocidade, posição, P_best de cada partícula e G_best global. Guardamos o histórico do G_best e da média dos P_best a cada iteração.
- Atualização da velocidade: `v = 0.7*v + 1.5*r1*(pbest - x) + 1.5*r2*(gbest - x)`, com a velocidade limitada em 0.2.
- A cada iteração, depois de mexer na posição, aplicamos a normalização: os valores negativos são cortados e o vetor é dividido pela soma. Assim `sum(w) = 1` sempre.
- 100 iterações para cada tamanho de população (10, 30 e 50 partículas).

### Saída do código

```text
======================================================================
LAB 01 - PSO para balanceamento de carga entre 6 AZs
======================================================================
C = [42. 35. 58. 30. 50. 65.]
Modelo: T_i = C_i * (1 + 3.0 * w_i) | limite critico = 75 °C

Melhor distribuicao W encontrada (seed = 42)
----------------------------------------------------------------------
Populacao = 10 particulas
  W = [0.1784, 0.2475, 0.0832, 0.3164, 0.1231, 0.0513]
  sum(W) = 1.0000000000 -> OK
  Temperaturas por AZ = [64.48, 60.99, 72.49, 58.48, 68.47, 75.00]
  Temperatura maxima = 75.00 °C (limite 75) -> dentro do limite
  Fitness final (temp. media ponderada) = 63.4137

Populacao = 30 particulas
  W = [0.1784, 0.2474, 0.0832, 0.3165, 0.1232, 0.0513]
  sum(W) = 1.0000000000 -> OK
  Temperaturas por AZ = [64.48, 60.97, 72.48, 58.49, 68.48, 75.00]
  Temperatura maxima = 75.00 °C (limite 75) -> dentro do limite
  Fitness final (temp. media ponderada) = 63.4137

Populacao = 50 particulas
  W = [0.1785, 0.2474, 0.0832, 0.3165, 0.1232, 0.0513]
  sum(W) = 1.0000000000 -> OK
  Temperaturas por AZ = [64.49, 60.98, 72.48, 58.48, 68.47, 75.00]
  Temperatura maxima = 75.00 °C (limite 75) -> dentro do limite
  Fitness final (temp. media ponderada) = 63.4137

Evolucao do G_best (fitness) ao longo das iteracoes
----------------------------------------------------------------------
Iteracao       10 part.     30 part.     50 part.
1              244.3848      65.5944     120.4801
5               64.6438      63.7492      63.9919
10              64.0067      63.4607      63.9770
20              63.4396      63.4279      63.4264
30              63.4177      63.4159      63.4146
50              63.4140      63.4137      63.4137
75              63.4137      63.4137      63.4137
100             63.4137      63.4137      63.4137

Estabilidade: 20 execucoes com seeds diferentes (100 iteracoes)
----------------------------------------------------------------------
Populacao       Media final         Desvio         Melhor           Pior
10                 64.04840        0.97907       63.41368       67.23641
30                 63.54919        0.27101       63.41368       64.09121
50                 63.41368        0.00001       63.41368       63.41371

Grafico salvo em: lab01_convergencia.png
```

### Tabela com a melhor distribuição W (seed 42)

| População | w1 | w2 | w3 | w4 | w5 | w6 | sum(W) | Fitness (°C) |
|---|---|---|---|---|---|---|---|---|
| 10 partículas | 0.1784 | 0.2475 | 0.0832 | 0.3164 | 0.1231 | 0.0513 | 1.0000 (OK) | 63.4137 |
| 30 partículas | 0.1784 | 0.2474 | 0.0832 | 0.3165 | 0.1232 | 0.0513 | 1.0000 (OK) | 63.4137 |
| 50 partículas | 0.1785 | 0.2474 | 0.0832 | 0.3165 | 0.1232 | 0.0513 | 1.0000 (OK) | 63.4137 |

### Gráfico

<img width="1440" height="540" alt="image" src="https://github.com/user-attachments/assets/122ecbe1-1966-4d5e-8f80-0e1d68143c54" />

### Análise

- Nas três populações o PSO chegou praticamente na mesma distribuição e no mesmo fitness (63.4137 °C). A AZ4, que é a mais fria, recebeu a maior parte do tráfego (cerca de 31,6%), e a AZ6, que é a mais quente, recebeu a menor (cerca de 5,1%).
- A AZ6 ficou com temperatura de exatamente 75.00 °C. Isso mostra que a penalidade está funcionando: o algoritmo empurra o peso da AZ6 até o limite, mas não passa dele.
- A diferença entre as populações aparece na velocidade e na estabilidade. Na execução com seed 42, a população de 10 começou com um fitness muito ruim (244 °C, por causa da penalidade) e demorou mais para cair. Com 30 e 50 partículas a queda foi mais rápida.
- Repetindo 20 vezes com seeds diferentes, a população de 10 teve desvio de 0.98 e chegou a parar em 67.24 °C numa das execuções. Com 30, o desvio caiu para 0.27, e com 50 foi praticamente zero (0.00001). Ou seja, mais partículas deixam o resultado mais confiável.
- O preço disso é o custo computacional: 10, 30 e 50 partículas fazem 1000, 3000 e 5000 avaliações de fitness em 100 iterações. Com 30 partículas o resultado já fica bem próximo do final, e com 50 ele fica mais consistente. Para este problema pequeno, o custo extra de 50 partículas não pesa.
- A soma dos pesos deu 1.0 nas três execuções, então a normalização cumpriu o que o enunciado pede.

---

## Lab 02 - AG binário com penalidade para seleção de microsserviços

### O que foi feito

Um nó de Edge precisa escolher quais dos 15 microsserviços manter carregados, maximizando o valor de negócio, com no máximo 16 GB de RAM e 8 cores de CPU. Somando todos os serviços, o total é 41.5 GB de RAM e 15.5 cores, então não dá para carregar todos.

Cada indivíduo é um vetor de 15 bits (1 = serviço carregado). Duas formas de calcular o fitness foram comparadas:

- Estratégia A (penalidade rígida): se passar de qualquer limite (RAM ou CPU), o fitness é 0.
- Estratégia B (penalidade proporcional): o fitness é o valor de negócio menos 80 pontos para cada GB ou core que passou do limite (nunca menor que 0).

### Como o código funciona

- População de 50 indivíduos, 100 gerações, elitismo de 1 indivíduo.
- Seleção por torneio (3 competidores), crossover de ponto único (taxa 0.8) e mutação binária (2% por bit).
- Rodamos 20 vezes cada estratégia (seeds 0 a 19) e fizemos a média, para não depender de uma execução com sorte.
- Como são só 15 bits, também testamos as 32768 combinações por força bruta para saber qual é a resposta certa e poder comparar.
- Para medir a diversidade genética usamos a distância de Hamming média entre todos os pares da população (dividida por 15) e também o número de genomas diferentes na população.

### Saída do código

```text
======================================================================
LAB 02 - AG binario: selecao de microsservicos no Edge
======================================================================
#   Servico          Valor  RAM(GB)    CPU
1   Autenticacao        80      2.0    1.0
2   Cache               60      3.5    0.5
3   Telemetria          40      1.5    0.5
4   Pagamentos          95      4.0    1.5
5   Catalogo            70      3.0    1.0
6   Busca               65      2.5    1.0
7   Notificacoes        35      1.0    0.5
8   Recomendacao        85      5.0    2.0
9   Logs                30      2.0    0.5
10  API Gateway         90      2.5    1.0
11  Chat                50      2.0    1.0
12  Analytics           55      3.5    1.5
13  Video               75      4.5    2.0
14  Backup              25      3.0    1.0
15  Monitoramento       45      1.5    0.5
Total: valor=900 | RAM=41.5 GB | CPU=15.5 cores
Limites: RAM <= 16 GB e CPU <= 8 cores

Solucao otima (forca bruta, 2^15 combinacoes):
  genoma = 101011100110001
  valor=475 | RAM=16.0 | CPU=6.5
  servicos: Autenticacao, Telemetria, Catalogo, Busca, Notificacoes, API Gateway, Chat, Monitoramento

Melhor combinacao final de uma execucao (seed = 0)
----------------------------------------------------------------------
Estrategia A: genoma=101110100100001 | valor=455 | RAM=15.5 | CPU=6.0
   servicos: Autenticacao, Telemetria, Pagamentos, Catalogo, Notificacoes, API Gateway, Monitoramento
Estrategia B: genoma=101011100110001 | valor=475 | RAM=16.0 | CPU=6.5
   servicos: Autenticacao, Telemetria, Catalogo, Busca, Notificacoes, API Gateway, Chat, Monitoramento

Resumo de 20 execucoes (seeds 0 a 19)
----------------------------------------------------------------------
Estrategia A: valor final medio=459.8 | desvio=14.7 | pior=425 | melhor=475 | achou o otimo (475) em 6 de 20 execucoes
Estrategia B: valor final medio=470.5 | desvio=5.0 | pior=465 | melhor=475 | achou o otimo (475) em 11 de 20 execucoes

Fitness medio e desvio-padrao da populacao por geracao (media das 20 execucoes)
----------------------------------------------------------------------
Ger.   | Estrategia A               | Estrategia B              
       |        media        desvio |        media        desvio
1      |        60.41        120.74 |       118.21        131.96
5      |       272.08        147.38 |       337.13         86.43
10     |       330.32        163.72 |       392.13         81.99
20     |       374.75        158.42 |       422.15         80.68
30     |       373.44        159.39 |       419.59         86.42
50     |       379.03        158.28 |       426.15         81.58
75     |       383.39        154.87 |       429.31         81.96
100    |       383.06        154.95 |       428.75         83.63

Diversidade genetica e % de individuos inviaveis (media das 20 execucoes)
----------------------------------------------------------------------
Ger.   | Estrategia A                     | Estrategia B                    
       |   Hamming distintos   % inviav. |   Hamming distintos   % inviav.
1      |     0.500      50.0        79.4 |     0.500      50.0        79.4
5      |     0.355      38.5        20.5 |     0.319      38.0        31.4
10     |     0.145      21.1        19.8 |     0.144      22.0        26.8
20     |     0.049      12.3        15.5 |     0.051      12.3        13.6
30     |     0.049      11.5        15.9 |     0.046      11.4        15.4
50     |     0.047      11.8        14.9 |     0.052      12.4        13.5
75     |     0.050      11.6        14.3 |     0.041      11.0        12.7
100    |     0.046      11.3        14.4 |     0.046      11.2        14.6
Media ao longo das 100 geracoes:
  Hamming medio:      A = 0.076 | B = 0.075
  Genomas distintos:  A = 14.2 | B = 14.2 (de 50 individuos)

Grafico salvo em: lab02_comparacao.png
```

### Gráfico

<img width="1440" height="960" alt="image" src="https://github.com/user-attachments/assets/8d14a9ae-db87-4e0f-bdb1-240e26345d7f" />

### Análise

Média e desvio-padrão do fitness:

- A Estratégia B teve fitness médio mais alto em todas as gerações (cerca de 429 contra 383 na geração 100).
- O desvio-padrão da A ficou alto o tempo todo (entre 140 e 165 depois das primeiras gerações), e o da B caiu para a faixa de 75 a 90. Isso acontece porque na A os indivíduos inválidos valem 0 e os bons valem perto de 450, então a população fica dividida em dois grupos. Na B, os inválidos ficam com uma nota parcial e a diferença entre os indivíduos é menor.
- Esse desvio é do fitness, e não da diversidade genética. Por isso olhamos a diversidade separadamente.

Diversidade genética:

- Na nossa simulação não deu diferença relevante entre as duas. A média da distância de Hamming foi 0.076 na A e 0.075 na B, e a média de genomas diferentes foi 14.2 nas duas.
- Só na geração 5 a A estava um pouco acima (0.355 contra 0.319). Depois disso as curvas ficam praticamente coladas.
- Nas duas estratégias a diversidade despenca de 0.5 para perto de 0.05 já por volta da geração 20, e só não chega a zero por causa da mutação. Então, nos nossos testes, não dá para dizer que uma estratégia preservou melhor a diversidade do que a outra.

Melhor combinação final:

- A solução ótima (força bruta) tem valor 475, com 16.0 GB de RAM e 6.5 cores. Os serviços são: Autenticacao, Telemetria, Catalogo, Busca, Notificacoes, API Gateway, Chat e Monitoramento.
- A Estratégia B achou esse ótimo em 11 das 20 execuções. A Estratégia A achou em 6 das 20.
- O valor final médio foi 470.5 na B (desvio 5.0, pior caso 465) e 459.8 na A (desvio 14.7, pior caso 425).
- Na execução com seed 0, a B chegou em 475 (o ótimo) e a A parou em 455.
- Portanto, a Estratégia B encontrou melhores combinações e foi mais consistente. Uma explicação provável é que na A um indivíduo que passou só um pouquinho do limite vira 0 e some, perdendo genes bons, enquanto na B ele continua valendo alguma coisa e ajuda a população a chegar perto da fronteira de RAM/CPU.

---

## Lab 03 - ACO para topologia de rede de baixa latência

### O que foi feito

Precisamos ligar 10 switches em uma árvore geradora (9 arestas, sem ciclo, todos conectados) com a menor latência total possível, usando a matriz de latências D (10x10). A matriz está impressa na saída do código abaixo.

Entendemos o objetivo como minimizar a soma das latências das arestas que formam a árvore.

### Como o código funciona

- Cada formiga constrói uma árvore escolhendo uma aresta por vez. A chance de escolher a aresta (i, j) é proporcional a `tau_ij^1 * (1/D_ij)^3`.
- Verificação de ciclos e conectividade: usamos Union-Find. A formiga só pode escolher arestas que ligam dois grupos de switches diferentes, então nunca fecha ciclo. No final a função `arvore_valida` confere se tem 9 arestas e se todos os switches estão conectados (o código para se alguma árvore for inválida).
- Atualização do feromônio seguindo o enunciado: só as arestas das 3 melhores topologias da iteração são atualizadas. Elas evaporam com `rho = 0.2` (`tau = 0.8 * tau`) e depois recebem depósito de `100 / custo` de cada topologia em que aparecem.
- 20 formigas e 100 iterações.
- Como referência, calculamos a árvore ótima com o algoritmo de Kruskal (só para comparar) e sorteamos árvores aleatórias válidas.

### Saída do código

```text
======================================================================
LAB 03 - ACO para topologia em arvore de 10 switches
======================================================================
Matriz de latencias D (ms):
[[ 0 12 28  6 11 15 14 37 33 37]
 [12  0 40  5  8 35  5  9  9 37]
 [28 40  0 16 13  9 20 25 33 26]
 [ 6  5 16  0 40  7 21 24 29  3]
 [11  8 13 40  0 10 20  5 40 27]
 [15 35  9  7 10  0 33 22 25 16]
 [14  5 20 21 20 33  0 15  7 10]
 [37  9 25 24  5 22 15  0 32 19]
 [33  9 33 29 40 25  7 32  0 34]
 [37 37 26  3 27 16 10 19 34  0]]

Parametros: 20 formigas | 100 iteracoes | alfa=1.0 | beta=3.0 | rho=0.2 | top_k=3

Arvore final do ACO (seed = 42)
----------------------------------------------------------------------
Valida (sem ciclo e conectada)? True
Arestas (switch_a, switch_b, latencia):
   S0 - S3 : 6 ms
   S1 - S3 : 5 ms
   S1 - S4 : 8 ms
   S1 - S6 : 5 ms
   S2 - S5 : 9 ms
   S3 - S5 : 7 ms
   S3 - S9 : 3 ms
   S4 - S7 : 5 ms
   S6 - S8 : 7 ms
Latencia total = 55 ms

Matriz de Adjacencia final (10x10):
     S0  S1  S2  S3  S4  S5  S6  S7  S8  S9 
S0   0  0  0  1  0  0  0  0  0  0
S1   0  0  0  1  1  0  1  0  0  0
S2   0  0  0  0  0  1  0  0  0  0
S3   1  1  0  0  0  1  0  0  0  1
S4   0  1  0  0  0  0  0  1  0  0
S5   0  0  1  1  0  0  0  0  0  0
S6   0  1  0  0  0  0  0  0  1  0
S7   0  0  0  0  1  0  0  0  0  0
S8   0  0  0  0  0  0  1  0  0  0
S9   0  0  0  1  0  0  0  0  0  0
Soma de cada linha (grau de cada switch): [1 3 1 4 2 2 2 1 1 1]
Numero de arestas: 9 (esperado: 9)

Comparacao com topologia aleatoria
----------------------------------------------------------------------
Latencia da arvore aleatoria (1 sorteio, seed 7): 169 ms
Latencia media de 1000 arvores aleatorias:        186.0 ms
Latencia do ACO:                                  55 ms
Latencia otima (Kruskal, so referencia):          55 ms

Ganho do ACO sobre o sorteio unico:   67.5 %
Ganho do ACO sobre a media aleatoria: 70.4 %

Estabilidade: 20 execucoes do ACO (seeds 0 a 19)
----------------------------------------------------------------------
Latencia media=55.0 | desvio=0.00 | melhor=55 | pior=55
Execucoes que acharam o otimo (55 ms): 20 de 20

Evolucao do custo (seed = 42)
----------------------------------------------------------------------
Iteracao    melhor da iter.    melhor global   media formigas
1                        58               58             69.8
5                        55               55             57.2
10                       55               55             55.9
20                       55               55             56.0
30                       55               55             56.0
50                       55               55             55.7
75                       55               55             56.1
100                      55               55             56.1

Grafico salvo em: lab03_evolucao.png
```

### Gráfico

<img width="960" height="540" alt="image" src="https://github.com/user-attachments/assets/e507f8a2-9b51-4ec1-92ff-53d315793dcf" />

### Análise

- O ACO encontrou uma árvore válida com latência total de 55 ms. A matriz de adjacência impressa tem 9 arestas (soma das linhas = 18) e cada switch está ligado a pelo menos um outro.
- Comparando com uma topologia aleatória:
  - contra um sorteio único (169 ms), o ganho foi de 67.5%;
  - contra a média de 1000 árvores aleatórias (186 ms), o ganho foi de 70.4%.
- A solução do ACO (55 ms) é igual à solução ótima calculada por Kruskal. Nas 20 execuções com seeds diferentes, o ACO chegou nos 55 ms em todas.
- O custo caiu muito rápido: já na iteração 5 o melhor global era 55 ms. Isso acontece porque este problema é o da árvore geradora mínima, que é fácil, e porque usamos `beta = 3`, que dá bastante peso para as arestas de baixa latência. Em uma rede com mais restrições (por exemplo, limite de grau por switch), o ACO teria que trabalhar mais.
- A média das formigas ficou em torno de 56 ms depois da iteração 10, um pouco acima do melhor. Isso mostra que as formigas ainda exploram variações, e não ficam todas iguais.

---

## Conclusão

- No PSO, mais partículas deram resultados mais estáveis, mas o valor final foi o mesmo nas três populações. A normalização manteve a soma dos pesos em 1 e a penalidade segurou a AZ6 no limite de 75 °C.
- No AG, a penalidade proporcional (B) achou a melhor combinação de microsserviços com mais frequência do que a penalidade rígida (A). Na diversidade genética, as duas ficaram praticamente iguais.
- No ACO, a verificação com Union-Find garantiu árvores válidas e a solução final igualou o ótimo, com ganho de cerca de 70% sobre uma topologia aleatória.
- Limitações: os dados dos Labs 2 e 3 foram criados por nós, e o modelo de temperatura do Lab 1 foi uma suposição. Os números podem mudar se os dados oficiais forem diferentes.
