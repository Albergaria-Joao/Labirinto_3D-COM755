import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider

P = 100
T = 150
S = 200
N = 100

# 3D array
labirinto = np.zeros((N, N, N), dtype=int)

def preencher():
    max_val = 5
    min_val = -5

    for i in range(N):
        for j in range(N):
            for k in range(N):
                prob = random.randint(1, 10)
                if prob <= 3:
                    labirinto[i][j][k] = P
                else:
                    score = random.randint(min_val, max_val)
                    labirinto[i][j][k] = score
                #print(labirinto[i][j][k], end="\t")
            # print()
        # print("\n\n")

preencher()



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
                
# Coloca de 1 a 2 teleportes
nT = random.randint(1, 5)
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

# Assuming labirinto is already filled
N = labirinto.shape[0]

# Normalization for blue values
norm = colors.Normalize(vmin=-5, vmax=5)
cmap = plt.cm.Blues

# Function to build the voxel plot for a given slice depth
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

# --- Setup figure ---
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection="3d")
plt.subplots_adjust(bottom=0.25)

# Initial plot
build_plot(ax, 0)

# Slider
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
slider = Slider(ax_slider, "Z-max", 0, N-1, valinit=0, valstep=1)

def update(val):
    build_plot(ax, int(slider.val))
    fig.canvas.draw_idle()

slider.on_changed(update)

#
# Salvar a matriz para usar no outro código
salvar = input("Salvar? <S/n>   ")
if salvar != "n" and salvar != "N":
    np.save("labirinto100.npy", labirinto)

# p/ carregar depois
# labirinto_loaded = np.load("labirinto.npy")

plt.show()

