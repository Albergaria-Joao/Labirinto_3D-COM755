import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


P = 100
T = 150
S = 200

def plotar(alg, prev, inicio, saida, time):
    # Carregar labirinto
    labirinto = np.load("labirinto100.npy")
    N = labirinto.shape[0]

    # Aqui entra seu código de Dijkstra (não repito pra não poluir)

    # ---- Plotando ----
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plotar paredes
    #px, py, pz = np.where(labirinto == P)
    #ax.scatter(px, py, pz, c="black", marker="s", s=2, alpha=0.2, label="Parede")

    # Plotar teleportes
    tx, ty, tz = np.where(labirinto == T)
    ax.scatter(tx, ty, tz, c="magenta", marker="o", s=40, label="Teleporte")

    # Plotar saída
    sx, sy, sz = np.where(labirinto == S)
    ax.scatter(sx, sy, sz, c="green", marker="*", s=200, label="Saída")

    # Plotar caminho encontrado
    
    caminho = []
    atual = saida
    while atual != inicio:
        caminho.append(atual)
        
        atual = prev[atual]
    caminho.append(inicio)
    caminho.reverse()

    cx, cy, cz = zip(*caminho)
    ax.plot(cx, cy, cz, c="red", linewidth=3, label="Caminho")
    ax.scatter(cx, cy, cz, c="red", s=30)

    # Ajustes de visualização
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    ax.set_title(f"{alg} - {len(caminho)} passos - Tempo: {time:.6f} segundos")
    plt.show()


