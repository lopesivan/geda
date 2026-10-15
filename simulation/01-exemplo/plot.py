import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
    description="Plota os resultados da simulação RC.")
parser.add_argument("arquivo", help="Arquivo de dados gerado pelo ngspice")
args = parser.parse_args()

data = np.loadtxt(args.arquivo, skiprows=1)

t = data[:, 0]
vin = data[:, 1]
vout = data[:, 2]

plt.plot(t * 1e3, vin, label="v(in)")
plt.plot(t * 1e3, vout, label="v(out)")

plt.xlabel("Tempo [ms]")
plt.ylabel("Tensão [V]")
plt.title("Resposta do circuito RC")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
