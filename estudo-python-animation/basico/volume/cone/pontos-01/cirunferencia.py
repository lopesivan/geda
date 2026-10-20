import numpy as np
import matplotlib.pyplot as plt


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

# Esta é a sua TUPLA (cada item é uma lista de coordenadas)
circunferencia_2d = (lista_x, lista_y)

# ==============================================================
# 2. DESENHANDO
# ==============================================================
plt.figure(figsize=(8, 8))

# Projetamos a tupla 3D para o plano 2D
pontos_2d = circunferencia_2d

# Desenhamos a linha (a caneta no papel)
plt.plot(pontos_2d[0], pontos_2d[1], color='blue',
         lw=2, label="Circunferência (Base do Cone)")

# Marcar o centro para referência
plt.plot(0, 0, 'ro')
plt.text(0.1, 0.1, "Centro (0,0)", color='red')

plt.title("Circunferência no R2")
plt.axis('equal')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.show()
