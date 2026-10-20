"""
Animação do Volume do Cone via Método das Cascas Cilíndricas
===========================================================

Mostra visualmente:
- A casca diferencial (ΔV) no raio ρ
- O volume acumulado até ρ
- O integrando A(ρ) = 2πρ h(ρ) (área lateral efetiva da casca)
- Consistência com V = (1/3)π r^2 h

Autor: Ivan Carlos Lopes (revisão/otimização: ChatGPT)
"""

from matplotlib import pyplot as plt, animation, cm, patches, path as mpath
import numpy as np

plt.rcParams.update({"font.family": "sans-serif", "mathtext.fontset": "cm"})


# ----------------------------
# Projeção 3D → 2D (cavaleira)
# ----------------------------
def c32(xyz):
    xyz = np.asarray(xyz)
    return np.array([
        xyz[1] - xyz[0] * np.sin(np.pi/4) / 2,
        xyz[2] - xyz[0] * np.cos(np.pi/4) / 2
    ])


# ----------------------------
# Parâmetros
# ----------------------------
Nf = 900
cl = list(cm.tab10.colors)

# cone
r = 0.50
h = 0.80

# posição do cone na tela
xy0 = np.array([0.0, 0.08])

# eixos "3D"
xm, ym, zm = 0.75, 0.75, 0.90

# ângulos da elipse (base)
t1 = np.pi - np.atan(2*np.sqrt(2))
t2 = t1 + np.pi
theta = np.linspace(t1, t2, 220)

rho_vals = np.linspace(0.0, r, Nf)


# função altura no raio ρ
def h_of_rho(rho):
    return h * (1.0 - rho / r)


# integrando "área lateral efetiva"
def A_of_rho(rho):
    return 2.0*np.pi*rho*h_of_rho(rho)


# volume acumulado analítico até ρ (útil p/ indicador)
# V(ρ) = ∫_0^ρ 2π s (h - (h/r)s) ds
def V_of_rho(rho):
    return 2*np.pi*(h*(rho**2)/2.0 - (h/r)*(rho**3)/3.0)


V_total = (1/3)*np.pi*r**2*h


# ----------------------------
# Figura (2 painéis)
# ----------------------------
fig = plt.figure(figsize=(11, 8))

# Painel esquerdo: cone 3D (projetado)
axL = fig.add_axes([0.03, 0.06, 0.63, 0.90])
axL.set_xlim(-0.95, 0.95)
axL.set_ylim(-0.40, 1.18)
axL.axis("off")

# Painel direito: gráfico do integrando
axR = fig.add_axes([0.70, 0.14, 0.28, 0.76])
axR.set_xlim(0.0, r)
axR.set_ylim(0.0, A_of_rho(r*0.55)*1.35)
axR.set_xlabel(r"$\rho$")
axR.set_ylabel(r"$A(\rho)=2\pi\rho\,h(\rho)$")
axR.grid(True, alpha=0.25)

axL.text(0.0, 1.12, "Método das Cascas Cilíndricas (Cone)",
         size=26, ha="center", va="top")


# ----------------------------
# Desenho estático do cone
# ----------------------------
# Eixos
axes_vectors = [c32([xm, 0, 0]), c32([0, ym, 0]), c32([0, 0, zm])]
for v in axes_vectors:
    axL.annotate('', xy=xy0 + v, xytext=xy0,
                 arrowprops=dict(arrowstyle='->', lw=1, color='k', alpha=0.6))

# Base (contorno: parte "traseira" tracejada, parte "frontal" cheia)
axL.plot(xy0[0] + r*c32([np.cos(theta), np.sin(theta), 0*theta])[0],
         xy0[1] + r*c32([np.cos(theta), np.sin(theta), 0*theta])[1],
         '--', c=cl[0], lw=1.2, alpha=0.6)

axL.plot(xy0[0] + r*c32([-np.cos(theta), -np.sin(theta), 0*theta])[0],
         xy0[1] + r*c32([-np.cos(theta), -np.sin(theta), 0*theta])[1],
         '-', c=cl[0], lw=2.2, alpha=0.6)

