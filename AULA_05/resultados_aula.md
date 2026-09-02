# Resultados — Aula 05 — CIAO
*Grupo:*  _Gabriela Camarço de Sousa_, _Igor Ferreira Alves_ e _Luis Gustavo dos Santos Talgatti._ 
---

## Outputs das missões

### Missão 1 – Partícula Solitária

Posição inicial: -8.0733 (fitness 65.18)\
Depois de 20 iterações: posição -7.8575 (fitness 61.74)\
Erro final em relação ao ótimo (x = 0): **7.86**

A partícula quase não se moveu. Isso faz sentido quando a gente para pra pensar: como só tem uma partícula, toda vez que ela melhora um pouquinho, o pBest já vira igual à posição atual, então o "puxão" cognitivo (que depende de pBest - posicao) some quase na hora. Sobra só a inércia carregando uma velocidade bem pequena, por isso o avanço foi tão lento.

<img width="1189" height="490" alt="cf981452-b6ac-4b38-a998-f81590168103" src="https://github.com/user-attachments/assets/fff54450-70a8-465a-9561-31863e57925b" />

### Missão 2 – O Enxame

Fitness inicial do enxame (melhor partícula): 4.29

Fitness final depois de 50 iterações: **0.0028** (o ótimo real é 0, em x=1, y=1)

Bem diferente da Missão 1, com 20 partículas trocando informação pelo gBest, o enxame convergiu rápido pra perto do mínimo da função de Rosenbrock, que é uma função bem mais complicada (tem aquele "vale" estreito e curvo) do que o x² da missão anterior.

<img width="1362" height="490" alt="3bbeb1ee-b4e1-405c-b005-9ac4a0e2ffcb" src="https://github.com/user-attachments/assets/c1b80436-3c63-4b3d-8aa0-5b4940673963" />

### Missão 3 – Problema Corporativo (Logística)

- 50 clientes, 5 centros de distribuição, demanda média de 51 unidades
- Tempo de execução: 0.43s
- Custo total final: **16955.05**
- Centros encontrados:
  - Centro 1: (10.00, 10.00)
  - Centro 2: (10.00, 10.00)
  - Centro 3: (10.00, 0.00)
  - Centro 4: (10.00, 0.00)
  - Centro 5: (10.00, 10.00)

Reparamos em duas coisas estranhas aqui. Primeiro, dos 5 centros, só sobraram **2 posições diferentes de verdade** (três foram parar exatamente no mesmo canto e dois no outro canto), o enxame não conseguiu espalhar os centros pelo mapa. Segundo, comparando com o custo inicial de um enxame recém-criado nesse mesmo problema (calculamos à parte e deu por volta de 11615), o custo final **piorou** em vez de melhorar. Olhando o código, a função fitness retorna -custo_total, mas o loop de atualização (que é código pronto do professor) sempre guarda o fitness *menor* (if fitness < pBest_fit). Isso faz o algoritmo, na prática, empurrar os centros pra **longe** dos clientes em vez de perto.

<img width="1389" height="490" alt="2e61ca37-78c4-470b-8d9c-e2f1848b01a0" src="https://github.com/user-attachments/assets/824afe2a-2991-4f27-82fe-18578d207186" />

### Missão 4 – Otimização de Parâmetros

Resultado médio de 5 execuções por configuração:

| Experimento      | Custo Médio | Melhor Custo | Pior Custo |
|-------------------|------------:|-------------:|-----------:|
| Padrão            |   16764.48  |     19025.98 |   15443.17 |
| Inércia Alta      |   19262.97  |     21460.47 |   16955.05 |
| Inércia Baixa     |   16386.38  |     19025.98 |   13552.66 |
| Cognitivo Alto    |   16570.90  |     21460.47 |   13552.66 |
| Social Alto       |   15812.90  |     16955.05 |   12756.20 |
| Mais Partículas   |   20164.06  |     21460.47 |   16955.05 |

(Mesma observação da Missão 3 vale aqui: a métrica "custo" desse experimento tá na mesma direção invertida, então o que a tabela mostra de confiável é a comparação **relativa** entre as configurações, não o valor absoluto.)

<img width="1389" height="790" alt="eb91f7c7-1897-4233-8d1c-ec55edf95962" src="https://github.com/user-attachments/assets/3921f126-e6d4-46cd-9dcb-22b4c1eeab47" />

---

## Relatório Final PSO

### Parte 1: O que você aprendeu?

**1. Explique com suas palavras o que é o PSO e como ele funciona.**

PSO é um jeito de otimizar que copia o comportamento de um bando de pássaros (ou cardume) procurando comida. Em vez de testar uma solução de cada vez, a gente solta várias "partículas" espalhadas pelo espaço de busca, e cada uma se move combinando três coisas: o quanto ela já vinha andando antes (inércia), o melhor lugar que ela mesma já achou (pBest) e o melhor lugar que qualquer partícula do grupo já achou (gBest). A cada iteração essas três forças são somadas pra formar a nova velocidade, a partícula se move, e o processo se repete. Com o tempo o grupo inteiro converge pra perto do ponto ótimo, porque toda partícula é puxada ao mesmo tempo pela própria experiência e pela experiência coletiva do bando.

