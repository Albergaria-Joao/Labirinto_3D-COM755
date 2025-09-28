import numpy as np
import heapq
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import time
from plot_caminho import plotar

P = 100
T = 150
S = 200

# ALGORITMO DE DIJKSTRA - LEVA EM CONSIDERAÇÃO OS CUSTOS

# Carregar o labirinto salvo
labirinto = np.load("labirinto100.npy")
N = labirinto.shape[0]

# Direções possíveis em 3D (6 vizinhos)
direcoes = [(1, 0, 0), (-1, 0, 0), # esquerda-direita
            (0, 1, 0), (0, -1, 0), # frente-trás
            (0, 0, 1), (0, 0, -1)] # cima-baixo

# Encontrar a posição da saída e teleportes
saida = None
teleportes = []

for x in range(N):
    for y in range(N):
        for z in range(N):
            if labirinto[x][y][z] == S:
                saida = (x, y, z)
            elif labirinto[x][y][z] == T:
                teleportes.append((x, y, z))

# Verifica se achou a saída
if saida is None:
    print("Erro: Saída (S) não encontrada no labirinto.")
    exit()


# Ponto de início (colocamos fixado no 0 para testes)
inicio = (0,0,0)
# inicio = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
# while labirinto[inicio] == P or labirinto[inicio] == S:
#     print("Erro: Início está em uma parede.")
#     inicio = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))

# Dijkstra
dist = np.full((N, N, N), np.inf)
dist[inicio] = 0

prev = {}  # Para reconstruir caminho

heap = [(0, inicio)]

start_time = time.time()
while heap:
    custo, atual = heapq.heappop(heap)
    if atual == saida:
        break

    x, y, z = atual

    # Movimentos normais
    for dx, dy, dz in direcoes:
        nx, ny, nz = x + dx, y + dy, z + dz
        if 0 <= nx < N and 0 <= ny < N and 0 <= nz < N:
            val = labirinto[nx][ny][nz]
            if val == P:
                continue
            novo_custo = custo + abs(val) if val < T else custo  # No Dijkstra, as arestas devem ter peso não negativo
            if novo_custo < dist[nx][ny][nz]:
                dist[nx][ny][nz] = novo_custo
                prev[(nx, ny, nz)] = (x, y, z)
                heapq.heappush(heap, (novo_custo, (nx, ny, nz)))

    # Teleporte
    # Se atual é um teleporte, envia para o início
    if labirinto[x][y][z] == T:
        if custo + 1 < dist[inicio]:
            dist[inicio] = custo + 1
            prev[inicio] = (x, y, z)
            heapq.heappush(heap, (custo + 1, inicio))
end_time = time.time()
elapsed_time = end_time - start_time

# Verificar se encontrou a saída
if dist[saida] == np.inf:
    print("Sem caminho até a saída.")
else:
    print(f"Custo mínimo até a saída: {dist[saida]}")

    # Reconstruir caminho
    caminho = []
    atual = saida
    while atual != inicio:
        caminho.append(atual)
        atual = prev[atual]
    caminho.append(inicio)
    caminho.reverse()

    print("Caminho:")
    for passo in caminho:
        print(passo)


plotar("Dijkstra", prev, inicio, saida, elapsed_time)

