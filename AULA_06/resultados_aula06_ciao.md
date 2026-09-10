# Resultados — Aula 06 — CIAO
*Grupo:*  _Gabriela Camarço de Sousa_, _Igor Ferreira Alves_ e _Luis Gustavo dos Santos Talgatti._ 
---
## Laboratório 01 — ACO básico

### Outputs

Vizinhos do nó 0: `[1, 2]`\
Vizinhos do nó 2: `[0, 1, 3, 4]`

Rotas de teste (5 formigas antes de qualquer feromônio ser reforçado):

```
Formiga 1: [0, 1, 2, 3, 4, 5]
Formiga 2: [0, 1, 2, 3, 4, 5]
Formiga 3: [0, 1, 2, 3, 4, 5]
Formiga 4: [0, 1, 2, 3, 4, 5]
Formiga 5: [0, 1, 2, 3, 4, 5]
```

Teste de custo de uma rota isolada:

```
Rota: [0, 2, 3, 4, 5]
Custo: 9.0
```

Resultado final, depois das 50 iterações com 20 formigas:

```
Melhor rota encontrada: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
```

Curva de convergência:

<img width="846" height="471" alt="lab01_convergencia" src="https://github.com/user-attachments/assets/520d5dfa-dba2-4bd3-aa22-121884e9fa54" />


A curva já nasce em 8 e fica reta até o final. Isso faz sentido: a rede tem só 6 nós, então já na primeira leva de 20 formigas alguma delas encontra uma das rotas de custo mínimo (na verdade existem duas rotas empatadas com custo 8: 0-1-2-3-4-5 e 0-1-2-4-5). Como o melhor valor já é achado logo de cara, não dá pra ver uma "queda" de custo ao longo das iterações, o que aconteceria de forma mais visível numa rede maior.

Matriz final de feromônio:

<img width="598" height="519" alt="lab01_feromonio" src="https://github.com/user-attachments/assets/b140a974-e25f-4e34-928e-75cc68d58e1c" />


```
[[  0. 500.   0.   0.   0.   0.]
 [  0.   0. 500.   0.   0.   0.]
 [  0.   0.   0. 500.   0.   0.]
 [  0.   0.   0.   0. 500.   0.]
 [  0.   0.   0.   0.   0. 500.]
 [  0.   0.   0.   0.   0.   0.]]
```

As conexões 0→1, 1→2, 2→3, 3→4 e 4→5 (exatamente a rota escolhida como melhor) ficaram com o valor máximo de feromônio, enquanto todas as outras conexões zeraram. Isso mostra o efeito de "bola de neve" do ACO: uma vez que uma rota boa começa a ser usada, ela vai recebendo cada vez mais reforço e as outras praticamente somem do mapa.

### Respostas

**1. Por que o ACO usa várias formigas em vez de uma só?**

Com uma formiga só, o algoritmo só teria um caminho por vez pra comparar com nada, não haveria como saber se aquele caminho é bom ou ruim. Usando várias formigas ao mesmo tempo, cada uma pode seguir um caminho diferente (a escolha é por sorteio, ponderada pela atratividade), e no final da rodada dá pra comparar os custos de várias rotas e reforçar só as melhores. É essa comparação entre várias tentativas que permite ao algoritmo aprender qual caminho compensa mais.

**2. Por que uma rota mais barata recebe mais feromônio?**

Porque o depósito é calculado como Q / custo. Quanto menor o custo, maior essa divisão, então rotas baratas recebem um reforço maior. Na prática isso cria um ciclo: rota barata → mais feromônio → maior atratividade → mais formigas escolhem essa rota nas próximas iterações → a rota recebe ainda mais feromônio. É esse ciclo que faz o algoritmo convergir para caminhos bons com o tempo.

**3. O que aconteceria sem evaporação?**

Sem evaporação, o feromônio só cresceria e nunca diminuiria. Se a primeira rota "boa" encontrada não for a melhor possível, ela mesmo assim ia acumular cada vez mais feromônio e virar praticamente a única opção, porque a diferença de atratividade entre ela e qualquer rota nova (que começa com feromônio baixo) ficaria enorme rapidinho. As formigas ficariam presas nessa escolha inicial e o algoritmo perderia a capacidade de descobrir rotas melhores depois. A evaporação existe justamente pra dar chance de caminhos novos competirem, mesmo depois de outro caminho já ter recebido bastante reforço.

---

## Laboratório 02 — Experimentando o ACO

Todas as execuções usaram a mesma semente aleatória (`seed=42`) pra garantir que a diferença entre os resultados venha dos parâmetros e não da sorte de cada rodada.

### Outputs

