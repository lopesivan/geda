from matplotlib import pyplot

pyplot.rcParams.update({"font.family": "sans-serif", "mathtext.fontset": "cm"})

fig = pyplot.figure(figsize=(12, 4))
ax = fig.add_axes([0, 0, 1, 1], xlim=[0, 1], ylim=[0, 1], fc='none')
ax.axis('off')

ax.text(
    0.5, 0.5,
    'Bom dia! Desejo que a sua manhã seja tão bela e especial quanto você e o seu coração. ',
    fontsize=80,
    ha='center', va='center',
    fontweight='bold',
    color='#1f77b4',
)

pyplot.savefig("01-exemplo.png", dpi=150, bbox_inches='tight')
# pyplot.show()
