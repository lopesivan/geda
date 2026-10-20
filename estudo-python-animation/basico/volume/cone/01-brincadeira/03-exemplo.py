from matplotlib import pyplot, animation

fig = pyplot.figure(figsize=(12, 4))
ax = fig.add_axes([0, 0, 1, 1], xlim=[0, 1], ylim=[0, 1], fc='none')
ax.axis('off')

texto = "Bom dia! Desejo que a sua manhã seja tão bela e especial quanto você e o seu coração."
txt = ax.text(0.5, 0.5, '', fontsize=90, ha='center', va='center',
              fontweight='bold', color='#1f77b4')


def animate(i):
    txt.set_text(texto[:i+1])
    return [txt]


anim = animation.FuncAnimation(fig, animate, frames=len(texto), interval=150)
anim.save("03-exemplo.mp4", writer=animation.FFMpegWriter(fps=8), dpi=150)
