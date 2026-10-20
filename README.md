# Saída do Labirinto

Essa atividade implementa diferentes algoritmos de busca para encontrar um
caminho entre a entrada e a saída de um labirinto.

## Representação do labirinto

O labirinto é representado por uma lista de strings:

- `I`: entrada;
- `F`: saída;
- `#`: parede;
- `.`: casa livre.

Cada casa livre é considerada um vértice do grafo. Casas livres vizinhas são
ligadas por arestas, considerando os movimentos para cima, direita, baixo e
esquerda:

```python
DIRECOES = [(-1, 0), (0, 1), (1, 0), (0, -1)]
```

A função `montar_grafo` cria um dicionário de listas de adjacência com as
possíveis movimentações de cada casa.

## Algoritmos implementados

### DFS — busca em profundidade

A DFS utiliza uma pilha e segue por um caminho até onde for possível. Quando
encontra um beco sem saída, retorna e tenta outra direção. Esse algoritmo não
garante encontrar o menor caminho.

### BFS — busca em largura

A BFS utiliza uma fila e explora o labirinto por camadas, começando pela
entrada. Como cada movimento possui o mesmo custo, a primeira vez que a saída
é encontrada corresponde ao menor caminho possível.

### Busca gulosa

A busca gulosa utiliza uma fila de prioridade. Ela escolhe a casa que possui a
menor distância Manhattan até a saída:

```python
abs(linha_atual - linha_saida) + abs(coluna_atual - coluna_saida)
```

Essa heurística não considera as paredes. Por isso, a busca pode escolher
inicialmente uma casa que parece próxima da saída, mas que está bloqueada ou
faz parte de um beco sem saída.

## Reconstrução do caminho

Durante cada busca, o dicionário `anteriores` registra de qual casa cada
vértice foi alcançado:

```python
anteriores[vizinho] = atual
```

Quando a saída é encontrada, a função `reconstruir_caminho` percorre esse
dicionário começando pela saída e voltando até a entrada. Como esse percurso é
feito de trás para frente, a lista é invertida antes de ser exibida.

As casas pertencentes ao caminho são marcadas com `*` no desenho do labirinto.

## Resultados obtidos

Com o labirinto utilizado no projeto, os algoritmos produziram os seguintes
resultados:

| Busca | Movimentos | Casas visitadas |
| DFS   |      31      |        36     |
| BFS   |      31      |        43     |
| Gulosa|      31      |        33     |

Neste exemplo, os três algoritmos encontraram um caminho com 31 movimentos.
Isso não significa que todos possuem a mesma garantia: a BFS garante o menor
caminho em um grafo sem pesos, enquanto a DFS e a busca gulosa não oferecem
essa garantia.

A busca gulosa visitou menos casas neste caso, mas foi enganada inicialmente
pela casa `(0, 1)`. Embora essa casa parecesse aproximar a busca da saída, as
paredes em `(0, 2)` e `(1, 1)` impediam a continuação, fazendo com que o
algoritmo precisasse voltar e seguir por outra rota.

## Execução

Na pasta do projeto, execute:

```bash
python labirinto.py
```

O programa desenha o caminho encontrado por cada algoritmo e apresenta uma
tabela comparativa com a quantidade de movimentos e casas visitadas.
