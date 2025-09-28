import numpy as np
import heapq
import random
from collections import deque
from plot_caminho import plotar
import time


P = 100
T = 150
S = 200

# Carregar o labirinto salvo
labirinto = np.load("labirinto100.npy")
N = labirinto.shape[0]

# Direções possíveis em 3D (6 vizinhos)
direcoes = [(1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)]

# Encontrar saída e teleportes
saida = None
teleportes = []

for x in range(N):
    for y in range(N):
        for z in range(N):
            if labirinto[x][y][z] == S:
                saida = (x, y, z)
            elif labirinto[x][y][z] == T:
                teleportes.append((x, y, z))

if saida is None:
    print("Erro: Saída (S) não encontrada.")
    exit()

# Ponto de início (aleatório válido)

inicio = (0,0,0)
# inicio = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
# while labirinto[inicio] == P:
#     inicio = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))

print(f"Início: {inicio}")
print(f"Saída: {saida}")

# BFS
fila = deque([inicio])
visitado = set([inicio])
prev = {}

encontrou = False

start_time = time.time()
while fila:
    atual = fila.popleft()
    if atual == saida:
        encontrou = True
        break

    x, y, z = atual

    # Movimentos normais
    for dx, dy, dz in direcoes:
        nx, ny, nz = x + dx, y + dy, z + dz
        if 0 <= nx < N and 0 <= ny < N and 0 <= nz < N:
            if labirinto[nx][ny][nz] != P and (nx, ny, nz) not in visitado:
                visitado.add((nx, ny, nz))
                prev[(nx, ny, nz)] = atual
                fila.append((nx, ny, nz))

    # Teleporte → volta ao início
    if labirinto[x][y][z] == T:
        if inicio not in visitado:
            visitado.add(inicio)
            prev[inicio] = atual
            fila.append(inicio)
end_time = time.time()
elapsed_time = end_time - start_time
# Reconstrução do caminho
if encontrou:
    caminho = []
    atual = saida
    while atual != inicio:
        caminho.append(atual)
        atual = prev[atual]
    caminho.append(inicio)
    caminho.reverse()

    print(f"Tamanho do menor caminho: {len(caminho)-1} passos")
    print("Caminho:")
    for passo in caminho:
        print(passo)
else:
    print("Não há caminho até a saída.")

#dist = np.full((N, N, N), np.inf)
plotar("BFS", prev, inicio, saida, elapsed_time)

