import numpy as np
from collections import deque
from plot_caminho import plotar
import time


P = 100
T = 150
S = 200

# ALGORITMO DE BUSCA EM LARGURA

# Carregar o labirinto salvo
labirinto = np.load("labirinto100.npy")
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

print(f"Início: {inicio}")
print(f"Saída: {saida}")

# BFS
fila = deque([inicio])
# Deque = double-ended queue ==> pode remover elementos dos dois lados com complexidade de O(1)
visitado = set([inicio])
# Set - conjunto que não guarda valores repetidos e tem tempo de busca muito rápido
# Cria ambos já com o ponto de início dentro

prev = {}

encontrou = False

start_time = time.time() # Inicia o timer
while fila:
    atual = fila.popleft() # Pega o primeiro valor da fila como atual
    if atual == saida:
        encontrou = True # Para o ciclo se encontrar a saída
        break

    x, y, z = atual

    # Movimentos normais
    for dx, dy, dz in direcoes: # Faz isso para cada uma das direções possíveis. Ou seja, vai abrindo para cada um dos movimentos possíveis até encontrar a rota mais curta (que chega primeiro)
        nx, ny, nz = x + dx, y + dy, z + dz
        if 0 <= nx < N and 0 <= ny < N and 0 <= nz < N: # Se não for cair fora do labirinto
            if labirinto[nx][ny][nz] != P and (nx, ny, nz) not in visitado: # Se não for parede nem já tiver passado lá
                visitado.add((nx, ny, nz)) # Adiciona aos visitados
                prev[(nx, ny, nz)] = atual # Coloca o valor "atual" como o anterior deste que iremos agora (para reconstruir o caminho depois no gráfico)
                fila.append((nx, ny, nz)) # Adiciona o valor novo à fila de casas a serem visitadas

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
    soma_custo = 0
    while atual != inicio:
        caminho.append(atual)
        soma_custo += labirinto[atual]
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
plotar("BFS", labirinto, prev, inicio, saida, elapsed_time, [])

