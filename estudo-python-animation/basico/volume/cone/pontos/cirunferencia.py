import numpy as np
import matplotlib.pyplot as plt


def c32(xyz):
    """ Projeção Cavaleira: 3D (x,y,z) -> 2D (x,y) """
    xyz = np.array(xyz)
    x, y, z = xyz[0], xyz[1], xyz[2]
    x_2d = y - x * np.sin(np.pi/4) / 2
    y_2d = z - x * np.cos(np.pi/4) / 2
    return np.array([x_2d, y_2d])


# ==============================================================
# 1. CRIANDO A CIRCUNFERÊNCIA (O "Plano de Voo" da Mosca)
# ==============================================================
raio = 1.0
pontos = 100  # Quanto mais pontos, mais "redondo" fica

# Criamos um ângulo que vai de 0 até 2*PI (uma volta completa)
theta = np.linspace(0, 2*np.pi, pontos)

# Geramos as listas de coordenadas para a tupla
# No R3, uma circunferência no "chão" tem Z sempre 0
lista_x = raio * np.cos(theta)
lista_y = raio * np.sin(theta)
lista_z = np.zeros_like(theta)

# Esta é a sua TUPLA (cada item é uma lista de coordenadas)
circunferencia_3d = (lista_x, lista_y, lista_z)

# ==============================================================
# 2. DESENHANDO
# ==============================================================
plt.figure(figsize=(8, 8))

# Projetamos a tupla 3D para o plano 2D
pontos_2d = c32(circunferencia_3d)

# Desenhamos a linha (a caneta no papel)
# pontos_2d[0] são todos os X projetados, pontos_2d[1] todos os Y
plt.plot(pontos_2d[0], pontos_2d[1], color='blue',
         lw=2, label="Circunferência (Base do Cone)")

# Marcar o centro para referência
plt.plot(0, 0, 'ro')
plt.text(0.1, 0.1, "Centro (0,0,0)", color='red')

plt.title("Circunferência no R3 projetada no R2")
plt.axis('equal')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()