| Experimento | ALPHA | BETA | Evaporação | Formigas | Melhor rota | Melhor custo | Iteração do melhor | Formigas sem rota (None) | Feromônio máx. | Feromônio médio |
|---|---|---|---|---|---|---|---|---|---|---|
| Baseline | 1.0 | 2.0 | 0.5 | 20 | [0,1,2,3,4,5] | 8.0 | 0 | 0 | 500.0 | 104.17 |
| ALPHA=0.1 | 0.1 | 2.0 | 0.5 | 20 | [0,1,2,3,4,5] | 8.0 | 0 | 2 | 392.52 | 90.9 |
| ALPHA=5.0 | 5.0 | 2.0 | 0.5 | 20 | [0,1,2,3,4,5] | 8.0 | 0 | 0 | 500.0 | 104.17 |
| BETA=0.5 | 1.0 | 0.5 | 0.5 | 20 | [0,1,2,3,4,5] | 8.0 | 0 | 4 | 500.0 | 104.17 |
| BETA=5.0 | 1.0 | 5.0 | 0.5 | 20 | [0,1,2,3,4,5] | 8.0 | 0 | 0 | 500.0 | 104.17 |
| Evaporação=0.1 | 1.0 | 2.0 | 0.1 | 20 | [0,1,2,3,4,5] | 8.0 | 0 | 0 | 2486.51 | 517.93 |
| Evaporação=0.9 | 1.0 | 2.0 | 0.9 | 20 | [0,1,2,3,4,5] | 8.0 | 0 | 0 | 277.78 | 57.87 |
| Formigas=5 | 1.0 | 2.0 | 0.5 | 5 | [0,1,2,3,4,5] | 8.0 | 0 | 0 | 125.0 | 26.04 |
| Formigas=50 | 1.0 | 2.0 | 0.5 | 50 | [0,1,2,3,4,5] | 8.0 | 0 | 1 | 1250.0 | 260.42 |

Em todas as 9 configurações o custo final foi 8.0, já na iteração 0. Como a rede é pequena e tem caminhos empatados no custo mínimo, mudar os parâmetros não muda o resultado final, quem muda é a "história" de como o algoritmo chega lá (quanto feromônio se acumula e quantas formigas se perdem no caminho). O gráfico de convergência abaixo é o da configuração base; os das outras 8 configurações ficaram praticamente idênticos (reta em 8).

<img width="691" height="394" alt="lab02_01" src="https://github.com/user-attachments/assets/10ea9843-8244-4571-9bfa-ecc1a2a94a8e" />


### Respostas

**Quando aumentamos o ALPHA, a influência da experiência acumulada aumenta ou diminui?**

Aumenta. O ALPHA é o expoente do feromônio na fórmula da atratividade, então quanto maior ele for, mais peso o feromônio acumulado tem na hora da formiga escolher o próximo passo. No teste com ALPHA=0.1 tivemos 2 formigas que não conseguiram fechar rota (ficaram sem opção no meio do caminho), porque a escolha ficou quase toda por conta do custo, ignorando o que já tinha sido aprendido. Com ALPHA=5.0 isso não aconteceu nenhuma vez, a experiência acumulada passou a guiar as formigas de forma bem mais consistente.

**BETA baixo x BETA alto:**

Com BETA=0.5 o custo pesa pouco na decisão, e foi justamente aí que apareceu o maior número de formigas sem rota (4), sem o custo guiando a escolha, a formiga acaba tomando caminhos mais aleatórios e às vezes entra num nó sem saída. Com BETA=5.0, o custo domina a decisão, o comportamento fica bem mais "certeiro" e nenhuma formiga se perdeu.

**O que acontece quando o algoritmo esquece rápido as experiências anteriores?**

Com TAXA_EVAPORACAO=0.9 (esquece rápido), o feromônio final ficou bem mais baixo (máximo de 277.78, contra 2486.51 com evaporação de 0.1). Ou seja: quando o esquecimento é rápido, o feromônio não tem tempo de se acumular muito, e o algoritmo depende mais do reforço constante das formigas recentes do que da "memória" de longo prazo da colônia. Numa rede pequena como essa isso não atrapalha o resultado final, mas numa rede maior, esquecer rápido demais poderia fazer o algoritmo perder rotas boas que ele já tinha encontrado antes.

**Poucas formigas x muitas formigas:**

Com 5 formigas, o feromônio acumulado no final foi bem menor (125.0) do que com 50 formigas (1250.0), faz sentido, porque cada formiga que passa por uma aresta deposita feromônio, então mais formigas por iteração significa mais depósito total. Também foi só com 50 formigas que apareceu 1 caso de formiga sem rota, com mais formigas rodando, a chance de pelo menos uma delas tomar um caminho ruim também aumenta, mesmo que a maioria continue encontrando a rota boa.

---

## Laboratório 03 — Completando o ACO

### Outputs

```
Melhor rota: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
```

