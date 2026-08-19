# Resultados — Aula 03 — CIAO
*Grupo:*  _Gabriela Camarço de Sousa_, _Igor Ferreira Alves_ e _Luis Gustavo dos Santos Talgatti._ 
---

## Lab 01 - Algoritmo Genético 

**Problema:** achar o x que maximiza f(x) = x² no intervalo [0, 31], usando cromossomo binário de 5 bits.
**Configuração:** população de 6 indivíduos, 8 gerações, seleção por roleta, elitismo de 1 indivíduo, taxa de mutação de 10%.

### Resultados

A população inicial veio bem espalhada, com indivíduos ruins (x=1, f(x)=1) e um razoável (x=24, f(x)=576):

```
População inicial: [[0,0,0,1,0], [1,0,1,1,0], [1,1,0,0,0], [1,1,0,0,0], [1,0,1,0,0], [0,0,0,0,1]]
```

Acompanhando o melhor indivíduo de cada geração:

| Geração | Melhor x | f(x) |
|---|---|---|
| 0 | 24 | 576 |
| 2 | 29 | 841 |
| 3 | 30 | 900 |
| 5 | 31 | 961 (ótimo) |
| 7 | 31 | 961 (ótimo) |

O AG chegou no ótimo global (x=31, f(x)=961) já na geração 5 e ficou estável até o final, com erro final igual a 0.

<img width="935" height="430" alt="image" src="https://github.com/user-attachments/assets/1dabdbb0-5587-454a-aece-5e47f17d044b" />


### Considerações do grupo

Com um problema pequeno desse jeito (só 32 valores possíveis de x, de 0 a 31), fez sentido o AG achar o ótimo rápido, em poucas gerações. Dava até pra resolver esse problema testando os 32 valores um por um, mas o objetivo do laboratório era mesmo entender o passo a passo do algoritmo, não resolver um problema difícil.

O que ficou mais claro pra gente foi o papel do elitismo: como o melhor indivíduo de cada geração é sempre copiado direto pra próxima (sem passar por crossover ou mutação), o fitness nunca piora de uma geração pra outra. Dá pra ver isso no gráfico, a linha azul só sobe ou fica igual, nunca cai.

Outra coisa que reparamos: entre a geração 0 e a 1 o melhor fitness ficou igual (576), mas olhando a população dava pra ver que ela ficou bem parecida (quase todos os indivíduos eram [1,1,0,0,0]). Isso é a seleção por roleta favorecendo o indivíduo mais forte, mas ao mesmo tempo mostra o risco de perder diversidade rápido demais nesse tipo de seleção.

---

## Lab 02 - OneMax

**Problema:** OneMax, maximizar a quantidade de 1s em um cromossomo de 20 bits. 

**Configuração:** população de 30 indivíduos, 50 gerações, seleção por torneio (3 candidatos), crossover com 85% de chance, mutação com 2% de chance, elitismo de 2 indivíduos.

### Resultados

```
Geração   0: Melhor = 15/20, Média = 10.87
Geração  10: Melhor = 19/20, Média = 17.77
Geração  20: Melhor = 20/20, Média = 19.80
Geração  30: Melhor = 20/20, Média = 19.53
Geração  40: Melhor = 20/20, Média = 19.77

MELHOR FITNESS: 20/20
Ótimo = 20 (todos os bits são 1)
```

O AG chegou no cromossomo ótimo (todos os 20 bits em 1) por volta da geração 20 e manteve esse resultado até a geração 50.

<img width="1306" height="426" alt="image" src="https://github.com/user-attachments/assets/df006477-c9cc-45b6-bc56-20e86e04f6c8" />


### Considerações do grupo

Dá pra ver bem a diferença entre a linha do melhor indivíduo e a linha da média da população no gráfico. O melhor sobe rápido e "trava" em 20 assim que acha a solução ótima (de novo, por causa do elitismo). Já a média sobe mais devagar e fica oscilando (19.80, depois 19.53, depois 19.77) mesmo depois do ótimo já ter sido encontrado. Isso é a mutação continuando a agir na população inteira, inclusive nos filhos "bons" - de vez em quando ela estraga um bit que estava certo, e por isso a média não fica travada em 20 igual o melhor.

