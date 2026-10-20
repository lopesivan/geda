from matplotlib import pyplot, patheffects

fig = pyplot.figure(figsize=(12, 4))
ax = fig.add_axes([0, 0, 1, 1], xlim=[0, 1], ylim=[0, 1], fc='#222')
ax.axis('off')

txt = ax.text(
    0.5, 0.5,
    'Bom dia! Desejo que a sua manhã seja tão bela e especial quanto você e o seu coração. ',
    fontsize=90,
    ha='center', va='center',
    fontweight='bold',
    color='#FFD700',
)

# Contorno preto ao redor das letras
txt.set_path_effects([
    patheffects.withStroke(linewidth=6, foreground='black')
])

pyplot.savefig("02-exemplo.png", dpi=150, bbox_inches='tight')
# pyplot.show()
