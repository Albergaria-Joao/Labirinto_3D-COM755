import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D


# Constants
P = 100
T = 50
S = 200
N = 10

# 3D array
labirinto = np.zeros((N, N, N), dtype=int)

def preencher():
    max_val = 5
    min_val = -5

    for i in range(N):
        for j in range(N):
            for k in range(N):
                prob = random.randint(1, 10)
                if prob <= 4:
                    labirinto[i][j][k] = P
                else:
                    score = random.randint(min_val, max_val)
                    labirinto[i][j][k] = score
                print(labirinto[i][j][k], end="\t")
            print()
        print("\n\n")

preencher()


# Assuming `labirinto` is already filled
N = labirinto.shape[0]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create coordinates
x, y, z = np.indices((N+1, N+1, N+1))  # +1 for voxel plotting

# Normalize the values between -5 and 5 for color intensity
norm = colors.Normalize(vmin=-5, vmax=5)
cmap = plt.cm.Blues  # Blue colormap

# Create facecolors array
facecolors = np.empty(labirinto.shape, dtype=object)

for i in range(N):
    for j in range(N):
        for k in range(N):
            val = labirinto[i, j, k]
            if val == 100:  # Special P blocks
                facecolors[i, j, k] = 'red'
            else:
                # Map -5..5 to 0..1 for colormap
                facecolors[i, j, k] = cmap(norm(val))

# Plot voxels
ax.voxels(np.ones_like(labirinto, dtype=bool), facecolors=facecolors, edgecolor='k')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()