import numpy as np
import matplotlib.pyplot as plt


# ==============================================================
# 1. CRIANDO A CIRCUNFERÊNCIA (O "Plano de Voo" da Mosca)
# ==============================================================
raio = 1.0
pontos = 100  # Quanto mais pontos, mais "redondo" fica

# 1. Ângulo de 0 a 2*PI
theta = np.linspace(0, 2*np.pi, pontos)

# 2. Usando Euler: e^(i*theta)
# Em Python, o número imaginário 'i' é escrito como '1j'
z_complexo = raio * np.exp(1j * theta)

# 3. Extraindo as coordenadas
lista_x = z_complexo.real  # Parte Real (Cos)
lista_y = z_complexo.imag  # Parte Imaginária (Sin)

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
