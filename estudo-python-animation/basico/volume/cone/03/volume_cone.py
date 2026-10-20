"""
Animação do Cálculo do Volume de um Cone usando 1 Método de Integração
======================================================================

Mostra visualmente como calcular V = (1/3)πr²h usando:
1. Cascas cilíndricas (variando ρ)

Autor: Ivan Carlos Lopes
"""

from matplotlib import pyplot, animation, cm, patches, path
import numpy as np

# Configuração de fontes para renderização matemática elegante
pyplot.rcParams.update({"font.family": "sans-serif", "mathtext.fontset": "cm"})


def c32(xyz):
    """
    Projeção isométrica (cavaleira) 3D → 2D
    """
    return np.array([
        xyz[1] - xyz[0] * np.sin(np.pi/4) / 2,
        xyz[2] - xyz[0] * np.cos(np.pi/4) / 2
    ])


# ==============================================================================
# CONFIGURAÇÃO DA ANIMAÇÃO
# ==============================================================================

Nf = 1000
cl = list(cm.tab10.colors)

fig = pyplot.figure(figsize=([9, 9]))

# Zoom (cone maior na tela)
xlim = [-0.9, 0.9]
ylim = [-0.35, 1.15]

ax1 = fig.add_axes([0, 0, 1, 1], xlim=xlim, ylim=ylim, fc='none')
ax1.axis('off')

ax = fig.add_axes([0, 0, 1, 1], xlim=xlim, ylim=ylim, fc='none')
ax.axis('off')

# Título
ax.text(np.sum(xlim)/2, ylim[1] - 0.05, 'Método das Cascas cilíndricas',
        size=35, ha='center', va='top')


# ==============================================================================
# PARÂMETROS GEOMÉTRICOS
# ==============================================================================

t1 = np.pi - np.atan(2*np.sqrt(2))
t2 = t1 + np.pi
theta = np.linspace(t1, t2, 100)

# Cone centralizado
xy = np.array([
    [0.0, 0.05],
])

xm, ym, zm = .8, .8, .9

r = .5
h = .8

rho = np.linspace(0, r, Nf)


# ==============================================================================
# DESENHO DA ESTRUTURA ESTÁTICA (1 CONE)
# ==============================================================================

for k in range(1):
    # Eixos
    axes_vectors = [
        c32([xm, 0, 0]),
        c32([0, ym, 0]),
        c32([0, 0, zm])
    ]

    for axis_vec in axes_vectors:
        ax.annotate('',
                    xy[k] + axis_vec,
                    xy[k],
                    arrowprops=dict(arrowstyle='->', lw=1, color='k'))

    # Contorno da base
    ax.plot(xy[k][0] + r*c32([np.cos(theta), np.sin(theta), 0*theta])[0],
            xy[k][1] + r*c32([np.cos(theta), np.sin(theta), 0*theta])[1],
            '--', c=cl[0], lw=1.2, alpha=.6)

    ax.plot(xy[k][0] + r*c32([-np.cos(theta), -np.sin(theta), 0*theta])[0],
            xy[k][1] + r*c32([-np.cos(theta), -np.sin(theta), 0*theta])[1],
            '-', c=cl[0], lw=2, alpha=.6)

    # Arestas laterais
    for i in range(2):
        edge_angle = t1 + np.pi * i
        base_point = xy[k] + c32([r*np.cos(edge_angle),
                                  r*np.sin(edge_angle), 0])
        apex_point = xy[k] + [0, h]
        ax.plot([base_point[0], apex_point[0]],
                [base_point[1], apex_point[1]],
                c=cl[0], lw=1, alpha=.6)

    # Linha do raio e rótulos r/h
    ax.plot([xy[k][0], xy[k][0] + r*c32([np.cos(t1), np.sin(t1), 0])[0]],
            [xy[k][1], xy[k][1] + r*c32([np.cos(t1), np.sin(t1), 0])[1]],
            '--', c='k', lw=1.2)

    ax.text(xy[k][0] + r*c32([np.cos(t1), np.sin(t1), 0])[0]/2,
            xy[k][1] + r*c32([np.cos(t1), np.sin(t1), 0])[1]/2,
            '$r$', size=25, c='k', ha='center', va='bottom')

    ax.text(xy[k][0], xy[k][1] + h/2,
            '$h$', size=25, c='k', ha='right', va='center')

    # ---------------------
    # Fórmulas na BASE (uma linha, lado a lado)
    # ---------------------
    # perto da borda inferior, mas dentro do quadro
    y_formula = ylim[0] + 0.03
    # espaçamento horizontal (cabe no xlim atual)
    dx = 0.62

    ax.text(xy[k][0] - dx, y_formula,
            r'$dV=2\pi\rho\left(h-\frac{h}{r}\rho\right)d\rho$',
            size=20, ha='center', va='bottom',
            bbox=dict(boxstyle='round', pad=0.25,
                      facecolor='none', edgecolor=cl[1], lw=3))

    ax.text(xy[k][0], y_formula,
            r'$V=\int_0^r 2\pi\rho\left(h-\frac{h}{r}\rho\right)\, d\rho$',
            size=20, ha='center', va='bottom',
            bbox=dict(boxstyle='round', pad=0.25,
                      facecolor='none', edgecolor=cl[0], lw=3))

    ax.text(xy[k][0] + dx, y_formula,
            r'$V=\frac{1}{3}\pi r^2h$',
            size=20, ha='center', va='bottom',
            bbox=dict(boxstyle='round', pad=0.30,
                      facecolor='none', edgecolor=cl[2], lw=5))


