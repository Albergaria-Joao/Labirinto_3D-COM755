import numpy as np
import random
import matplotlib.pyplot as plt
import time
from plot_caminho import plotar

P = 100
T = 150
S = 200


labirinto = np.load("Labirintos/labirinto100.npy")
N = labirinto.shape[0]


direcoes = [(1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)]


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
    print("Erro: Saída (S) não encontrada no labirinto.")
    exit()

inicio = (0, 0, 0)


dist = np.full((N, N, N), np.inf)
dist[inicio] = 0
prev = {}

# Algoritmo de BELLMAN-FORD
# Acaba demorando bastante justamente pela ordem de complexidade

# Aqui, ele vai transformar o labirinto num grafo ==> cada célula é um nó, e ele vai criar arestas entre elas
arestas = []
for x in range(N):
    for y in range(N):
        for z in range(N):
            # Percorre o labirinto inteiro
            if labirinto[x][y][z] == P:
                continue # Se a célula atual for parede, continua
            for dx, dy, dz in direcoes:
                nx, ny, nz = x + dx, y + dy, z + dz # Olha as direções possíveis da célula
                if 0 <= nx < N and 0 <= ny < N and 0 <= nz < N:
                    if labirinto[nx][ny][nz] != P:
                        peso = abs(labirinto[nx][ny][nz]) if labirinto[nx][ny][nz] < T else 0
                        arestas.append(((x, y, z), (nx, ny, nz), peso)) # Cria uma aresta com peso equivalente ao módulo do valor da célula
            
            if labirinto[x][y][z] == T:
                arestas.append(((x, y, z), inicio, 1)) # Se for teletransporte, cria aresta com o início


start_time = time.time()
for _ in range(N**3 - 1): # Repete o número de nós - 1
    atualizado = False
    # Para cada aresta
    for u, v, peso in arestas: # u: de onde ele sai; v: aonde ele chega
        # dist[u] = distância mínima conhecida até o nó u
        # peso = custo da aresta de u até v
        # dist[v] = distância mínima conhecida até o nó v

        if dist[u] + peso < dist[v]: 
            # Se passando por u até chegar em v (dist u + peso) for melhor do que já tínhamos em dist v, encontramos um caminho mais curto
            dist[v] = dist[u] + peso
            prev[v] = u # Guarda quem foi o "pai" de cada nó/anterior para guardar o caminho percorrido
            # Marca que teve essa atualização no caminho
            atualizado = True
    if not atualizado:
        break
end_time = time.time()
elapsed_time = end_time - start_time


if dist[saida] == np.inf:
    print("Sem caminho até a saída.")
else:
    print(f"Custo mínimo até a saída: {dist[saida]}")
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

    plotar("Bellman-Ford", labirinto, prev, inicio, saida, elapsed_time, [])
