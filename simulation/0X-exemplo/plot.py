import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
    description="Plota os resultados da simulação RC.")
parser.add_argument("arquivo", help="Arquivo de dados gerado pelo ngspice")
args = parser.parse_args()

# Lê o título do arquivo .title no diretório atual.
arquivo_titulo = Path("title")
titulo = arquivo_titulo.read_text(
    encoding="utf-8").strip() if arquivo_titulo.is_file() else "Resposta do circuito RC"

data = np.loadtxt(args.arquivo, skiprows=1)

t = data[:, 0]
vin = data[:, 1]
vout = data[:, 2]

plt.plot(t * 1e3, vin, label="v(in)")
plt.plot(t * 1e3, vout, label="v(out)")

plt.xlabel("Tempo [ms]")
plt.ylabel("Tensão [V]")
plt.title(titulo)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
