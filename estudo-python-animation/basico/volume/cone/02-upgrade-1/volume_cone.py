"""
Animação do Cálculo do Volume de um Cone - Representação Fiel de Cascas
=========================================================================
Correção de erro de broadcasting e representação de acúmulo de tubos.
"""

from matplotlib import pyplot, animation, cm, patches, path
import numpy as np

# Configuração de fontes
pyplot.rcParams.update({"font.family": "sans-serif", "mathtext.fontset": "cm"})


def c32(xyz):
    """
    Projeção isométrica 3D -> 2D
    xyz deve ter formato (3, N)
    """
    xyz = np.array(xyz)
    x, y, z = xyz[0], xyz[1], xyz[2]
    # Retorna (2, N)
    return np.array([
        y - x * np.sin(np.pi/4) / 2,
        z - x * np.cos(np.pi/4) / 2
    ])


# ==============================================================================
# PARÂMETROS E CONFIGURAÇÃO
# ==============================================================================
Nf = 100
r, h = 0.5, 0.8
X_POS, Y_POS = 0.0, 0.05
# Transformado em vetor coluna (2, 1) para broadcast
xy = np.array([[X_POS], [Y_POS]])
cl = list(cm.tab10.colors)

fig = pyplot.figure(figsize=(10, 10))
xlim, ylim = [-0.9, 0.9], [-0.35, 1.15]
ax = fig.add_axes([0, 0, 1, 1], xlim=xlim, ylim=ylim, fc='none')
ax1 = fig.add_axes([0, 0, 1, 1], xlim=xlim, ylim=ylim, fc='none')
ax.axis('off')
ax1.axis('off')

ax.text(0, ylim[1] - 0.05, 'Construção por Cascas Cilíndricas',
        size=28, ha='center', va='top', weight='bold')

# Pré-cálculos geométricos
t1 = np.pi - np.atan(2*np.sqrt(2))
t2 = t1 + np.pi
theta = np.linspace(t1, t2, 100)
theta_plus_pi = theta + np.pi
cos_theta, sin_theta = np.cos(theta), np.sin(theta)
cos_theta_pi, sin_theta_pi = np.cos(theta_plus_pi), np.sin(theta_plus_pi)
rho = np.linspace(0, r, Nf)


def draw_static():
    # Eixo Z (Altura)
    apex_3d = np.array([[0], [0], [h]])
    apex_pt = xy + c32(apex_3d)
    ax.annotate('', xy=(apex_pt[0, 0], apex_pt[1, 0]), xytext=(xy[0, 0], xy[1, 0]),
                arrowprops=dict(arrowstyle='->', lw=1))

    # Guia do Cone (pontilhado)
    for i in [0, 1]:
        angle = t1 + np.pi * i
        base_pt = xy + c32([[r*np.cos(angle)], [r*np.sin(angle)], [0]])
        ax.plot([base_pt[0, 0], apex_pt[0, 0]], [
                base_pt[1, 0], apex_pt[1, 0]], ':', c='gray', alpha=0.4)

    # Base do cone - Aqui corrigimos o broadcast
    coords_3d = np.array([r * cos_theta, r * sin_theta, np.zeros_like(theta)])
    b_vis = xy + c32(coords_3d)
    ax.plot(b_vis[0], b_vis[1], '--', c='blue', lw=1, alpha=0.3)


draw_static()

history_verts = []


def animate(i):
    global history_verts
    ax1.cla()
    ax1.set_xlim(xlim)
    ax1.set_ylim(ylim)
    ax1.axis('off')

    rho_i = rho[i]
    if rho_i < 1e-7:
        return []

    z_top = h * (1 - rho_i / r)
    n_theta = len(theta_plus_pi)

    # 1. Desenhar o histórico (acúmulo de tubos)
    for v_past in history_verts[::3]:  # Otimização para performance
        ax1.plot(v_past[0], v_past[1], c=cl[0], lw=0.5, alpha=0.15)

    # 2. Casca Atual (Laranja)
    # Base
    b_coords_3d = np.array(
        [rho_i * cos_theta_pi, rho_i * sin_theta_pi, np.zeros(n_theta)])
    b_2d = xy + c32(b_coords_3d)

    # Topo
    t_coords_3d = np.array([rho_i * cos_theta_pi[::-1],
                           rho_i * sin_theta_pi[::-1], np.full(n_theta, z_top)])
    t_2d = xy + c32(t_coords_3d)

    # Montar vértices para o PathPatch (N, 2)
    verts = np.zeros((2 * n_theta + 1, 2))
    verts[:n_theta, 0] = b_2d[0]
    verts[:n_theta, 1] = b_2d[1]
    verts[n_theta:2*n_theta, 0] = t_2d[0]
    verts[n_theta:2*n_theta, 1] = t_2d[1]
    verts[-1] = verts[0]

    codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
        (2*n_theta - 1) + [path.Path.CLOSEPOLY]
    ax1.add_patch(patches.PathPatch(path.Path(verts, codes),
                  fc='orange', ec='darkorange', alpha=0.8, zorder=3))

    # Guardar círculo superior no histórico
    top_circle_3d = np.array(
        [rho_i * cos_theta, rho_i * sin_theta, np.full(len(theta), z_top)])
    history_verts.append(xy + c32(top_circle_3d))

    ax1.text(0, ylim[0] + 0.1, f'Raio: {rho_i:.2f} | Altura Casca: {z_top:.2f}',
             ha='center', size=15, bbox=dict(facecolor='white', alpha=0.7))

    return []


print("Gerando animação...")
anim = animation.FuncAnimation(
    fig, animate, frames=Nf, interval=50, blit=False)
anim.save("volume_cone_fiel.mp4",
          writer=animation.FFMpegWriter(fps=30), dpi=150)
print("✓ Sucesso!")
