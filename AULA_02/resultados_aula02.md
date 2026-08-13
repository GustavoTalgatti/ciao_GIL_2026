# Resultados — Aula 02 — CIAO
*Grupo:*  _Gabriela Camarço de Sousa_, _Igor Ferreira Alves_ e _Luis Gustavo dos Santos Talgatti._ 
---

## Laboratório 1

**Resultados obtidos:**
```
Total de solucoes avaliadas: 32
Tempo de execucao: 0.000033 segundos
Melhor valor encontrado: 9
Combinacao otima (0=nao leva, 1=leva): (1, 1, 0, 1, 1)

Itens escolhidos:
 - Livro (peso: 2, valor: 3)
 - Fone (peso: 1, valor: 2)
 - Carregador (peso: 1, valor: 3)
 - Chocolate (peso: 1, valor: 1)
```

**Respostas:**

1- O número de soluções avaliadas foi exatamente 32 porque temos 5 itens e cada um deles só
pode estar em dois estados: dentro da mochila ou fora dela. Isso dá 2⁵ = 32 combinações
possíveis, que é justamente o espaço de busca do problema.

2- Se colocássemos 15 itens em vez de 5, o espaço de busca passaria para 2¹⁵ = 32.768
combinações. Ainda é um número que o computador resolve em menos de um segundo, mas já dá
pra perceber o crescimento: com 20 itens já passamos de 1 milhão de combinações, como o
material da aula mostra. É esse crescimento que depois vira inviável.

3- Um problema parecido do dia a dia: fazer a mala pra uma viagem de avião respeitando o
limite de peso da bagagem, decidindo quais roupas e itens levar pra ter o "valor" (o quanto
cada coisa é útil/importante) máximo sem estourar o peso. Outro exemplo: montar o carrinho
de compras do mês com orçamento fixo, escolhendo os produtos que trazem mais benefício
para o dinheiro disponível.

---

## Laboratório 2

**Resultados obtidos:**
```
>>> 4 cidades
    Rotas avaliadas : 6
    Melhor custo    : 80
    Melhor rota     : (0, 1, 3, 2, 0)
    Tempo (segundos): 0.000305

>>> 5 cidades
    Rotas avaliadas : 24
    Melhor custo    : 41
    Melhor rota     : (0, 1, 2, 3, 4, 0)
    Tempo (segundos): 0.000043

>>> 6 cidades
    Rotas avaliadas : 120
    Melhor custo    : 91
    Melhor rota     : (0, 1, 3, 4, 5, 2, 0)
    Tempo (segundos): 0.000199
```

| Número de cidades | Rotas avaliadas | Tempo (s) | Melhor custo |
|---|---|---|---|
| 4 | 6 | 0.000305 | 80 |
| 5 | 24 | 0.000043 | 41 |
| 6 | 120 | 0.000199 | 91 |

**Respostas:**

1- O número de rotas não cresce nem de forma linear nem quadrática, cresce de forma fatorial,
que é muito mais rápida que as duas. Dá pra ver isso nos próprios números: de 4 para 5
cidades o total de rotas salta de 6 para 24 (multiplicou por 4), e de 5 para 6 cidades
salta de 24 para 120 (multiplicou por 5). Se fosse crescimento linear, o aumento seria
sempre o mesmo valor fixo; se fosse quadrático, cresceria proporcional ao quadrado do
número de cidades. Aqui o fator de multiplicação vai aumentando a cada cidade nova, porque
é (n-1)!.

2- Para estimar 10 cidades: seriam (10-1)! = 362.880 rotas. Usando como referência o tempo de
6 cidades (120 rotas em ~0,0002s), a proporção seria de 362.880 / 120 ≈ 3.024 vezes mais
rotas, o que daria algo em torno de 0,6 segundo nesse mesmo computador — ainda rápido, mas
o crescimento é tão agressivo que com 15 cidades (87 bilhões de rotas, como o próprio
código menciona) o tempo já passaria de dias ou semanas.

3- Dizemos que o TSP é um problema "difícil" não porque ele é complicado de entender (a regra
é simples: visitar todas as cidades e voltar gastando o mínimo possível), mas porque o
tempo necessário para garantir a rota ótima cresce de forma explosiva (fatorial) conforme
aumenta o número de cidades. Não existe hoje um método conhecido que resolva isso de forma
exata e rápida para instâncias grandes.

---

## Laboratório 3 

