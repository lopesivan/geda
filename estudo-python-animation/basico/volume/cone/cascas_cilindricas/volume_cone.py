"""
Cálculo do Volume de um Cone usando Cascas Cilíndricas
======================================================

Mostra visualmente como calcular V = (1/3)πr²h usando integração
por cascas cilíndricas variando o raio ρ de 0 até r.

Método: dV = 2πρ·h(1-ρ/r)·dρ
Integral: V = ∫₀ʳ 2πρ(h - h/r·ρ) dρ = (1/3)πr²h

Autor: Ivan Carlos Lopes
"""

from matplotlib import pyplot, animation, cm, patches, path
import numpy as np

# Configuração de fontes para renderização matemática elegante
pyplot.rcParams.update({"font.family": "sans-serif", "mathtext.fontset": "cm"})


def c32(xyz):
    """
    Projeção isométrica (cavaleira) 3D → 2D

    Transforma coordenadas 3D (x, y, z) em coordenadas 2D para simular 3D
    usando projeção isométrica a 45°

    Args:
        xyz: array ou lista [x, y, z] com coordenadas 3D

    Returns:
        array [x_2d, y_2d] com coordenadas projetadas
    """
    return np.array([
        xyz[1] - xyz[0] * np.sin(np.pi/4) / 2,
        xyz[2] - xyz[0] * np.cos(np.pi/4) / 2
    ])


# ==============================================================================
# CONFIGURAÇÃO DA ANIMAÇÃO
# ==============================================================================

Nf = 100  # Número de frames
cl = list(cm.tab10.colors)  # Paleta de cores

# Criação da figura
fig = pyplot.figure(figsize=([12, 9]))
xlim = [-1.5, 1.5]
ylim = [-1.2, 1.2]

# Dois eixos: um para animação (ax1) e outro para elementos fixos (ax)
ax1 = fig.add_axes([0, 0, 1, 1], xlim=xlim, ylim=ylim, fc='none')
ax1.axis('off')

ax = fig.add_axes([0, 0, 1, 1], xlim=xlim, ylim=ylim, fc='none')
ax.axis('off')

# Título
ax.text(0, 1.05, 'Volume do Cone - Método das Cascas Cilíndricas',
        size=32, ha='center', va='bottom', weight='bold')


# ==============================================================================
# PARÂMETROS GEOMÉTRICOS
# ==============================================================================

# Ângulos de visibilidade (partes visíveis vs ocultas)
t1 = np.pi - np.atan(2*np.sqrt(2))  # ~135°
t2 = t1 + np.pi                      # ~315°
theta = np.linspace(t1, t2, 100)     # Arco visível
theta_full = np.linspace(0, 2*np.pi, 100)  # Círculo completo

# Posição central do cone
xy = np.array([0, 0.1])

# Tamanho dos eixos de coordenadas
xm, ym, zm = .5, .5, 1.0

# Dimensões do cone
r = .4    # raio da base
h = .9    # altura

# Parâmetro de integração: raio das cascas cilíndricas
rho = np.linspace(0, r, Nf)


# ==============================================================================
# DESENHO DA ESTRUTURA ESTÁTICA
# ==============================================================================

# Eixos de coordenadas (x, y, z)
axes_data = [
    (c32([xm, 0, 0]), 'x', (-0.05, -0.05)),
    (c32([0, ym, 0]), 'y', (0.05, -0.05)),
    (c32([0, 0, zm]), 'z', (0, 0.05))
]

for axis_vec, label, offset in axes_data:
    ax.annotate('',
                xy + axis_vec,
                xy,
                arrowprops=dict(arrowstyle='->', lw=2, color='k'))
    ax.text(xy[0] + axis_vec[0] + offset[0],
            xy[1] + axis_vec[1] + offset[1],
            label, size=20, weight='bold', ha='center')

# Contorno da base do cone
# Parte visível (frente)
ax.plot(xy[0] + r*c32([np.cos(theta), np.sin(theta), 0*theta])[0],
        xy[1] + r*c32([np.cos(theta), np.sin(theta), 0*theta])[1],
        '--', c=cl[0], lw=2, alpha=.7, label='Base (visível)')