### Respostas

**1. Por que usar 1/custo em vez do custo direto?**

Porque a lógica é: quanto menor o custo, mais atraente o caminho deve ser. Se usássemos o custo direto na fórmula, ia acontecer o contrário, caminhos caros teriam atratividade maior, o que não faz sentido nenhum pro problema. Invertendo (1/custo), um custo pequeno vira um número grande, e é isso que empurra a atratividade pra cima.

**2. O que acontece com a atratividade quando uma rota recebe mais feromônio?**

A atratividade daquela aresta aumenta, porque o feromônio entra na conta elevado a ALPHA (fer ** ALPHA) multiplicando o termo do custo. Mais feromônio significa uma probabilidade maior daquele caminho ser escolhido de novo nas próximas rotas.

**3. Por que impedir revisitar um nó já visitado?**

Sem essa trava, a formiga poderia ficar indo e voltando entre os mesmos nós pra sempre, sem nunca fechar caminho até o destino (um loop infinito). Além disso, uma rota que passa duas vezes pelo mesmo nó não faz sentido como caminho de rede. Ao só permitir nós que ainda não estão na lista visitados/rota, garantimos que a formiga sempre está avançando: ou ela chega ao destino, ou fica sem candidatos e a rota é descartada (None).

---

## Laboratório 04 — ACO do zero

### Outputs — configuração mínima pedida (ALPHA=1.0, BETA=2.0, evaporação=0.5, 20 formigas, 50 iterações)

```
========== RESULTADO ==========
Melhor rota encontrada: [0, 1, 2, 3, 4, 5]
Melhor custo: 8.0
```

<img width="691" height="394" alt="lab04_01" src="https://github.com/user-attachments/assets/ab4ca081-26a2-400d-b7d5-8f3988e7c201" />


### Outputs — configuração alternativa testada (ALPHA=3.0, BETA=1.0, evaporação=0.2, 10 formigas, 30 iterações)

```
Melhor rota encontrada: [0, 1, 2, 4, 5]
Melhor custo: 8.0
```

<img width="691" height="394" alt="lab04_02" src="https://github.com/user-attachments/assets/1582480c-bcc5-4e0b-8fff-684bc4e43c1d" />


Mesmo mudando bastante os parâmetros (menos formigas, menos iterações, ALPHA maior, BETA menor, evaporação mais rápida), o algoritmo ainda encontrou uma rota de custo 8 — só que dessa vez foi a outra rota empatada (0-1-2-4-5 em vez de 0-1-2-3-4-5). Isso reforça algo que já tinha aparecido no Laboratório 02: numa rede pequena como essa, o resultado final tende a ser o mesmo custo ótimo em quase qualquer configuração razoável de parâmetros; o que muda é o caminho específico escolhido e a rapidez/estabilidade com que se chega lá.

### Respostas

**1. Como o feromônio ajuda o ACO a aprender quais caminhos são melhores?**

O feromônio funciona como uma espécie de "memória coletiva" da colônia. Toda vez que uma formiga termina uma rota, ela deposita feromônio proporcional ao quão boa (barata) foi aquela rota. Com o tempo, os caminhos que foram usados por rotas boas vão acumulando mais feromônio que os outros, e como a escolha do próximo passo leva o feromônio em conta, esses caminhos passam a ser escolhidos com mais frequência. Ninguém "decide" qual é o melhor caminho, ele vai se destacando sozinho conforme mais formigas passam por ele.

**2. Qual a diferença entre explorar e aproveitar (exploitar)?**

Explorar é testar caminhos novos ou pouco usados, mesmo sem garantia de que vão ser bons, é o que permite ao algoritmo descobrir rotas melhores que ainda não foram tentadas. Aproveitar é focar nos caminhos que já mostraram ser bons até agora, usando o que já foi aprendido pra tentar garantir um resultado consistente. O ACO precisa equilibrar os dois: só explorar nunca converge pra nada, e só aproveitar corre o risco de travar na primeira solução razoável encontrada, mesmo que exista uma melhor.

**3. Numa rede muito maior, o que investigar primeiro pra melhorar o desempenho?**

Primeiro eu olharia pra função de escolha (escolher_proximo) e o equilíbrio entre ALPHA e BETA, numa rede grande, com muito mais caminhos possíveis, esse equilíbrio entre confiar na experiência acumulada e no custo direto fica bem mais crítico do que numa rede de 6 nós, onde quase qualquer configuração já dá certo. Em seguida, olharia o número de formigas e de iterações: uma rede maior tem um espaço de busca muito maior, então provavelmente vai precisar de mais formigas explorando ao mesmo tempo e mais iterações pra dar tempo do feromônio realmente se firmar nos caminhos bons, em vez de convergir cedo demais pra uma solução só razoável.