# Arestas laterais
for i in range(2):
    edge_angle = t1 + np.pi*i
    base_point = xy0 + c32([r*np.cos(edge_angle), r*np.sin(edge_angle), 0])
    apex_point = xy0 + np.array([0.0, h])
    axL.plot([base_point[0], apex_point[0]],
             [base_point[1], apex_point[1]],
             c=cl[0], lw=1.4, alpha=0.6)

# raio r (linha na base) + rótulos
axL.plot([xy0[0], xy0[0] + r*c32([np.cos(t1), np.sin(t1), 0])[0]],
         [xy0[1], xy0[1] + r*c32([np.cos(t1), np.sin(t1), 0])[1]],
         '--', c='k', lw=1.2, alpha=0.7)

axL.text(xy0[0] + r*c32([np.cos(t1), np.sin(t1), 0])[0]/2,
         xy0[1] + r*c32([np.cos(t1), np.sin(t1), 0])[1]/2,
         r"$r$", size=22, c="k", ha="center", va="bottom")

axL.text(xy0[0], xy0[1] + h/2,
         r"$h$", size=22, c="k", ha="right", va="center")

# Fórmulas (linha única)
y_formula = -0.34
dx = 0.62
axL.text(-dx, y_formula,
         r"$dV = 2\pi\rho\left(h-\frac{h}{r}\rho\right)\,d\rho$",
         size=18, ha="center", va="bottom",
         bbox=dict(boxstyle="round", pad=0.25, facecolor="none",
                   edgecolor=cl[1], lw=2.5))

axL.text(0.0, y_formula,
         r"$V=\int_0^r 2\pi\rho\left(h-\frac{h}{r}\rho\right)\,d\rho$",
         size=18, ha="center", va="bottom",
         bbox=dict(boxstyle="round", pad=0.25, facecolor="none",
                   edgecolor=cl[0], lw=2.5))

axL.text(+dx, y_formula,
         r"$V=\frac{1}{3}\pi r^2 h$",
         size=18, ha="center", va="bottom",
         bbox=dict(boxstyle="round", pad=0.25, facecolor="none",
                   edgecolor=cl[2], lw=3.5))

# Assinatura
axL.text(0.0, -0.385, r"@Ivan Lopes", size=11, c=".2", alpha=0.35,
         ha="center", va="bottom")


# ----------------------------
# Artistas dinâmicos (criados UMA vez)
# ----------------------------
Path = mpath.Path

shell_patch = patches.PathPatch(Path([(0, 0)], [Path.MOVETO]),
                                fc=cl[1], ec='none', alpha=0.75, zorder=3)
axL.add_patch(shell_patch)

(shell_top_line,) = axL.plot([], [], '--', c=cl[1], lw=1.2, alpha=0.9, zorder=2)

acc_patch = patches.PathPatch(Path([(0, 0)], [Path.MOVETO]),
                              fc=cl[0], ec='none', alpha=0.60, zorder=1)
axL.add_patch(acc_patch)

info_text = axL.text(0.62, 0.92, "", transform=axL.transAxes,
                     ha="left", va="top", fontsize=14,
                     bbox=dict(boxstyle="round", pad=0.35,
                               facecolor="white", alpha=0.75, edgecolor="0.8"))

rho_plot = np.linspace(0, r, 400)
A_plot = A_of_rho(rho_plot)
(axA,) = axR.plot(rho_plot, A_plot, lw=2.0)

(marker,) = axR.plot([0], [0], marker="o", markersize=7)
gtext = axR.text(0.02, 0.98, "", transform=axR.transAxes,
                 ha="left", va="top", fontsize=12)

# >>> IMPORTANTE: guarda a coleção do fill_between para remover depois
fill_poly = axR.fill_between(rho_plot, 0, 0*rho_plot, alpha=0.20)


