"""
Animação do Cálculo do Volume de um Cone - Método das Cascas Cilíndricas
=========================================================================

Mostra visualmente como calcular V = (1/3)πr²h usando integração por
cascas cilíndricas variando ρ de 0 até r.

Autor: Ivan Carlos Lopes
"""

from matplotlib import pyplot, animation, cm, patches, path
import numpy as np

# Configuração de fontes para renderização matemática elegante
pyplot.rcParams.update({"font.family": "sans-serif", "mathtext.fontset": "cm"})


def c32(xyz):
    """
    Projeção isométrica (cavaleira) 3D → 2D

    Vetorizada para aceitar arrays numpy
    """
    return np.array([
        xyz[1] - xyz[0] * np.sin(np.pi/4) / 2,
        xyz[2] - xyz[0] * np.cos(np.pi/4) / 2
    ])


# ==============================================================================
# CONFIGURAÇÃO DA ANIMAÇÃO
# ==============================================================================

Nf = 100  # Número de frames
cl = list(cm.tab10.colors)

# Criação da figura
fig = pyplot.figure(figsize=(9, 9))

# Limites de visualização (zoom)
xlim = [-0.9, 0.9]
ylim = [-0.35, 1.15]

# Dois eixos sobrepostos
ax1 = fig.add_axes([0, 0, 1, 1], xlim=xlim, ylim=ylim, fc='none')
ax1.axis('off')

ax = fig.add_axes([0, 0, 1, 1], xlim=xlim, ylim=ylim, fc='none')
ax.axis('off')

# Título
ax.text(0, ylim[1] - 0.05, 'Método das Cascas Cilíndricas',
        size=35, ha='center', va='top', weight='bold')


# ==============================================================================
# PARÂMETROS GEOMÉTRICOS
# ==============================================================================

# Dimensões do cone
r = 0.5   # raio da base
h = 0.8   # altura

# ==============================================================
# POSIÇÃO GLOBAL DO DESENHO (AJUSTE ANTES DE RODAR)
# ==============================================================

X_POS = 0.0    # deslocamento horizontal
Y_POS = 0.05    # deslocamento vertical

# Posição central
xy = np.array([X_POS, Y_POS])

# Tamanho dos eixos
xm, ym, zm = 0.8, 0.8, 0.9

# Ângulos de visibilidade
t1 = np.pi - np.atan(2*np.sqrt(2))
t2 = t1 + np.pi
theta = np.linspace(t1, t2, 100)

# ⚡ PRÉ-CALCULA valores que não mudam
theta_plus_pi = theta + np.pi
cos_theta = np.cos(theta)
sin_theta = np.sin(theta)
cos_theta_pi = np.cos(theta_plus_pi)
sin_theta_pi = np.sin(theta_plus_pi)

# Array de raios para animação
rho = np.linspace(0, r, Nf)

# ⚡ PRÉ-CALCULA coordenadas da base do cone (não muda)
base_visible_x = xy[0] + r * \
    c32([cos_theta, sin_theta, np.zeros_like(theta)])[0]
base_visible_y = xy[1] + r * \
    c32([cos_theta, sin_theta, np.zeros_like(theta)])[1]

base_hidden_x = xy[0] + r * \
    c32([-cos_theta, -sin_theta, np.zeros_like(theta)])[0]
base_hidden_y = xy[1] + r * \
    c32([-cos_theta, -sin_theta, np.zeros_like(theta)])[1]

# ⚡ PRÉ-CALCULA arestas laterais
edge_points = []
for i in range(2):
    angle = t1 + np.pi * i
    base_pt = xy + c32([r*np.cos(angle), r*np.sin(angle), 0])
    apex_pt = xy + c32([0, 0, h])
    edge_points.append((base_pt, apex_pt))


# ==============================================================================
# DESENHO DA ESTRUTURA ESTÁTICA
# ==============================================================================

# Eixos de coordenadas
axes = [c32([xm, 0, 0]), c32([0, ym, 0]), c32([0, 0, zm])]
for axis_vec in axes:
    ax.annotate('', xy + axis_vec, xy,
                arrowprops=dict(arrowstyle='->', lw=1, color='k'))

# Contorno da base (pré-calculado)
ax.plot(base_visible_x, base_visible_y, '--', c=cl[0], lw=1.2, alpha=.6)
ax.plot(base_hidden_x, base_hidden_y, '-', c=cl[0], lw=2, alpha=.6)

# Arestas laterais (pré-calculadas)
for base_pt, apex_pt in edge_points:
    ax.plot([base_pt[0], apex_pt[0]], [base_pt[1], apex_pt[1]],
            c=cl[0], lw=1, alpha=.6)

# Linha do raio com label
r_end = xy + c32([r*np.cos(t1), r*np.sin(t1), 0])
ax.plot([xy[0], r_end[0]], [xy[1], r_end[1]], '--', c='k', lw=1.2)
ax.text((xy[0] + r_end[0])/2, (xy[1] + r_end[1])/2,
        '$r$', size=25, c='k', ha='center', va='bottom')

# Label de altura
ax.text(xy[0], xy[1] + h/2, '$h$', size=25, c='k', ha='right', va='center')

# Fórmulas matemáticas
formulas_y = ylim[0] + 0.1