# ==============================================================================
# FUNÇÃO DE ANIMAÇÃO
# ==============================================================================

def animate(i):

    if i % 50 == 0:
        print(f"Frame {i}/{Nf}")

    ax1.cla()
    ax1.set_xlim(xlim)
    ax1.set_ylim(ylim)
    ax1.axis('off')

    # Casca cilíndrica
    verts = []
    for t in theta + np.pi:
        verts.append(xy[0] + c32([rho[i]*np.cos(t), rho[i]*np.sin(t), 0]))

    for t in reversed(theta + np.pi):
        z_top = h - h/r * rho[i]
        verts.append(xy[0] + c32([rho[i]*np.cos(t), rho[i]*np.sin(t), z_top]))

    verts.append((0, 0))

    codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
        (len(verts)-2) + [path.Path.CLOSEPOLY]
    ax1.add_patch(patches.PathPatch(
        path.Path(verts, codes),
        fc=cl[1], ec='none', alpha=.8, zorder=1
    ))

    # Círculo superior
    z_top = h - h/r * rho[i]
    ax1.plot(
        xy[0][0] + c32([rho[i]*np.cos(theta), rho[i] *
                       np.sin(theta), 0*theta + z_top])[0],
        xy[0][1] + c32([rho[i]*np.cos(theta), rho[i] *
                       np.sin(theta), 0*theta + z_top])[1],
        '--', c=cl[1], lw=1.2, zorder=-2
    )

    # Volume acumulado (cone interno até ρ)
    verts = []
    for t in theta + np.pi:
        verts.append(xy[0] + c32([rho[i]*np.cos(t), rho[i]*np.sin(t), z_top]))
    verts.append(xy[0] + c32([0, 0, h]))
    verts.append((0, 0))

    codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
        (len(verts)-2) + [path.Path.CLOSEPOLY]
    ax1.add_patch(patches.PathPatch(
        path.Path(verts, codes),
        fc=cl[0], ec='none', alpha=.8, zorder=1
    ))

    return []


# ==============================================================================
# RENDERIZAÇÃO E SALVAMENTO
# ==============================================================================

# Assinatura
ax.text(np.average(ax.get_xlim()),
        ylim[0] + 0.005,
        r'@Ivan Lopes',
        size=12, c='.2', alpha=.3, ha='center', va='bottom')

anim = animation.FuncAnimation(fig, animate, frames=Nf, interval=20)

print("Salvando animação...")
anim.save("volume_cone.mp4", writer=animation.FFMpegWriter(fps=60), dpi=200)
print("✓ Animação salva: volume_cone.mp4")