**Resultados obtidos (20 instâncias, 12 itens cada, capacidade 30):**
```
Instancia  1 | Otimo:  199 | Gulosa:  199 | Gap:   0.0%
Instancia  2 | Otimo:  170 | Gulosa:  170 | Gap:   0.0%
Instancia  3 | Otimo:  155 | Gulosa:  155 | Gap:   0.0%
Instancia  4 | Otimo:  147 | Gulosa:  147 | Gap:   0.0%
Instancia  5 | Otimo:  261 | Gulosa:  261 | Gap:   0.0%
Instancia  6 | Otimo:  214 | Gulosa:  214 | Gap:   0.0%
Instancia  7 | Otimo:  191 | Gulosa:  187 | Gap:   2.1%
Instancia  8 | Otimo:  183 | Gulosa:  183 | Gap:   0.0%
Instancia  9 | Otimo:  215 | Gulosa:  206 | Gap:   4.2%
Instancia 10 | Otimo:  174 | Gulosa:  174 | Gap:   0.0%
Instancia 11 | Otimo:  262 | Gulosa:  262 | Gap:   0.0%
Instancia 12 | Otimo:  206 | Gulosa:  206 | Gap:   0.0%
Instancia 13 | Otimo:  231 | Gulosa:  231 | Gap:   0.0%
Instancia 14 | Otimo:  309 | Gulosa:  309 | Gap:   0.0%
Instancia 15 | Otimo:  294 | Gulosa:  294 | Gap:   0.0%
Instancia 16 | Otimo:  247 | Gulosa:  247 | Gap:   0.0%
Instancia 17 | Otimo:  136 | Gulosa:  134 | Gap:   1.5%
Instancia 18 | Otimo:  212 | Gulosa:  212 | Gap:   0.0%
Instancia 19 | Otimo:  243 | Gulosa:  243 | Gap:   0.0%
Instancia 20 | Otimo:  193 | Gulosa:  193 | Gap:   0.0%

===== RESUMO =====
Gap medio     : 0.39%
Gap minimo    : 0.00%
Gap maximo    : 4.19%
Desvio padrao : 1.03%
```

**Respostas**

**1- Código completo:** a função `calcular_gap` e o loop de experimentos foram
implementados e estão funcionando — o código roda as 20 instâncias, calcula o gap de cada
uma e imprime o resumo final sem erros.

**2 - Valor do gap médio obtido:** o gap médio ficou em 0,39%. Em 17 das 20 instâncias a
heurística gulosa achou exatamente o valor ótimo (gap de 0%), e no pior caso (instância 9)
ficou 4,19% abaixo do ótimo.

**3 - A heurística gulosa é boa o suficiente?** Para esse problema, sim — o resultado dela
chega muito perto do ótimo na maioria das vezes, mesmo sendo bem mais simples e rápida que
testar todas as combinações. Usaríamos essa heurística em situações onde a resposta
precisa ser rápida e não é viável esperar um método exato, como um sistema que decide isso
em tempo real ou um problema com muitos itens. Já em decisões críticas, com poucos itens e
onde vale a pena gastar mais tempo de computador pra garantir a melhor resposta possível
(por exemplo, um investimento grande, ou um problema pequeno o suficiente pra ser resolvido
de forma exata em tempo razoável), preferiríamos usar o método exato.


## Laboratório 4 — Modelagem de um problema real

**Problema escolhido:** escolha de corridas de aplicativo durante um turno de trabalho

## 4.1 Descrição do problema

Quem trabalha com aplicativo de transporte ou de entrega (tipo Uber, 99 ou iFood) recebe
várias solicitações de corrida durante o turno de trabalho. Cada corrida tem uma duração
estimada (em minutos) e um ganho (em reais). O motorista não consegue aceitar todas as
corridas, porque o turno tem um tempo limitado.

O problema é: **dado um conjunto de corridas disponíveis, quais delas o motorista deve
aceitar para ganhar o máximo possível sem estourar o tempo total do turno?**

Esse problema é bem parecido com o Problema da Mochila visto em aula: no lugar de "peso"
temos "duração da corrida", e no lugar de "valor" temos "ganho em reais". A "mochila" é o
tempo disponível no turno.

## 4.2 Modelagem formal

**O que é uma solução**
Uma solução candidata é um vetor de 0s e 1s, um para cada corrida disponível: 1 significa
que o motorista aceita a corrida, 0 significa que ele recusa. Por exemplo, com 10 corridas
disponíveis, uma solução poderia ser `[0,0,1,0,0,0,0,1,1,0]`, indicando que só as corridas
2, 7 e 8 foram aceitas.

**Espaço de busca**
Como cada corrida só pode ser aceita ou recusada, com *n* corridas existem 2ⁿ soluções
possíveis. No nosso exemplo usamos 10 corridas, então existem 2¹⁰ = 1.024 combinações
possíveis. Se o motorista recebesse 30 propostas no turno (o que não é incomum em um
turno cheio), já teríamos mais de 1 bilhão de combinações — o mesmo tipo de explosão
combinatória que vimos com a mochila e o caixeiro-viajante.