Sobre o desafio proposto no final do código (mudar TAXA_MUT, POPULACAO, GERACOES, ELITE), entendemos o seguinte a partir do que vimos na aula e no material:
- Aumentar a taxa de mutação demais tende a atrapalhar depois que a população já está próxima do ótimo, porque passa a estragar soluções boas com mais frequência.
- Diminuir a população reduz a diversidade de indivíduos disponíveis pra seleção e crossover, o que pode fazer o AG convergir mais devagar ou travar num resultado que não é o ótimo.
- Zerar o elitismo é arriscado porque nada garante que o melhor indivíduo de uma geração sobreviva pra próxima - ele pode não ser selecionado ou pode ser destruído pelo crossover/mutação, e nesse caso o fitness do melhor pode até piorar de uma geração pra outra.

---

## Lab 03 - Completando o Algoritmo Genético

**Problema:** achar o x no intervalo [0, 10] que maximiza f(x) = x·sen(3x), usando cromossomo binário de 8 bits (256 valores possíveis).
**Configuração:** população de 20 indivíduos, 50 gerações, seleção por roleta, crossover com 80% de chance, mutação com 5% de chance, elitismo de 2 indivíduos.

Esse laboratório veio com três funções incompletas (Todos), que o grupo precisou terminar:

1. **`bits_para_x`** - converte a lista de 8 bits pra decimal (mesma lógica de conversão binário→decimal do Lab 01) e depois normaliza esse valor pro intervalo [0, 10], já que 8 bits representam números de 0 a 255.
2. **`fitness`** - chama o `bits_para_x` pra saber o x do indivíduo e devolve `funcao_objetivo(x)`.
3. **`mutacao`** - percorre cada bit do indivíduo e inverte (0 vira 1, 1 vira 0) com probabilidade `TAXA_MUT`, igual ao que já tinha no Lab 01.

### Resultados

```
Geração   0: Melhor f(x) = 6.8149 (x = 6.8235)
Geração  10: Melhor f(x) = 6.8149 (x = 6.8235)
Geração  20: Melhor f(x) = 8.8769 (x = 8.9412)
Geração  30: Melhor f(x) = 8.8769 (x = 8.9412)
Geração  40: Melhor f(x) = 8.8769 (x = 8.9412)

MELHOR SOLUÇÃO: x = 8.9412, f(x) = 8.8769
```

<img width="1308" height="536" alt="image" src="https://github.com/user-attachments/assets/508397f8-b014-4dda-92de-9db17020f550" />


### Considerações do grupo

Esse foi o laboratório mais interessante dos três porque a função f(x) = x·sen(3x) tem vários picos (máximos locais) no intervalo [0, 10], então dava pra ver o AG realmente "procurando" a melhor solução, e não só melhorando de forma constante como nos outros dois.

Olhando o gráfico da esquerda, dá pra perceber que o pico onde o algoritmo ficou parado do início até por volta da geração 10 (perto de x=6.82) não é o pico mais alto da função - é só o segundo maior. O pico mais alto de verdade fica perto de x=8.9. O algoritmo ficou "preso" nesse ótimo local por um tempo e só escapou dele por volta da geração 20, muito provavelmente graças à mutação, já que sem ela a população tenderia a ficar cada vez mais parecida em torno da melhor solução já encontrada. Esse foi um exemplo bem prático do que o material da aula chama de mínimo (ou nesse caso, máximo) local, e do porquê a mutação existe mesmo sendo usada com uma taxa baixa.

O resultado final (x = 8.9412, f(x) = 8.8769) ficou bem perto do máximo real da função nesse intervalo, que é aproximadamente x = 8.91 e f(x) = 8.91. A pequena diferença acontece porque com 8 bits só é possível representar 256 valores de x igualmente espaçados entre 0 e 10 - ou seja, existe um limite de precisão que vem direto da representação escolhida, e não é um erro do algoritmo em si.

---

## Considerações gerais do grupo

Fazendo os três laboratórios em sequência, deu pra perceber que o "esqueleto" do AG é sempre o mesmo (criar população, avaliar, selecionar, cruzar, mutar, repetir), e o que muda de um problema pro outro é basicamente: como o cromossomo representa a solução, como a função de fitness é calculada e, em alguns casos, o método de seleção usado (roleta no Lab 01 e no Lab 03, torneio no Lab 02).

O Lab 03 ajudou bastante a fixar o conteúdo porque, pra completar os TODOs, tivemos que entender de verdade a lógica de cada função em vez de só ler e rodar um código pronto.
