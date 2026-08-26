# Resultados — Aula 04 — CIAO
*Grupo:*  _Gabriela Camarço de Sousa_, _Igor Ferreira Alves_ e _Luis Gustavo dos Santos Talgatti._ 
---
## Exercício 1 - Elitismo e estabilidade

Rodamos o algoritmo genético duas vezes, com e sem elitismo, usando a
mesma seed nas duas execuções (assim a população inicial e a matriz de
distâncias ficam idênticas, e a única diferença real é o elitismo).

Em vez de olhar só pro melhor fitness já visto (que por definição nunca
piora), acompanhamos o melhor fitness **de cada geração**. É aí que a
diferença aparece:

- Com elitismo: o melhor da geração nunca piora (0 retrocessos em 80
  gerações), porque o campeão da geração anterior sempre é copiado para
  a próxima.
- Sem elitismo: o melhor da geração piorou 2 vezes. Dá pra ver isso
  claramente no gráfico (`convergencia_elitismo.png`) — por volta da
  geração 21, a curva sem elitismo cai até 182 e depois sobe de volta
  pra quase 199, porque o melhor indivíduo daquele momento se perdeu no
  meio da seleção/crossover/mutação.

Isso confirma o que o roteiro pede pra observar: o elitismo não
necessariamente acelera a convergência, mas garante estabilidade —
o algoritmo nunca "esquece" a melhor solução encontrada até ali.

## Exercício 2 - Penalidade de SLA

Implementamos a penalidade estática de 1000 ms para qualquer enlace da
rota que ultrapasse o limite de SLA de 50 ms. Com a seed 15 e a rota de
teste `[0, 1, 2, 3, 4, 5]`, apenas o enlace 3→4 (62,04 ms) estourou o
limite, então:

- Custo somando só as latências: 160,00 ms
- Penalidade aplicada: 1000,00 ms (1 violação)
- Custo final: 1160,00 ms

## Exercício 3 - Balanceamento de carga em servidores

Problema de alocar 20 tarefas em 4 servidores minimizando o makespan
(tempo do servidor mais sobrecarregado). Como esse problema não é uma
permutação (pode repetir servidor, um servidor pode ficar de fora), o
crossover OX do exemplo do professor não serve aqui — usamos crossover
uniforme e mutação por gene.

Resultado: makespan de 137s, contra uma média teórica ideal de 135,25s
(soma de todos os tempos dividida por 4 servidores). Ou seja, ficamos a
menos de 2 segundos do limite inferior teórico, o que indica uma
distribuição bem equilibrada. Gráfico de convergência em
`convergencia_exercicio03.png`.

## Desafio de Fechamento AC-1 - SD-WAN Zero-Trust

Esse foi o mais trabalhoso. O enunciado pede uma topologia de 12
roteadores (0 a 11), origem fixa no nó 0, destino fixo no nó 11, com
latência, perda de pacotes e reputação de segurança por nó.

Decisões de projeto (documentadas também no cabeçalho do próprio
arquivo `desafio_ac1_master_sdwan.py`):

- A topologia não é uma malha completa: montamos uma árvore geradora
  aleatória (garante que todos os nós estão alcançáveis) mais alguns
  enlaces extras, sem deixar um link direto entre a origem e o destino.
  Isso obriga o algoritmo a escolher de fato uma rota por nós
  intermediários.
- Cada indivíduo é uma permutação dos nós intermediários mais um valor
  de corte `k`, que define quantos nós da permutação realmente entram
  na rota. Isso permite ao algoritmo evoluir rotas de tamanhos
  diferentes (e não só rotas que passam por todo mundo).
- Os nós 0 e 11 ficam de fora da checagem de reputação, porque são os
  roteadores da própria rede (origem e destino fixos).

Com a seed 2026, os nós 3, 5 e 9 ficaram com reputação abaixo de 50. A
rota escolhida pelo algoritmo foi `0 → 2 → 11`, com fitness 139,90 e
nenhuma penalidade de segurança.

Pra justificar essa escolha, comparamos com rotas reais alternativas
que passam pelos nós não confiáveis:

| Rota | Latência | Perda | Penalidade | Fitness |
|---|---|---|---|---|
| 0 → 2 → 11 (escolhida) | 88,15 ms | 10,35% | 0 | **139,90** |
| 0 → 2 → 5 → 11 | 117,25 ms | 11,21% | 5000 | 5173,30 |
| 0 → 9 → 2 → 11 | 84,19 ms | 12,05% | 5000 | 5144,46 |
| 0 → 9 → 3 → 11 | 87,60 ms | 10,75% | 5000 | 5141,33 |

O caso mais interessante é a rota por `0 → 9 → 2 → 11`: ela tem
latência ainda **menor** que a rota escolhida (84,19 ms contra 88,15
ms). Se o fitness considerasse só latência e perda de pacotes, essa
rota venceria. Mas como o nó 9 tem reputação 25,0 (abaixo de 50), a
penalidade de segurança de 5000 pontos faz o fitness dela disparar.
Isso mostra que a penalidade está cumprindo exatamente o papel que
deveria: impedir que uma rota mais rápida, porém insegura, seja
escolhida no lugar de uma rota confiável.

Gráfico de convergência em `convergencia_desafio_ac1.png`.
