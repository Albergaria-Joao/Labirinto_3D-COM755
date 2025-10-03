import numpy as np
from collections import deque
from plot_caminho import plotar
import time
import heapq

P = 100
T = 150
S = 200

# ALGORITMO DFS (DEPTH-FIRST SEARCH) = Busca em profundidade
# É um algoritmo recursivo. No 100, atingiu o limite máximo (deu stack overflow). Mas no 10, teve um tempo de execução bem melhor que todos os outros

# Carregar o labirinto salvo
labirinto = np.load("Labirintos/labirinto100.npy")
N = labirinto.shape[0]

# Direções possíveis em 3D (6 vizinhos)
direcoes = [(1, 0, 0), (-1, 0, 0), # esquerda-direita
            (0, 1, 0), (0, -1, 0), # frente-trás
            (0, 0, 1), (0, 0, -1)] # cima-baixo

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

# Ponto de início (colocamos fixado no 0 para testes)
inicio = (0,0,0)
# inicio = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))
# while labirinto[inicio] == P:
#     inicio = (random.randint(0, N-1), random.randint(0, N-1), random.randint(0, N-1))

def distancia(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])

print(f"Início: {inicio}")
print(f"Saída: {saida}")

visitados = set()
caminho = []

def dfs(atual):
    x, y, z = atual

    # Se achou a saída
    if atual == saida:
        caminho.append(atual)
        return True

    visitados.add(atual)

    for dx, dy, dz in direcoes:
        nx, ny, nz = x+dx, y+dy, z+dz
        if 0 <= nx < N and 0 <= ny < N and 0 <= nz < N:
            if labirinto[nx][ny][nz] != P and (nx, ny, nz) not in visitados:
                caminho.append(atual) # Adiciona o atual ao caminho
                if dfs((nx, ny, nz)): # Aplica recursão para verificar nesse vizinho
                    return True 
                # Backtrack se ficar sem saída
                caminho.pop()

    return False

start_time = time.time() # Inicia o timer
# Executar
if dfs(inicio):
    print("Saída encontrada!")
    print("Caminho:", caminho)
else:
    print("Sem saída")
end_time = time.time()
elapsed_time = end_time - start_time
print("ENCONTROU SAÍDA")


plotar("Autoral", labirinto, [], inicio, saida, elapsed_time, caminho)