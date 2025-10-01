import numpy as np
from collections import deque
from plot_caminho import plotar
import time
import random
import threading

P = 100
T = 150
S = 200

N_THREADS = 10

# ALGORITMO AUTORAL 3
#AINDA EM TESTE

# Carregar o labirinto salvo
labirinto = np.load("labirinto10_2.npy")
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

caminhos = {}

def caminhar():
    start_thread_time = time.time()
    encontrou_saida = False

    visitados = [inicio]
    caminho_atual = [inicio]


    
    while encontrou_saida == False:
        if time.time() - start_thread_time > 300:
            break
        
        x, y, z = caminho_atual[-1]
        if (x, y, z) == saida:
            encontrou_saida = True
            break

        rd = direcoes
        random.shuffle(rd)
        for dx, dy, dz in rd:
        #print(proximo[0])
        # Faz isso para cada uma das direções possíveis. Ou seja, vai abrindo para cada um dos movimentos possíveis até encontrar a rota mais curta (que chega primeiro)
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < N and 0 <= ny < N and 0 <= nz < N:
                if labirinto[nx][ny][nz] != P and (nx, ny, nz) not in visitados: # Se não for parede nem já tiver passado lá
                    fechado = False
                    
                    visitados.append((nx, ny, nz))
                    caminho_atual.append((nx, ny, nz))
                    break # Vai sempre no primeiro caminho aberto que encontrar
                else: 
                    fechado = True 
        if (fechado == True):
            caminho_atual.pop() # Se ficar sem saída, ele volta 1 (backtracking) até achar um novo caminho aberto

        #print(caminho_atual[-1])
        #print(caminho_atual)
    
    if encontrou_saida:
        caminhos[len(caminho_atual)] = caminho_atual


start_time = time.time() # Inicia o timer

threads = []

for i in range(N_THREADS):
    threads.append(threading.Thread(target=caminhar))

for i in range(len(threads)):
    threads[i].start()

for i in range(len(threads)):
    threads[i].join()

#print(dict(caminhos))

caminhos_ordenados = dict(sorted(caminhos.items()))
#print(dict(caminhos_ordenados))
primeira_chave = next(iter(caminhos_ordenados))

melhor_caminho = caminhos_ordenados[primeira_chave]


end_time = time.time()
elapsed_time = end_time - start_time
print("ENCONTROU SAÍDA")

    
plotar("Autoral - Random com Threads", labirinto, [], inicio, saida, elapsed_time, melhor_caminho)