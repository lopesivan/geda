"""
Animação do Volume do Cone via Método das Cascas Cilíndricas
===========================================================

Melhoria didática:
- Mostra NÃO só a casca atual, mas também as últimas N cascas simultaneamente,
  com transparência decrescente (efeito de “soma de cilindros ocos”).
- Mostra volume acumulado até ρ.
- Mostra o integrando A(ρ)=2πρh(ρ) e marca o ponto atual.

Autor: Ivan Carlos Lopes (revisão/otimização)
"""

from matplotlib import pyplot as plt, animation, cm, patches, path as mpath
import numpy as np

plt.rcParams.update({"font.family": "sans-serif", "mathtext.fontset": "cm"})


# ----------------------------
# Projeção 3D → 2D (cavaleira)
# ----------------------------
def c32(xyz):
    xyz = np.asarray(xyz)
    return np.array(
        [
            xyz[1] - xyz[0] * np.sin(np.pi / 4) / 2,
            xyz[2] - xyz[0] * np.cos(np.pi / 4) / 2,
        ]
    )


# ----------------------------
# Parâmetros
# ----------------------------
Nf = 100
cl = list(cm.tab10.colors)

# cone
r = 0.50
h = 0.80

# posição do cone na tela
xy0 = np.array([0.0, 0.08])

# eixos "3D"
xm, ym, zm = 0.75, 0.75, 0.90

# ângulos da elipse (base)
t1 = np.pi - np.atan(2 * np.sqrt(2))
t2 = t1 + np.pi
theta = np.linspace(t1, t2, 220)

rho_vals = np.linspace(0.0, r, Nf)

# número de cascas “visíveis” (rastro)
NSHELLS = 20

# espessura visual da casca (radial)
drho = r / (Nf - 1)

# transparência base da casca mais recente
alpha_shell_max = 0.80
alpha_shell_min = 0.05


# função altura no raio ρ
def h_of_rho(rho):
    return h * (1.0 - rho / r)


# integrando "área lateral efetiva"
def A_of_rho(rho):
    return 2.0 * np.pi * rho * h_of_rho(rho)


# volume acumulado analítico até ρ
def V_of_rho(rho):
    return 2.0 * np.pi * (h * (rho**2) / 2.0 - (h / r) * (rho**3) / 3.0)


V_total = (1.0 / 3.0) * np.pi * r**2 * h


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
axR.set_ylim(0.0, A_of_rho(r * 0.55) * 1.35)
axR.set_xlabel(r"$\rho$")
axR.set_ylabel(r"$A(\rho)=2\pi\rho\,h(\rho)$")
axR.grid(True, alpha=0.25)

axL.text(
    0.0,
    1.12,
    "Método das Cascas Cilíndricas (Cone)",
    size=26,
    ha="center",
    va="top",
)

# ----------------------------
# Desenho estático do cone
# ----------------------------
# Eixos
axes_vectors = [c32([xm, 0, 0]), c32([0, ym, 0]), c32([0, 0, zm])]
for v in axes_vectors:
    axL.annotate(
        "",
        xy=xy0 + v,
        xytext=xy0,
        arrowprops=dict(arrowstyle="->", lw=1, color="k", alpha=0.6),
    )

# Base (contorno: parte "traseira" tracejada, parte "frontal" cheia)
axL.plot(
    xy0[0] + r * c32([np.cos(theta), np.sin(theta), 0 * theta])[0],
    xy0[1] + r * c32([np.cos(theta), np.sin(theta), 0 * theta])[1],
    "--",
    c=cl[0],
    lw=1.2,
    alpha=0.6,
)

axL.plot(
    xy0[0] + r * c32([-np.cos(theta), -np.sin(theta), 0 * theta])[0],
    xy0[1] + r * c32([-np.cos(theta), -np.sin(theta), 0 * theta])[1],
    "-",
    c=cl[0],
    lw=2.2,
    alpha=0.6,
)

# Arestas laterais
for i in range(2):
    edge_angle = t1 + np.pi * i
    base_point = xy0 + c32([r * np.cos(edge_angle), r * np.sin(edge_angle), 0])
    apex_point = xy0 + np.array([0.0, h])
    axL.plot(
        [base_point[0], apex_point[0]],
        [base_point[1], apex_point[1]],
        c=cl[0],
        lw=1.4,
        alpha=0.6,
    )

# raio r (linha na base) + rótulos
axL.plot(
    [xy0[0], xy0[0] + r * c32([np.cos(t1), np.sin(t1), 0])[0]],
    [xy0[1], xy0[1] + r * c32([np.cos(t1), np.sin(t1), 0])[1]],
    "--",
    c="k",
    lw=1.2,
    alpha=0.7,
)