**2. Qual a diferença entre pBest e gBest? Por que ambos são importantes?**

pBest é a memória individual, a melhor posição que aquela partícula específica já visitou sozinha. gBest é a memória coletiva, a melhor posição que qualquer partícula do enxame inteiro já encontrou até agora. Os dois são importantes porque, sem um deles, o algoritmo perde o equilíbrio: só com pBest, cada partícula fica presa na própria experiência e não aproveita o que as outras descobriram (foi mais ou menos isso que vimos na Missão 1, com uma partícula só, sem gBest de verdade, ela demorou muito mais pra convergir). Só com gBest, todo mundo converge rápido demais pro mesmo ponto e o enxame perde a capacidade de explorar outras regiões, correndo o risco de ficar preso num mínimo local, algo parecido com o que aconteceu na Missão 3, quando os centros colapsaram em só 2 posições.

### Parte 2: Sua experiência com as missões

**Missão 1 – A Partícula Solitária:**

A partícula encontrou o mínimo?
( ) Sim &nbsp; (X) Não

Quantas iterações foram necessárias?
Não foi suficiente, rodamos as 20 e ela ainda estava longe do zero (erro final de ~7,86). Pelo ritmo que ela tava indo, ia precisar de muito mais iterações.

Dificuldade: (X) Fácil &nbsp; ( ) Médio &nbsp; ( ) Difícil

**Missão 2 – O Enxame:**

O enxame encontrou o mínimo global?\
(X) Sim &nbsp; ( ) Não\
*(chegou bem perto, fitness final de 0,0028, sendo que o ótimo é 0. Na prática consideramos que convergiu.)*

Compare com a Missão 1: O enxame foi mais rápido?\
(X) Sim &nbsp; ( ) Não

Dificuldade: ( ) Fácil &nbsp; (X) Médio &nbsp; ( ) Difícil

**Missão 3 – Problema Corporativo:**

Compare com o custo inicial: Melhorou?\
( ) Sim &nbsp; (X) Não\
*(o custo final ficou maior que o custo inicial do enxame, ver observação acima sobre o sinal da função fitness.)*

Quantos centros foram alocados? 
Os 5 centros foram criados, mas só 2 posições realmente diferentes apareceram no resultado (3 centros caíram no mesmo ponto e os outros 2 em outro ponto).

Dificuldade: ( ) Fácil &nbsp; ( ) Médio &nbsp; (X) Difícil

**Missão 4 – Otimização de Parâmetros:**

Melhor configuração encontrada: w = 0.7, c1 = 1.8, c2 = 2.5, partículas = 30 *("Social Alto")*

Pior configuração encontrada: w = 0.7, c1 = 1.8, c2 = 1.8, partículas = 60 *("Mais Partículas")*

Dificuldade: (X) Fácil &nbsp; ( ) Médio &nbsp; ( ) Difícil

**3. O que você observou sobre o efeito de:**

- **Inércia (w):** aumentar de 0,7 pra 0,9 piorou o resultado, a partícula fica "flutuando" mais e demora mais pra se acomodar dentro do número de iterações que a gente rodou. Baixar pra 0,5 ajudou um pouco, o oposto do que a inércia alta fez.
- **Cognitivo (c1):** subir de 1,8 pra 2,5 quase não mudou nada, ficou dentro da margem de variação entre execuções.
- **Social (c2):** foi o que mais ajudou, subir de 1,8 pra 2,5 deu o melhor resultado entre todos os experimentos. Faz sentido: puxar mais forte pro gBest acelera a convergência.
- **Número de partículas:** foi o mais contraintuitivo, passar de 30 pra 60 partículas piorou o resultado médio. A gente também notou que o desvio padrão dos experimentos foi bem alto (chegando a ±2600 em alguns casos), e como cada configuração só rodou 5 vezes, dá pra desconfiar que parte dessa diferença seja só ruído estatístico e não um efeito real do parâmetro.

**4. Qual configuração você recomenda para este problema? Por quê?**

A "Social Alto" (w=0.7, c1=1.8, c2=2.5), teve o menor custo médio e também o menor valor entre as melhores execuções. Faz sentido pro nosso caso: como o orçamento de iterações é curto (50), dar mais peso pro que o grupo já descobriu ajuda o enxame a convergir mais rápido em vez de ficar cada partícula explorando por conta própria.

---

### Observações gerais

A parte mais trabalhosa foi a Missão 3, por causa das 10 dimensões (5 centros × x,y), é bem mais difícil de visualizar mentalmente o que tá acontecendo do que nas Missões 1 e 2, que dava pra ver no gráfico. A descoberta da inconsistência no sinal da função fitness (Missões 3 e 4) também tomou um tempo pra entender.