# ax.text(0, formulas_y,
#         r'$dV = 2\pi\rho \cdot h\left(1-\frac{\rho}{r}\right) d\rho$',
#         size=20, ha='center', va='bottom',
#         bbox=dict(boxstyle='round', pad=0.4, facecolor='lightyellow',
#                   edgecolor=cl[1], lw=2.5))

# ax.text(0, formulas_y - 0.15,
#         r'$V = \int_0^r 2\pi\rho\left(h - \frac{h}{r}\rho\right) d\rho = \frac{1}{3}\pi r^2 h$',
#         size=22, ha='center', va='bottom', weight='bold',
#         bbox=dict(boxstyle='round', pad=0.5, facecolor='lightgreen',
#                   edgecolor=cl[2], lw=3))


# ==============================================================================
# FUNÇÃO DE ANIMAÇÃO OTIMIZADA
# ==============================================================================

# ⚡ Objetos que serão atualizados (evita recriar em cada frame)
shell_patch = None
top_circle_line = None
volume_patch = None

# ⚡ PRÉ-CALCULA códigos de path (não mudam)
n_theta = len(theta_plus_pi)
# codes_shell: base (n_theta) + topo (n_theta) + fechamento (1) = 2*n_theta + 1
codes_shell = [path.Path.MOVETO] + [path.Path.LINETO] * \
    (2*n_theta - 1) + [path.Path.CLOSEPOLY]
# codes_volume: círculo (n_theta) + apex (1) + fechamento (1) = n_theta + 2
codes_volume = [path.Path.MOVETO] + \
    [path.Path.LINETO]*(n_theta) + [path.Path.CLOSEPOLY]


def animate(i):
    """Animação otimizada - minimiza recriação de objetos"""
    global shell_patch, top_circle_line, volume_patch

    if i % 25 == 0:
        print(f"Frame {i}/{Nf}")

    # Limpa apenas os patches dinâmicos
    ax1.cla()
    ax1.set_xlim(xlim)
    ax1.set_ylim(ylim)
    ax1.axis('off')

    rho_i = rho[i]

    # ⚡ Evita divisão por zero
    if rho_i < 1e-6:
        return []

    z_top = h * (1 - rho_i / r)

    # ===========================================================================
    # CASCA CILÍNDRICA (vetorizado)
    # ===========================================================================

    # ⚡ Calcula vértices de forma vetorizada
    verts = np.zeros((2*n_theta + 1, 2))

    # Base (círculo inferior)
    base_coords = c32([rho_i * cos_theta_pi, rho_i * sin_theta_pi,
                       np.zeros(n_theta)])
    verts[:n_theta, 0] = xy[0] + base_coords[0]
    verts[:n_theta, 1] = xy[1] + base_coords[1]

    # Topo (círculo superior) - ordem reversa
    top_coords = c32([rho_i * cos_theta_pi[::-1],
                     rho_i * sin_theta_pi[::-1],
                     np.full(n_theta, z_top)])
    verts[n_theta:2*n_theta, 0] = xy[0] + top_coords[0]
    verts[n_theta:2*n_theta, 1] = xy[1] + top_coords[1]

    # Fecha o polígono
    verts[-1] = [0, 0]

    # Adiciona patch da casca
    ax1.add_patch(patches.PathPatch(
        path.Path(verts, codes_shell),
        fc=cl[1], ec='none', alpha=0.8, zorder=1
    ))

    # ===========================================================================
    # CÍRCULO SUPERIOR (tracejado)
    # ===========================================================================

    top_circle_coords = c32([rho_i * cos_theta, rho_i * sin_theta,
                             np.full(len(theta), z_top)])

    ax1.plot(xy[0] + top_circle_coords[0],
             xy[1] + top_circle_coords[1],
             '--', c=cl[1], lw=1.2, zorder=-2)

    # ===========================================================================
    # VOLUME ACUMULADO (vetorizado)
    # ===========================================================================

    verts_vol = np.zeros((n_theta + 2, 2))

    # Círculo no topo da casca
    verts_vol[:n_theta, 0] = xy[0] + top_coords[0][::-1]  # reverte de volta
    verts_vol[:n_theta, 1] = xy[1] + top_coords[1][::-1]

    # Vértice do cone
    apex = xy + c32([0, 0, h])
    verts_vol[n_theta] = apex

    # Fecha o polígono
    verts_vol[-1] = [0, 0]

    ax1.add_patch(patches.PathPatch(
        path.Path(verts_vol, codes_volume),
        fc=cl[0], ec='none', alpha=0.8, zorder=1
    ))

    return []


# ==============================================================================
# RENDERIZAÇÃO E SALVAMENTO
# ==============================================================================

# Assinatura
ax.text(0, ylim[0] + 0.01,
        r'@Ivan Carlos Lopes',
        size=12, c='.2', alpha=.3, ha='center', va='bottom',
        style='italic')

print("Criando animação...")
anim = animation.FuncAnimation(
    fig, animate, frames=Nf, interval=20, blit=False)

print("Salvando animação (pode demorar alguns minutos)...")
anim.save("volume_cone_optimized.mp4",
          writer=animation.FFMpegWriter(fps=60),
          dpi=200)
print("✓ Animação salva: volume_cone_optimized.mp4")