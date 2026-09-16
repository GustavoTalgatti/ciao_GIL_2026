# Resultados — Aula 07 — CIAO
*Grupo:*  _Gabriela Camarço de Sousa_, _Igor Ferreira Alves_ e _Luis Gustavo dos Santos Talgatti._ 
---
## LAB 01 — ACO com Busca Local (Exploration vs. Exploitation)

**Output da execução:**
```
[LAB 01 - SUCESSO] Melhor Caminho: [0, 1, 3, 4, 2, 0] | Custo: 70
```
<img width="843" height="680" alt="image" src="https://github.com/user-attachments/assets/55d0bc71-5385-4e8d-a76b-f8da59b62d06" />


**Questões técnicas**

1- Como o uso da busca local 2-opt afeta o equilíbrio entre Exploration e Exploitation na busca de caminhos?

A construção do caminho pelas formigas (escolha do próximo nó com base em feromônio e visibilidade) é a parte de Exploration do algoritmo, já que cada formiga monta uma rota de forma probabilística e caminhos bem diferentes podem surgir a cada iteração. O 2-opt entra depois, pegando o caminho que a formiga já montou e testando trocas na ordem dos nós para ver se o custo cai, isso é Exploitation, porque refina uma solução que já existe em vez de gerar uma nova do zero. Na prática, o 2-opt puxa o algoritmo mais para o lado da intensificação: mesmo que a formiga tenha escolhido um caminho mediano, a busca local corrige boa parte dos erros antes do feromônio ser atualizado, o que acelera a convergência, mas também diminui a diversidade das soluções ao longo das iterações.

2- O que aconteceria com a convergência do algoritmo se a taxa de evaporação (rho) fosse definida em 0.0 (sem evaporação)?

Sem evaporação, o feromônio de cada aresta só cresce, nunca diminui. Os primeiros caminhos razoáveis encontrados acumulam feromônio e continuam atraindo as formigas nas iterações seguintes, porque o rastro nunca perde força. O algoritmo tende a convergir mais rápido, só que para uma solução que pode não ser a melhor possível, ele fica preso no primeiro mínimo local encontrado, sem abrir espaço para novas explorações. A evaporação é justamente o que evita essa estagnação.

---

## LAB 02 — Algoritmo Genético: Seleção, Crossover e Mutação

**Output da execução:**
```
[LAB 02] Execute e teste o seu algoritmo preenchido!
[LAB 02] Melhor indivíduo encontrado: [0 1 1 1 1]
[LAB 02] Peso total: 8 / 15
[LAB 02] Valor (Fitness) total: 15
```

**Questões técnicas**

1- Explique qual é o papel do operador de Mutação em um Algoritmo Genético e o que ocorre se a taxa de mutação for configurada em 100%.

A mutação serve para inserir variação genética que não veio dos pais, evitando que a população fique presa em soluções parecidas e ajudando a escapar de mínimos locais, é o mecanismo de Exploration do AG. Se a taxa de mutação fosse 100%, todo gene de todo filho seria invertido sempre, o que destrói a herança genética vinda dos pais. O crossover perde o sentido, porque tudo acaba sendo invertido de qualquer jeito, e o algoritmo vira, na prática, uma busca aleatória. A convergência para uma boa solução fica praticamente impossível, já que a população nunca se estabiliza.

2- Por que a penalização do fitness (atribuir 0 para indivíduos que estouram a capacidade) é fundamental para a convergência das restrições?

Se um indivíduo que ultrapassa o peso máximo recebesse um fitness normal (ou até mais alto, já que carrega mais itens), a seleção por torneio continuaria escolhendo indivíduos inválidos para reproduzir, e a restrição de capacidade da mochila nunca seria respeitada. Zerando o fitness desses indivíduos, a seleção por torneio praticamente os elimina da reprodução ao longo das gerações, e a população converge naturalmente para soluções dentro do limite de peso. É a penalização que ensina o algoritmo, via pressão seletiva, o que é uma solução viável.

---

## LAB 03 — PSO: Inércia, Componente Cognitiva e Social

**Output da execução:**
```
[LAB 03] Melhor posição encontrada pelo Enxame (gbest): [-0.00065973 -0.0744211 ]
```

**Questões técnicas**

1- O que acontece com o comportamento das partículas se zerarmos a componente cognitiva (c1 = 0)?