**Função objetivo**
Queremos **maximizar** a soma do ganho (em reais) de todas as corridas aceitas:

```
Ganho total = soma do ganho das corridas em que solucao[i] = 1
```

**Restrições**
A soma da duração das corridas aceitas não pode ultrapassar o tempo disponível no turno:

```
soma da duracao das corridas aceitas <= tempo_turno
```

No código, usamos um turno de 180 minutos (3 horas) como exemplo.

## 4.3 Classificação: fácil ou difícil?

Esse problema é essencialmente uma versão do Problema da Mochila 0/1, que é conhecido
por ser **NP-difícil**. Isso significa que, para garantir a melhor combinação de corridas
possível, em princípio seria necessário testar todas as 2ⁿ combinações — o que já vimos
na Atividade 1 que se torna inviável rapidamente conforme *n* cresce.

Na prática, com poucas corridas (10, 15) ainda dá para resolver por força bruta em um
computador comum. Mas se pensarmos em um aplicativo real, que teria que decidir isso para
milhares de motoristas e milhares de corridas ao mesmo tempo, e em tempo real, um método
exato deixa de ser viável — e é aí que fariam sentido as heurísticas e metaheurísticas
que vamos estudar ao longo da disciplina.

## 4.4 Sobre o código

O arquivo `lab04_aula02_CIAO.ipynb` implementa:
- Geração de uma lista de corridas com duração e ganho aleatórios;
- Uma função que gera uma solução aleatória (vetor de 0s e 1s);
- A função objetivo, que calcula o ganho total de uma solução;
- Uma função que verifica se a solução respeita a restrição de tempo do turno (ou seja,
  se ela é factível);
- Um teste com uma solução aleatória e mais 4 soluções extras para efeito de comparação.

O código não busca a solução ótima (isso não foi pedido nesta atividade) — ele só gera
soluções aleatórias, calcula o valor da função objetivo e verifica se cada uma é válida.

**Resultados obtidos:**
```
Corridas disponiveis no turno:
  Corrida 0: duracao=20 min | ganho=R$17.87
  Corrida 1: duracao=40 min | ganho=R$9.57
  Corrida 2: duracao=14 min | ganho=R$21.70
  Corrida 3: duracao=22 min | ganho=R$9.01
  Corrida 4: duracao=30 min | ganho=R$19.71
  Corrida 5: duracao=11 min | ganho=R$9.89
  Corrida 6: duracao=12 min | ganho=R$10.45
  Corrida 7: duracao=36 min | ganho=R$19.46
  Corrida 8: duracao=27 min | ganho=R$30.33
  Corrida 9: duracao=13 min | ganho=R$11.34

Solucao aleatoria gerada (1=aceita, 0=recusa): [0, 0, 1, 0, 0, 0, 0, 1, 1, 0]
Tempo total usado: 77 min (limite do turno: 180 min)
Ganho total da solucao: R$ 71.49
Essa solucao respeita a restricao de tempo? True

Gerando mais 4 solucoes aleatorias para comparacao:
  Tentativa 1: ganho=R$ 19.46 | tempo= 51 min | FACTIVEL
  Tentativa 2: ganho=R$ 98.20 | tempo=149 min | FACTIVEL
  Tentativa 3: ganho=R$100.21 | tempo=144 min | FACTIVEL
  Tentativa 4: ganho=R$120.16 | tempo=144 min | FACTIVEL
```

**Considerações do grupo:**

Escolhemos esse problema porque é uma decisão que qualquer motorista ou entregador de
aplicativo toma na prática, várias vezes por dia. A estrutura é basicamente a mesma da
mochila: no lugar de peso temos duração da corrida, no lugar de valor temos o ganho em
reais, e no lugar da capacidade da mochila temos o tempo disponível no turno.

Nos testes, todas as soluções aleatórias geradas acabaram sendo factíveis, mas isso foi
"sorte" da aleatoriedade — nada impede que uma combinação de corridas aleatória ultrapasse
o tempo do turno, por isso o código sempre verifica a restrição antes de considerar a
solução válida. Dá pra ver também que soluções diferentes geram ganhos bem diferentes
(de R$19,46 até R$120,16 nas tentativas), o que mostra a importância de não escolher as
corridas de forma aleatória e sim de forma inteligente — que é exatamente o que as
heurísticas e metaheurísticas que vamos ver ao longo do curso se propõem a fazer.

Classificamos esse problema como difícil (NP-difícil), pela mesma razão do Problema da
Mochila: com *n* corridas disponíveis existem 2ⁿ combinações possíveis, e não existe um
método conhecido que garanta a melhor combinação sem, no pior caso, ter que testar (quase)
todas elas.