# ----------------------------
# Helpers para construir Paths
# ----------------------------
def make_shell_path(rho, drho):
    rho_in = max(rho - drho, 0.0)
    rho_out = rho

    z_out = h_of_rho(rho_out)
    z_in = h_of_rho(rho_in)

    verts = []
    for t in theta + np.pi:
        verts.append(xy0 + c32([rho_out*np.cos(t), rho_out*np.sin(t), 0.0]))
    for t in reversed(theta + np.pi):
        verts.append(xy0 + c32([rho_out*np.cos(t), rho_out*np.sin(t), z_out]))

    for t in theta + np.pi:
        verts.append(xy0 + c32([rho_in*np.cos(t), rho_in*np.sin(t), z_in]))
    for t in reversed(theta + np.pi):
        verts.append(xy0 + c32([rho_in*np.cos(t), rho_in*np.sin(t), 0.0]))

    verts.append(verts[0])
    codes = [Path.MOVETO] + [Path.LINETO]*(len(verts)-2) + [Path.CLOSEPOLY]
    return Path(verts, codes), z_out


def make_acc_path(rho):
    z_top = h_of_rho(rho)
    verts = []
    for t in theta + np.pi:
        verts.append(xy0 + c32([rho*np.cos(t), rho*np.sin(t), z_top]))

    verts.append(xy0 + c32([0.0, 0.0, h]))
    verts.append(verts[0])

    codes = [Path.MOVETO] + [Path.LINETO]*(len(verts)-2) + [Path.CLOSEPOLY]
    return Path(verts, codes), z_top


# ----------------------------
# Animação
# ----------------------------
drho = r / (Nf - 1)


def init():
    global fill_poly
    shell_patch.set_path(Path([(0, 0)], [Path.MOVETO]))
    acc_patch.set_path(Path([(0, 0)], [Path.MOVETO]))
    shell_top_line.set_data([], [])

    marker.set_data([0.0], [A_of_rho(0.0)])
    gtext.set_text("")
    info_text.set_text("")

    # zera o preenchimento (remove e recria)
    try:
        fill_poly.remove()
    except Exception:
        pass
    fill_poly = axR.fill_between(rho_plot, 0, 0*rho_plot, alpha=0.20)

    return (shell_patch, acc_patch, shell_top_line, marker, gtext, info_text, fill_poly)


def animate(i):
    global fill_poly

    rho = float(rho_vals[i])

    shell_path, z_out = make_shell_path(rho, drho)
    shell_patch.set_path(shell_path)

    xt = xy0[0] + c32([rho*np.cos(theta), rho *
                      np.sin(theta), 0*theta + z_out])[0]
    yt = xy0[1] + c32([rho*np.cos(theta), rho *
                      np.sin(theta), 0*theta + z_out])[1]
    shell_top_line.set_data(xt, yt)

    acc_path, _ = make_acc_path(rho)
    acc_patch.set_path(acc_path)

    V_now = V_of_rho(rho)
    A_now = A_of_rho(rho)

    # >>> aqui é CRÍTICO: usar strings raw para LaTeX com \frac
    info_text.set_text(
        r"$\rho=" + f"{rho:.3f}" + r"$" + "\n"
        r"$h(\rho)=h\left(1-\frac{\rho}{r}\right)=" +
        f"{h_of_rho(rho):.3f}" + r"$" + "\n"
        r"$A(\rho)=2\pi\rho h(\rho)=" + f"{A_now:.3f}" + r"$" + "\n"
        r"$V(\rho)=\int_0^\rho A(s)\,ds=" + f"{V_now:.4f}" + r"$" + "\n"
        r"$V_{\rm total}=\frac{1}{3}\pi r^2h=" + f"{V_total:.4f}" + r"$"
    )

    marker.set_data([rho], [A_now])
    gtext.set_text(rf"$A(\rho)$ no ponto: {A_now:.4f}")

    # >>> substitui o axR.collections.clear() por remove + recria do PolyCollection
    try:
        fill_poly.remove()
    except Exception:
        pass
    fill_poly = axR.fill_between(
        rho_plot, 0, A_plot, where=(rho_plot <= rho), alpha=0.20)

    return (shell_patch, acc_patch, shell_top_line, marker, gtext, info_text, fill_poly)


anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=Nf, interval=20, blit=False)

print("Salvando animação...")
anim.save("volume_cone_shells.mp4",
          writer=animation.FFMpegWriter(fps=60),
          dpi=200)
print("✓ Animação salva: volume_cone_shells.mp4")