axL.text(
    xy0[0] + r * c32([np.cos(t1), np.sin(t1), 0])[0] / 2,
    xy0[1] + r * c32([np.cos(t1), np.sin(t1), 0])[1] / 2,
    r"$r$",
    size=22,
    c="k",
    ha="center",
    va="bottom",
)

axL.text(
    xy0[0],
    xy0[1] + h / 2,
    r"$h$",
    size=22,
    c="k",
    ha="right",
    va="center",
)

# Fórmulas (linha única)
y_formula = -0.34
dx = 0.62
axL.text(
    -dx,
    y_formula,
    r"$dV = 2\pi\rho\left(h-\frac{h}{r}\rho\right)\,d\rho$",
    size=18,
    ha="center",
    va="bottom",
    bbox=dict(boxstyle="round", pad=0.25,
              facecolor="none", edgecolor=cl[1], lw=2.5),
)

axL.text(
    0.0,
    y_formula,
    r"$V=\int_0^r 2\pi\rho\left(h-\frac{h}{r}\rho\right)\,d\rho$",
    size=18,
    ha="center",
    va="bottom",
    bbox=dict(boxstyle="round", pad=0.25,
              facecolor="none", edgecolor=cl[0], lw=2.5),
)

axL.text(
    +dx,
    y_formula,
    r"$V=\frac{1}{3}\pi r^2 h$",
    size=18,
    ha="center",
    va="bottom",
    bbox=dict(boxstyle="round", pad=0.25,
              facecolor="none", edgecolor=cl[2], lw=3.5),
)

# Assinatura
axL.text(0.0, -0.385, r"@Ivan Lopes", size=11,
         c=".2", alpha=0.35, ha="center", va="bottom")


# ----------------------------
# Artistas dinâmicos (criados UMA vez)
# ----------------------------
Path = mpath.Path

# Volume acumulado (cone interno até ρ): cor cl[0]
acc_patch = patches.PathPatch(
    Path([(0, 0)], [Path.MOVETO]),
    fc=cl[0],
    ec="none",
    alpha=0.55,
    zorder=1,
)
axL.add_patch(acc_patch)

# Conjunto de cascas (rastro): NSHELLS patches
shell_patches = []
for _ in range(NSHELLS):
    p = patches.PathPatch(
        Path([(0, 0)], [Path.MOVETO]),
        fc=cl[1],
        ec="none",
        alpha=0.0,
        zorder=3,
    )
    axL.add_patch(p)
    shell_patches.append(p)

# Círculo superior da casca MAIS RECENTE (reforça o “tubo” atual)
(shell_top_line,) = axL.plot([], [], "--", c=cl[1], lw=1.2, alpha=0.95, zorder=4)

# Indicadores numéricos
info_text = axL.text(
    0.62,
    0.92,
    "",
    transform=axL.transAxes,
    ha="left",
    va="top",
    fontsize=14,
    bbox=dict(boxstyle="round", pad=0.35, facecolor="white",
              alpha=0.75, edgecolor="0.8"),
)

# Gráfico do integrando A(ρ)
rho_plot = np.linspace(0, r, 400)
A_plot = A_of_rho(rho_plot)
(axA,) = axR.plot(rho_plot, A_plot, lw=2.0)

# marcador no ponto atual
(marker,) = axR.plot([0], [A_of_rho(0.0)], marker="o", markersize=7)

# Texto no gráfico
gtext = axR.text(0.02, 0.98, "", transform=axR.transAxes,
                 ha="left", va="top", fontsize=12)

# manter referência ao preenchimento (para remover/atualizar)
fill_ref = None

# LaTeX puro (sem números) pode ser raw
latex_Vtotal = r"$V_{\rm total}=\frac{1}{3}\pi r^2 h$"


# ----------------------------
# Helpers para construir Paths
# ----------------------------
def make_shell_path(rho, drho):
    """
    Casca de espessura drho entre rho-drho e rho.
    Retorna (Path, z_top_externo).
    """
    rho_in = max(rho - drho, 0.0)
    rho_out = rho

    z_out = h_of_rho(rho_out)
    z_in = h_of_rho(rho_in)

    verts = []

    # contorno externo (base → topo)
    for t in theta + np.pi:
        verts.append(
            xy0 + c32([rho_out * np.cos(t), rho_out * np.sin(t), 0.0]))
    for t in reversed(theta + np.pi):
        verts.append(
            xy0 + c32([rho_out * np.cos(t), rho_out * np.sin(t), z_out]))

    # contorno interno (topo → base)
    for t in theta + np.pi:
        verts.append(xy0 + c32([rho_in * np.cos(t), rho_in * np.sin(t), z_in]))
    for t in reversed(theta + np.pi):
        verts.append(xy0 + c32([rho_in * np.cos(t), rho_in * np.sin(t), 0.0]))

    verts.append(verts[0])

    codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 2) + [Path.CLOSEPOLY]
    return Path(verts, codes), z_out


