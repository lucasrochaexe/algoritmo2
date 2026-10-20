from collections import deque
from heapq import heappop, heappush


labirinto = [
    "I.#.#####.",
    ".##...##.#",
    "....#.....",
    ".#######.#",
    "..######..",
    ".########.",
    "####......",
    ".....#####",
    ".#.##F####",
    "##....####",
]

DIRECOES = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def livre(lab, i, j):
    dentro = 0 <= i < len(lab) and 0 <= j < len(lab[0])
    return dentro and lab[i][j] != "#"


def montar_grafo(lab):
    grafo = {}
    for i in range(len(lab)):
        for j in range(len(lab[0])):
            if not livre(lab, i, j):
                continue

            grafo[(i, j)] = []
            for di, dj in DIRECOES:
                vizinho = (i + di, j + dj)
                if livre(lab, *vizinho):
                    grafo[(i, j)].append(vizinho)
    return grafo


def achar(lab, simbolo):
    for i, linha in enumerate(lab):
        for j, valor in enumerate(linha):
            if valor == simbolo:
                return (i, j)
    raise ValueError(f"Marcador {simbolo!r} não encontrado.")


def reconstruir_caminho(anteriores, atual):
    caminho = []
    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]
    return caminho[::-1]


def dfs(grafo, inicio, saida):
    pilha = [inicio]
    anteriores = {inicio: None}
    visitadas = []

    while pilha:
        atual = pilha.pop()
        visitadas.append(atual)
        if atual == saida:
            return reconstruir_caminho(anteriores, atual), visitadas

        for vizinho in reversed(grafo[atual]):
            if vizinho not in anteriores:
                anteriores[vizinho] = atual
                pilha.append(vizinho)

    return [], visitadas


def bfs(grafo, inicio, saida):
    fila = deque([inicio])
    anteriores = {inicio: None}
    visitadas = []

    while fila:
        atual = fila.popleft()
        visitadas.append(atual)
        if atual == saida:
            return reconstruir_caminho(anteriores, atual), visitadas

        for vizinho in grafo[atual]:
            if vizinho not in anteriores:
                anteriores[vizinho] = atual
                fila.append(vizinho)

    return [], visitadas


def heuristica(posicao, destino):
    return abs(posicao[0] - destino[0]) + abs(posicao[1] - destino[1])


def gulosa(grafo, inicio, saida):
    fronteira = [(heuristica(inicio, saida), inicio)]
    anteriores = {inicio: None}
    visitadas = []

    while fronteira:
        _, atual = heappop(fronteira)
        visitadas.append(atual)
        if atual == saida:
            return reconstruir_caminho(anteriores, atual), visitadas

        for vizinho in grafo[atual]:
            if vizinho not in anteriores:
                anteriores[vizinho] = atual
                prioridade = heuristica(vizinho, saida)
                heappush(fronteira, (prioridade, vizinho))

    return [], visitadas


def desenhar(lab, caminho):
    grade = [list(linha) for linha in lab]
    for i, j in caminho:
        if grade[i][j] == ".":
            grade[i][j] = "*"
    for linha in grade:
        print("".join(linha))


def executar(nome, busca, grafo, inicio, saida):
    caminho, visitadas = busca(grafo, inicio, saida)
    print(f"\n===== {nome} =====")
    desenhar(labirinto, caminho)
    print(f"Tamanho do caminho: {len(caminho) - 1} movimentos")
    print(f"Casas visitadas: {len(visitadas)}")
    return len(caminho) - 1, len(visitadas)


grafo = montar_grafo(labirinto)
inicio = achar(labirinto, "I")
saida = achar(labirinto, "F")

resultados = {
    "DFS": executar("DFS", dfs, grafo, inicio, saida),
    "BFS": executar("BFS", bfs, grafo, inicio, saida),
    "Gulosa": executar("Gulosa", gulosa, grafo, inicio, saida),
}

print("\n====================================")
print(f"{'Busca':<10} {'Movimentos':>12} {'Visitadas':>12}")
for nome, (tamanho, visitadas) in resultados.items():
    print(f"{nome:<10} {tamanho:>12} {visitadas:>12}")
print("====================================")

'''
            RESULTADO
Busca        Movimentos    Visitadas
DFS                  31           36
BFS                  31           43
Gulosa               31           33
===================================='''