Zerando c1, a partícula perde a própria memória, ela deixa de se importar com a melhor posição que ela mesma já visitou (pbest) e passa a se guiar só pela inércia e pela componente social (gbest, o melhor ponto de todo o enxame). Isso faz o enxame convergir mais rápido para a região do gbest, já que todas as partículas são puxadas para o mesmo lugar, mas aumenta o risco de convergência prematura: se o gbest atual não for o mínimo global de fato, o enxame inteiro pode ficar preso ali, sem ninguém explorando individualmente outras regiões.

2- Qual a função do parâmetro de Inércia (w) na busca por mínimos globais?

A inércia controla o quanto a partícula mantém a direção de movimento que já tinha, funcionando como um freio ou acelerador da busca. Com w alto, a partícula tende a manter a direção por mais tempo, favorecendo Exploration (varre mais o espaço antes de se fixar). Com w baixo, a velocidade decai mais rápido e a partícula se ajusta com mais facilidade em torno do pbest/gbest, favorecendo Exploitation. Por isso é comum começar com w mais alto e ir reduzindo ao longo das iterações, explora no começo, refina no final.

---

## LAB 04 — ACO: Feromônio, Evaporação e Atratividade

**Output da execução:**
```
[LAB 04] Matriz de Feromônio Atualizada:
 [[0.75       0.91666667 0.91666667 0.75      ]
 [0.75       0.75       0.75       1.08333333]
 [0.75       0.91666667 0.75       0.75      ]
 [0.75       0.75       0.75       0.75      ]]
```

**Questões técnicas**

1- Por que a evaporação do feromônio é necessária no algoritmo ACO?

A evaporação evita que o algoritmo fique preso nos primeiros caminhos encontrados. Sem ela, o feromônio de uma aresta só aumenta, então caminhos que pareciam bons no início continuam sendo escolhidos mesmo que existam alternativas melhores. Evaporando aos poucos, o feromônio de caminhos que não são mais reforçados vai perdendo força, abrindo espaço para a colônia experimentar outras rotas.

2- O que ocorreria em grafos complexos sem ela? Qual a relação matemática entre a latência de um enlace e sua atratividade inicial (eta) para as formigas?

Em grafos grandes e com muitas rotas possíveis, sem evaporação o algoritmo tende a convergir cedo demais para o primeiro caminho razoável encontrado pelas primeiras formigas, porque esse caminho acumula feromônio indefinidamente e domina a escolha das formigas seguintes, perde-se a chance de explorar rotas alternativas que poderiam ser melhores. Sobre a relação matemática: a atratividade heurística é o inverso do custo, ou seja, eta_ij = 1 / custo_ij. Então quanto menor a latência entre dois roteadores, maior o eta daquela aresta, mesmo antes de qualquer feromônio ser depositado, as formigas já tendem a preferir os enlaces de menor latência.

---

## LAB 05 — Memético: Meta-heurística + Busca Local

**Output da execução:**
```
[LAB 05] Solução Inicial: [ 2.5 -3.1] | Fitness: 37.7698
[LAB 05] Solução Refinada: [ 2.49789411 -3.06120518] | Fitness: 36.3400
```

**Questões técnicas**

1- Qual a diferença fundamental de conceito entre um Algoritmo Genético Puro e um Algoritmo Memético?

O AG puro trabalha só com os operadores evolutivos, seleção, crossover e mutação, e depende inteiramente da população e das gerações para melhorar as soluções, sem nenhum refinamento adicional. O Algoritmo Memético pega essa mesma lógica evolutiva (pode ser um AG, um ACO etc.) e adiciona uma busca local logo depois que cada solução é gerada, refinando individualmente cada indivíduo antes de seguir para a próxima etapa. Ou seja, o memético combina busca global (evolução da população) com busca local (aprendizado individual de cada solução), o que costuma trazer mais precisão e convergência mais rápida, ao custo de mais processamento.

2- Em termos de custo computacional, qual o impacto de executar a busca local sobre todos os indivíduos de uma população a cada geração?

O custo cresce bastante. Além de avaliar o fitness de cada indivíduo (como no AG puro), também é preciso rodar várias iterações de busca local (no nosso caso, até 20 passos de hill climbing) para cada indivíduo, em cada geração. Se a população tem N indivíduos e a busca local usa M passos, o custo por geração passa a ser proporcional a N × M, o que pode deixar a execução bem mais lenta em populações grandes ou com muitas gerações. Por isso, em problemas reais é comum aplicar a busca local só nos melhores indivíduos, e não em todos, para equilibrar qualidade da solução com tempo de execução.