def make_acc_path(rho):
    """
    Cone interno até rho: borda na altura z_top e vértice em z=h.
    """
    z_top = h_of_rho(rho)
    verts = []

    for t in theta + np.pi:
        verts.append(xy0 + c32([rho * np.cos(t), rho * np.sin(t), z_top]))

    verts.append(xy0 + c32([0.0, 0.0, h]))
    verts.append(verts[0])

    codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 2) + [Path.CLOSEPOLY]
    return Path(verts, codes), z_top


def alpha_for_k(k, n):
    """
    k = 0 é a casca mais recente.
    k = n-1 é a mais antiga (mais transparente).
    """
    if n <= 1:
        return alpha_shell_max
    t = k / (n - 1)
    return (1 - t) * alpha_shell_max + t * alpha_shell_min


# ----------------------------
# Animação
# ----------------------------
def init():
    acc_patch.set_path(Path([(0, 0)], [Path.MOVETO]))
    shell_top_line.set_data([], [])

    for p in shell_patches:
        p.set_path(Path([(0, 0)], [Path.MOVETO]))
        p.set_alpha(0.0)

    marker.set_data([0.0], [A_of_rho(0.0)])
    gtext.set_text("")
    info_text.set_text("")
    return (acc_patch, shell_top_line, marker, gtext, info_text, *shell_patches)


def animate(i):
    global fill_ref

    rho_now = float(rho_vals[i])

    # 1) Atualiza volume acumulado (cone interno)
    acc_path, _ = make_acc_path(rho_now)
    acc_patch.set_path(acc_path)

    # 2) Atualiza o “rastro” de cascas: últimas NSHELLS
    # k=0: casca mais recente (índice i), k=1: i-1, etc.
    z_out_recent = None
    rho_recent = None

    for k in range(NSHELLS):
        idx = i - k
        p = shell_patches[k]

        if idx < 0:
            # ainda não existe casca para esse idx
            p.set_alpha(0.0)
            continue

        rho_k = float(rho_vals[idx])
        shell_path, z_out = make_shell_path(rho_k, drho)
        p.set_path(shell_path)
        p.set_alpha(alpha_for_k(k, NSHELLS))

        if k == 0:
            z_out_recent = z_out
            rho_recent = rho_k

    # 3) Linha do topo apenas para a casca mais recente
    if rho_recent is not None and z_out_recent is not None:
        xt = xy0[0] + c32([rho_recent * np.cos(theta), rho_recent *
                          np.sin(theta), 0 * theta + z_out_recent])[0]
        yt = xy0[1] + c32([rho_recent * np.cos(theta), rho_recent *
                          np.sin(theta), 0 * theta + z_out_recent])[1]
        shell_top_line.set_data(xt, yt)
    else:
        shell_top_line.set_data([], [])

    # 4) Indicadores numéricos
    V_now = V_of_rho(rho_now)
    A_now = A_of_rho(rho_now)

    info_text.set_text(
        f"$\\rho={rho_now:.3f}$\n"
        f"$h(\\rho)=h\\left(1-\\rho/r\\right)={h_of_rho(rho_now):.3f}$\n"
        f"$A(\\rho)=2\\pi\\rho\\,h(\\rho)={A_now:.3f}$\n"
        f"$V(\\rho)=\\int_0^\\rho A(s)\\,ds={V_now:.4f}$\n"
        + latex_Vtotal + f" = {V_total:.4f}"
    )

    # 5) Gráfico do integrando
    marker.set_data([rho_now], [A_now])
    gtext.set_text(f"A(ρ) no ponto: {A_now:.4f}")

    # Atualiza preenchimento (removendo o anterior com segurança)
    if fill_ref is not None:
        try:
            fill_ref.remove()
        except Exception:
            pass

    fill_ref = axR.fill_between(
        rho_plot, 0, A_plot, where=(rho_plot <= rho_now), alpha=0.20)

    return (acc_patch, shell_top_line, marker, gtext, info_text, *shell_patches)


anim = animation.FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=Nf,
    interval=20,
    blit=False,
)

# ----------------------------
# Salvar
# ----------------------------
print("Salvando animação...")
anim.save(
    "volume_cone_shells_trail.mp4",
    writer=animation.FFMpegWriter(fps=60),
    dpi=200,
)
print("✓ Animação salva: volume_cone_shells_trail.mp4")