# Parte oculta (atrás)
ax.plot(xy[0] + r*c32([-np.cos(theta), -np.sin(theta), 0*theta])[0],
        xy[1] + r*c32([-np.cos(theta), -np.sin(theta), 0*theta])[1],
        '-', c=cl[0], lw=2.5, alpha=.8, label='Base (oculta)')

# Arestas laterais do cone (da base ao vértice)
for i in range(2):
    edge_angle = t1 + np.pi * i
    base_point = xy + c32([r*np.cos(edge_angle), r*np.sin(edge_angle), 0])
    apex_point = xy + c32([0, 0, h])

    ax.plot([base_point[0], apex_point[0]],
            [base_point[1], apex_point[1]],
            c=cl[0], lw=2, alpha=.7)

# Vértice do cone
apex = xy + c32([0, 0, h])
ax.plot(apex[0], apex[1], 'o', c=cl[0], markersize=8, zorder=10)

# Dimensões anotadas (r e h)
# Raio r
r_line_end = xy + c32([r*np.cos(t1), r*np.sin(t1), 0])
ax.plot([xy[0], r_line_end[0]], [xy[1], r_line_end[1]],
        '--', c='k', lw=2)
ax.text((xy[0] + r_line_end[0])/2 - 0.05,
        (xy[1] + r_line_end[1])/2,
        '$r$', size=28, c='k', ha='center', va='bottom',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Altura h
ax.plot([xy[0], apex[0]], [xy[1], apex[1]], '--', c='k', lw=2)
ax.text(xy[0] - 0.08, xy[1] + h/2,
        '$h$', size=28, c='k', ha='right', va='center',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Fórmulas matemáticas
formulas_y = -0.6

# Diferencial
ax.text(0, formulas_y,
        r'$dV = 2\pi\rho \cdot h\left(1-\frac{\rho}{r}\right) d\rho$',
        size=22, ha='center', va='bottom',
        bbox=dict(boxstyle='round', pad=0.5, facecolor='lightyellow',
                  edgecolor=cl[1], lw=3))

# Integral
ax.text(0, formulas_y - 0.35,
        r'$V = \int_0^r 2\pi\rho\left(h - \frac{h}{r}\rho\right) d\rho$',
        size=24, ha='center', va='bottom',
        bbox=dict(boxstyle='round', pad=0.5, facecolor='lightblue',
                  edgecolor=cl[0], lw=3))

# Resultado final
ax.text(0, formulas_y - 0.75,
        r'$V = \frac{1}{3}\pi r^2 h$',
        size=32, ha='center', va='bottom', weight='bold',
        bbox=dict(boxstyle='round', pad=0.7, facecolor='lightgreen',
                  edgecolor=cl[2], lw=4))

# Legenda explicativa
legend_x = -1.3
legend_y = 0.7
ax.text(legend_x, legend_y,
        'Método das Cascas Cilíndricas:', size=16, weight='bold')
ax.text(legend_x, legend_y - 0.15,
        '• Cada casca tem raio ρ', size=14)
ax.text(legend_x, legend_y - 0.3,
        '• Altura na superfície: h(1-ρ/r)', size=14)
ax.text(legend_x, legend_y - 0.45,
        '• Área lateral: 2πρ × h(1-ρ/r)', size=14)
ax.text(legend_x, legend_y - 0.6,
        '• Espessura: dρ', size=14)

# Indicador de progresso (será atualizado na animação)
progress_text = ax.text(1.1, 0.7, '', size=16, ha='left', va='top',
                        bbox=dict(boxstyle='round', facecolor='white',
                                  edgecolor='gray', lw=2))


# ==============================================================================
# FUNÇÃO DE ANIMAÇÃO
# ==============================================================================

def animate(i):
    """
    Desenha a casca cilíndrica no frame i

    Args:
        i: índice do frame atual (0 até Nf-1)
    """
    if i % 50 == 0:
        print(f"Frame {i}/{Nf}")

    # Limpa o eixo dinâmico
    ax1.cla()
    ax1.set_xlim(xlim)
    ax1.set_ylim(ylim)
    ax1.axis('off')

    # Raio atual da casca
    rho_current = rho[i]

    # Altura da casca na superfície do cone
    z_top = h * (1 - rho_current / r)

    # ---------------------------------------------------------------------------
    # CASCA CILÍNDRICA ATUAL (destacada em cor diferente)
    # ---------------------------------------------------------------------------

    if rho_current > 0.01:  # Evita casca de raio zero
        # Superfície lateral da casca (retângulo enrolado)
        verts = []

        # Base (círculo inferior em z=0)
        for t in theta + np.pi:
            verts.append(xy + c32([rho_current*np.cos(t),
                                  rho_current*np.sin(t), 0]))

        # Topo (círculo superior na superfície do cone) - ordem reversa
        for t in reversed(theta + np.pi):
            verts.append(xy + c32([rho_current*np.cos(t),
                                  rho_current*np.sin(t), z_top]))

        verts.append((0, 0))  # Fecha o polígono

        # Desenha a casca atual
        codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
            (len(verts)-2) + [path.Path.CLOSEPOLY]
        ax1.add_patch(patches.PathPatch(
            path.Path(verts, codes),
            fc=cl[3], ec=cl[1], lw=2, alpha=0.85, zorder=2,
            label='Casca atual'
        ))

        # Círculo superior da casca (tracejado)
        ax1.plot(
            xy[0] + c32([rho_current*np.cos(theta),
                        rho_current*np.sin(theta),
                        0*theta + z_top])[0],
            xy[1] + c32([rho_current*np.cos(theta),
                        rho_current*np.sin(theta),
                        0*theta + z_top])[1],
            '--', c=cl[1], lw=2.5, zorder=3, alpha=0.9
        )

        # Círculo inferior da casca
        ax1.plot(
            xy[0] + c32([rho_current*np.cos(theta),
                        rho_current*np.sin(theta),
                        0*theta])[0],
            xy[1] + c32([rho_current*np.cos(theta),
                        rho_current*np.sin(theta),
                        0*theta])[1],
            '--', c=cl[1], lw=2.5, zorder=3, alpha=0.9
        )

        # Indicador do raio ρ atual
        rho_line_end = xy + c32([rho_current*np.cos(t1),
                                 rho_current*np.sin(t1), 0])
        ax1.plot([xy[0], rho_line_end[0]],
                 [xy[1], rho_line_end[1]],
                 '-', c='red', lw=3, zorder=5)
        ax1.text((xy[0] + rho_line_end[0])/2 - 0.05,
                 (xy[1] + rho_line_end[1])/2 + 0.05,
                 r'$\rho$', size=24, c='red', ha='center', va='bottom',
                 weight='bold',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    # ---------------------------------------------------------------------------
    # VOLUME ACUMULADO (cone interno até ρ)
    # ---------------------------------------------------------------------------

    if rho_current > 0.01:
        # Cone sólido da base até a casca atual
        verts = []

        # Círculo no topo (na superfície do cone)
        for t in theta + np.pi:
            verts.append(xy + c32([rho_current*np.cos(t),
                                  rho_current*np.sin(t), z_top]))

        # Vértice do cone
        verts.append(xy + c32([0, 0, h]))
        verts.append((0, 0))

        codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
            (len(verts)-2) + [path.Path.CLOSEPOLY]
        ax1.add_patch(patches.PathPatch(
            path.Path(verts, codes),
            fc=cl[0], ec='none', alpha=0.6, zorder=1,
            label='Volume acumulado'
        ))

    # ---------------------------------------------------------------------------
    # ATUALIZAR INFORMAÇÕES DE PROGRESSO
    # ---------------------------------------------------------------------------

    progress_percent = (i / Nf) * 100
    progress_text.set_text(
        f'Progresso: {progress_percent:.1f}%\n'
        f'ρ = {rho_current:.3f}\n'
        f'h(ρ) = {z_top:.3f}'
    )

    return []


# ==============================================================================
# RENDERIZAÇÃO E SALVAMENTO
# ==============================================================================

# Assinatura
ax.text(0, -1.1,
        r'@Ivan Carlos Lopes',
        size=14, c='.3', alpha=.5, ha='center', va='bottom',
        style='italic')

# Cria a animação
print("Criando animação...")
anim = animation.FuncAnimation(fig, animate, frames=Nf, interval=20)

# Salva como vídeo MP4
print("Salvando animação (isso pode demorar alguns minutos)...")
anim.save("cone_cascas_cilindricas.mp4",
          writer=animation.FFMpegWriter(fps=60),
          dpi=200)
print("✓ Animação salva: cone_cascas_cilindricas.mp4")

#
