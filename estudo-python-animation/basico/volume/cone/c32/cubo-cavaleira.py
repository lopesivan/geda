import numpy as np
import matplotlib.pyplot as plt


def c32(xyz):
    """
    Projeção Cavaleira (3D -> 2D)
    Recebe matriz (3, N), retorna matriz (2, N)
    """
    xyz = np.array(xyz)
    x, y, z = xyz[0], xyz[1], xyz[2]

    # O truque: o eixo X (profundidade) é projetado a 45°
    # O fator 0.5 encurta a profundidade para parecer mais natural
    x_2d = y - x * np.sin(np.pi/4) / 2
    y_2d = z - x * np.cos(np.pi/4) / 2

    return np.array([x_2d, y_2d])


# 1. Definindo as arestas de um cubo unitário no R3
# Cada tupla representa uma linha entre dois pontos (x, y, z)
arestas_3d = [
    ([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0]),  # Base inferior (Z=0)
    ([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [1, 1, 1, 1, 1]),  # Base superior (Z=1)
    ([0, 0], [0, 0], [0, 1]),  # Coluna 1
    ([1, 1], [0, 0], [0, 1]),  # Coluna 2
    ([1, 1], [1, 1], [0, 1]),  # Coluna 3
    ([0, 0], [1, 1], [0, 1]),  # Coluna 4
]

# 2. Configuração do gráfico
plt.figure(figsize=(8, 8))
plt.axhline(0, color='black', lw=1, alpha=0.3)
plt.axvline(0, color='black', lw=1, alpha=0.3)

# 3. Projetando e desenhando cada aresta
for x_coords, y_coords, z_coords in arestas_3d:
    # Convertendo os pontos da aresta de 3D para 2D
    pontos_3d = np.array([x_coords, y_coords, z_coords])
    pontos_2d = c32(pontos_3d)

    plt.plot(pontos_2d[0], pontos_2d[1], 'bo-', lw=2)

# 4. Desenhando os eixos projetados para referência
eixos_3d = np.array([
    [1, 0, 0],  # Eixo X (Vermelho) - Profundidade
    [0, 1, 0],  # Eixo Y (Verde) - Horizontal
    [0, 0, 1]  # Eixo Z (Azul) - Vertical
]).T

labels = ['X (Profundidade)', 'Y (Horizontal)', 'Z (Vertical)']
cores = ['r', 'g', 'b']

for i in range(3):
    # Projeta a ponta do vetor unitário de cada eixo
    ponta = c32(eixos_3d[:, i].reshape(3, 1))
    plt.arrow(0, 0, ponta[0, 0], ponta[1, 0], color=cores[i],
              head_width=0.05, label=labels[i])

plt.title("Projeção de um Cubo R3 -> R2 (Perspectiva Cavaleira)")
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.axis('equal')
plt.show()
