import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider
from collections import deque

P = 100
T = 150
S = 200
N = 10

PERCENTUAL_PAREDES = 60
NOME_ARQUIVO = "TESTE.npy"


labirinto = np.zeros((N, N, N), dtype=int)

def preencher():
    max_val = 5
    min_val = -5

    for i in range(N):
        for j in range(N):
            for k in range(N):
                prob = random.randint(1, 100)
                if prob <= PERCENTUAL_PAREDES:
                    labirinto[i][j][k] = P
                else:
                    score = random.randint(min_val, max_val)
                    labirinto[i][j][k] = score
                #print(labirinto[i][j][k], end="\t")
            # print()
        # print("\n\n")

    sPos = False
    # Coloca uma saída
    while sPos == False:
        xS = random.randint(0, N-1)
        yS = random.randint(0, N-1)
        zS = random.randint(0, N-1)

        if (labirinto[(xS - 1) % N][yS][zS] < P and labirinto[(xS + 1) % N][yS][zS] < P and
            labirinto[xS][(yS - 1) % N][zS] < P and labirinto[xS][(yS + 1) % N][zS] < P and 
            labirinto[xS][yS][(zS - 1) % N] < P and labirinto[xS][yS][(zS + 1) % N] < P):
            
            labirinto[xS][yS][zS] = S
            sPos = True    

    # labirinto[N - 1][N - 1][N - 1] = S          
    
    # Coloca de N a M teleportes
    nT = random.randint(1, 3)
    for i in range (nT):
        tPos = False
        while tPos == False:
            xT = random.randint(0, N-1)
            yT = random.randint(0, N-1)
            zT = random.randint(0, N-1)

            if (labirinto[(xT - 1) % N][yT][zT] < P and labirinto[(xT + 1) % N][yT][zT] < P and
                labirinto[xT][(yT - 1) % N][zT] < P and labirinto[xT][(yT + 1) % N][zT] < P and 
                labirinto[xT][yT][(zT - 1) % N] < P and labirinto[xT][yT][(zT + 1) % N] < P and
                labirinto[xT][yT][zT] != S):
                
                labirinto[xT][yT][zT] = T
                tPos = True    

def teste_bfs():
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

    return encontrou

encontrou = False
while encontrou == False:
    preencher()
    encontrou = teste_bfs()
    # Para garantir que existe pelo menos um caminho possível nesse labirinto, ele vai testar com um BFS
    

salvar = input("Salvar? <S/n>   ")
if salvar != "n" and salvar != "N":
    np.save(f"Labirintos/{NOME_ARQUIVO}", labirinto)



# PLOTAGEM

N = labirinto.shape[0]

# Normalization for blue values
norm = colors.Normalize(vmin=-5, vmax=5)
cmap = plt.cm.Blues

# Plotagem da matriz (com ajuda de IA)
def build_plot(ax, max_k):
    ax.clear()
    facecolors = np.empty(labirinto.shape, dtype=object)
    filled = np.zeros(labirinto.shape, dtype=bool)

    for i in range(N):
        for j in range(N):
            for k in range(max_k + 1):  # only show up to current slice
                val = labirinto[i, j, k]
                filled[i, j, k] = True
                if val == P:  # special P blocks
                    facecolors[i, j, k] = (1, 0, 0, 1.0)  # red, fully opaque
                elif val == S:
                    facecolors[i, j, k] = (0, 1, 0, 1.0)
                elif val == T:
                    facecolors[i, j, k] = (1, 1, 0, 1.0)
                else:
                    rgba = cmap(norm(val))  # (r,g,b,a)
                    facecolors[i, j, k] = (rgba[0], rgba[1], rgba[2], 0.6)  # semi-transparent blue

    ax.voxels(filled, facecolors=facecolors, edgecolor='k')

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(f"Showing layers up to Z={max_k}")

def plot():
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")
    plt.subplots_adjust(bottom=0.25)

    build_plot(ax, 0)

    # Slider
    ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
    slider = Slider(ax_slider, "Z-max", 0, N-1, valinit=0, valstep=1)

    def update(val):
        build_plot(ax, int(slider.val))
        fig.canvas.draw_idle()

    slider.on_changed(update)

    plt.show()

plot()





# labirinto ==> N = 10, 60% de paredes; saída aleatória
# labirinto10_2 ==> N = 100, 60% de paredes; saída no extremo superior
# labirinto100 ==> N = 100, 60% de paredes; saída aleatória
# labirinto100_2 ==> N = 100, 70% de paredes; saída no extremo superior