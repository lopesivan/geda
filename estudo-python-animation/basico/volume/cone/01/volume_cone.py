"""
Animação do Cálculo do Volume de um Cone usando 3 Métodos de Integração
========================================================================

Mostra visualmente como calcular V = (1/3)πr²h usando:
1. Cascas cilíndricas (variando ρ)
2. Fatias angulares (variando φ)
3. Discos horizontais (variando z)

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

    Matemática:
        - x_2d = y - x*sin(45°)/2
        - y_2d = z - x*cos(45°)/2

    Isso cria uma projeção onde:
        - Eixo X aponta para baixo-esquerda
        - Eixo Y aponta para baixo-direita
        - Eixo Z aponta para cima
    """
    return np.array([
        xyz[1] - xyz[0] * np.sin(np.pi/4) / 2,  # componente x da projeção
        xyz[2] - xyz[0] * np.cos(np.pi/4) / 2   # componente y da projeção
    ])


# ==============================================================================
# CONFIGURAÇÃO DA ANIMAÇÃO
# ==============================================================================

Nf = 600  # Número de frames da animação
cl = list(cm.tab10.colors)  # Paleta de 10 cores do matplotlib

# Criação da figura
fig = pyplot.figure(figsize=([9, 9]))
xlim = [-1.2, 1.2]
ylim = [-1.2, 1.2]

# Dois eixos sobrepostos:
# - ax1: dinâmico (limpo a cada frame para animação)
# - ax: estático (desenha estrutura fixa: eixos, contornos, fórmulas)
ax1 = fig.add_axes([0, 0, 1, 1], xlim=xlim, ylim=ylim, fc='none')
ax1.axis('off')

ax = fig.add_axes([0, 0, 1, 1], xlim=xlim, ylim=ylim, fc='none')
ax.axis('off')

# Título
ax.text(np.sum(xlim)/2, 1, 'Cone Volume',
        size=35, ha='center', va='bottom')


# ==============================================================================
# PARÂMETROS GEOMÉTRICOS
# ==============================================================================

# Ângulos de visibilidade para simular profundidade
# t1 e t2 definem quais partes do círculo são "visíveis" vs "ocultas"
t1 = np.pi - np.atan(2*np.sqrt(2))  # ~135° - início da parte visível
t2 = t1 + np.pi                      # ~315° - fim da parte visível
theta = np.linspace(t1, t2, 100)     # Ângulos para arcos visíveis

# Posições dos 3 cones (esquerda, centro, direita)
xy = np.array([
    [-.8, .2],  # Método 1: cascas cilíndricas
    [0, .2],    # Método 2: fatias angulares
    [.8, .2]    # Método 3: discos horizontais
])

# Tamanho dos eixos de coordenadas
xm, ym, zm = .4, .4, .8

# Dimensões do cone
r = .3   # raio da base
h = .75  # altura

# Parâmetros de integração (arrays de 0 a valor máximo)
rho = np.linspace(0, r, Nf)        # raio para cascas cilíndricas
phi = np.linspace(0, 2*np.pi, Nf)  # ângulo para fatias angulares
z = np.linspace(0, h, Nf)          # altura para discos horizontais

# Encontra índices onde phi cruza os ângulos de visibilidade
# (usado para controlar zorder e simular profundidade)
t1_index = np.argmin(np.abs(phi - t1))  # mais eficiente que min/lambda
t2_index = np.argmin(np.abs(phi - t2))


# ==============================================================================
# DESENHO DA ESTRUTURA ESTÁTICA (3 CONES)
# ==============================================================================

for k in range(3):
    # ---------------------
    # Eixos de coordenadas (x, y, z)
    # ---------------------
    axes_vectors = [
        c32([xm, 0, 0]),   # eixo x
        c32([0, ym, 0]),   # eixo y
        c32([0, 0, zm])    # eixo z
    ]

    for i, axis_vec in enumerate(axes_vectors):
        ax.annotate('',
                    xy[k] + axis_vec,  # ponta da seta
                    xy[k],              # origem da seta
                    arrowprops=dict(arrowstyle='->', lw=1, color='k'))

    # ---------------------
    # Contorno da base do cone
    # ---------------------
    # Parte visível (tracejada na frente)
    ax.plot(xy[k][0] + r*c32([np.cos(theta), np.sin(theta), 0*theta])[0],
            xy[k][1] + r*c32([np.cos(theta), np.sin(theta), 0*theta])[1],
            '--', c=cl[0], lw=1.2, alpha=.6)

    # Parte oculta (contínua atrás)
    ax.plot(xy[k][0] + r*c32([-np.cos(theta), -np.sin(theta), 0*theta])[0],
            xy[k][1] + r*c32([-np.cos(theta), -np.sin(theta), 0*theta])[1],
            '-', c=cl[0], lw=2, alpha=.6)

    # ---------------------
    # Arestas laterais do cone (da base ao vértice)
    # ---------------------
    for i in range(2):
        # Duas arestas: em t1 e t1+π (lados opostos)
        edge_angle = t1 + np.pi * i
        base_point = xy[k] + c32([r*np.cos(edge_angle),
                                  r*np.sin(edge_angle), 0])
        apex_point = xy[k] + [0, h]  # vértice do cone em (0, h)

        ax.plot([base_point[0], apex_point[0]],
                [base_point[1], apex_point[1]],
                c=cl[0], lw=1, alpha=.6)

    # ---------------------
    # Dimensões anotadas (r e h)
    # ---------------------
    # Linha do raio
    ax.plot([xy[k][0], xy[k][0] + r*c32([np.cos(t1), np.sin(t1), 0])[0]],
            [xy[k][1], xy[k][1] + r*c32([np.cos(t1), np.sin(t1), 0])[1]],
            '--', c='k', lw=1.2)

    # Label 'r'
    ax.text(xy[k][0] + r*c32([np.cos(t1), np.sin(t1), 0])[0]/2,
            xy[k][1] + r*c32([np.cos(t1), np.sin(t1), 0])[1]/2,
            '$r$', size=25, c='k', ha='center', va='bottom')

    # Label 'h'
    ax.text(xy[k][0], xy[k][1] + h/2,
            '$h$', size=25, c='k', ha='right', va='center')

    # ---------------------
    # Fórmulas matemáticas (diferencial, integral, resultado)
    # ---------------------

    # Fórmula do elemento diferencial dV
    differentials = [
        # cascas cilíndricas
        r'$dV=2\pi\rho\left(h-\frac{h}{r}\rho\right)d\rho$',
        # fatias angulares (corrigido)
        r'$dV=\frac{1}{3}rh \cdot d\varphi$',
        # discos horizontais
        r'$dV = \pi \left(r-\frac{r}{h}z\right)^2 dz$'
    ]

    ax.text(xy[k][0], xy[k][1] - .3, differentials[k],
            size=18, ha='center', va='bottom',
            bbox=dict(boxstyle='ellipse', pad=0,
                      facecolor='none', edgecolor=cl[1], lw=3))

    # Fórmula da integral
    integrals = [
        r'$V=\int_0^r 2\pi\rho\left(h-\frac{h}{r}\rho\right) d\rho$',
        r'$V=\int_0^{2\pi} \frac{1}{3}rh \cdot d\varphi$',
        r'$V=\int_0^h  \pi \left(r-\frac{r}{h}z\right)^2 dz$'
    ]

    ax.text(xy[k][0], xy[k][1] - .7, integrals[k],
            size=20, ha='center', va='bottom',
            bbox=dict(boxstyle='round', pad=.2,
                      facecolor='none', edgecolor=cl[0], lw=3))

    # Resultado final
    ax.text(xy[k][0], xy[k][1] - 1.15,
            # fórmula correta (era h/3, agora 1/3)
            r'$V= \frac{1}{3}\pi r^2h$',
            size=40, ha='center', va='bottom',
            bbox=dict(boxstyle='roundtooth', pad=.6,
                      facecolor='none', edgecolor=cl[2], lw=5))


# ==============================================================================
# FUNÇÃO DE ANIMAÇÃO
# ==============================================================================

def animate(i):
    """
    Desenha os elementos dinâmicos da animação no frame i

    Para cada frame:
    1. Limpa o eixo dinâmico (ax1)
    2. Desenha cascas/fatias/discos progressivamente
    3. Usa zorder para simular profundidade

    Args:
        i: índice do frame atual (0 até Nf-1)
    """
    if i % 50 == 0:
        print(f"Frame {i}/{Nf}")

    # Limpa e reconfigura o eixo dinâmico
    ax1.cla()
    ax1.set_xlim(xlim)
    ax1.set_ylim(ylim)
    ax1.axis('off')

    # ==========================================================================
    # MÉTODO 1: Cascas Cilíndricas (varying ρ)
    # ==========================================================================
    # Integra usando cascas cilíndricas de raio ρ e altura h(1-ρ/r)

    # Casca cilíndrica: retângulo enrolado
    # - Base inferior: círculo de raio ρ em z=0
    # - Topo superior: círculo de raio ρ em z=h-h*ρ/r (linha do cone)

    # Vértices da casca (base + topo invertido)
    verts = []
    # Base (círculo inferior)
    for t in theta + np.pi:
        verts.append(xy[0] + c32([rho[i]*np.cos(t), rho[i]*np.sin(t), 0]))

    # Topo (círculo superior na superfície do cone) - invertido
    for t in reversed(theta + np.pi):
        z_top = h - h/r * rho[i]  # altura no cone
        verts.append(xy[0] + c32([rho[i]*np.cos(t), rho[i]*np.sin(t), z_top]))

    verts.append((0, 0))  # fecha o polígono

    # Desenha a casca
    codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
        (len(verts)-2) + [path.Path.CLOSEPOLY]
    ax1.add_patch(patches.PathPatch(
        path.Path(verts, codes),
        fc=cl[1], ec='none', alpha=.8, zorder=1
    ))

    # Círculo superior da casca (tracejado)
    z_top = h - h/r * rho[i]
    ax1.plot(
        xy[0][0] + c32([rho[i]*np.cos(theta), rho[i]*np.sin(theta),
                        0*theta + z_top])[0],
        xy[0][1] + c32([rho[i]*np.cos(theta), rho[i]*np.sin(theta),
                        0*theta + z_top])[1],
        '--', c=cl[1], lw=1.2, zorder=-2
    )

    # Volume acumulado (cone interno até ρ)
    verts = []
    for t in theta + np.pi:
        verts.append(xy[0] + c32([rho[i]*np.cos(t), rho[i]*np.sin(t), z_top]))
    verts.append(xy[0] + c32([0, 0, h]))  # vértice do cone
    verts.append((0, 0))

    codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
        (len(verts)-2) + [path.Path.CLOSEPOLY]
    ax1.add_patch(patches.PathPatch(
        path.Path(verts, codes),
        fc=cl[0], ec='none', alpha=.8, zorder=1
    ))

    # ==========================================================================
    # MÉTODO 2: Fatias Angulares (varying φ)
    # ==========================================================================
    # Integra usando fatias como pedaços de pizza do vértice até a base

    # Controle de visibilidade com zorder (frente vs atrás)
    if i < t1_index:
        # Fase 1: apenas a parte da frente
        verts = []
        for t in phi[:i+1]:
            verts.append(xy[1] + c32([r*np.cos(t), r*np.sin(t), 0]))
        verts.append(xy[1] + c32([0, 0, h]))  # vértice
        verts.append((0, 0))

        codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
            (len(verts)-2) + [path.Path.CLOSEPOLY]
        ax1.add_patch(patches.PathPatch(
            path.Path(verts, codes),
            fc=cl[0], ec='none', alpha=.8, zorder=1
        ))

    elif i < t2_index:
        # Fase 2: parte da frente + parte de trás (com zorder diferente)

        # Frente (zorder=1)
        verts = []
        for t in phi[:t1_index+1]:
            verts.append(xy[1] + c32([r*np.cos(t), r*np.sin(t), 0]))
        verts.append(xy[1] + c32([0, 0, h]))
        verts.append((0, 0))

        codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
            (len(verts)-2) + [path.Path.CLOSEPOLY]
        ax1.add_patch(patches.PathPatch(
            path.Path(verts, codes),
            fc=cl[0], ec='none', alpha=.8, zorder=1
        ))

        # Trás (zorder=-1, renderiza atrás)
        verts = []
        for t in phi[t1_index:i+1]:
            verts.append(xy[1] + c32([r*np.cos(t), r*np.sin(t), 0]))
        verts.append(xy[1] + c32([0, 0, h]))
        verts.append((0, 0))

        codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
            (len(verts)-2) + [path.Path.CLOSEPOLY]
        ax1.add_patch(patches.PathPatch(
            path.Path(verts, codes),
            fc=cl[0], ec='none', alpha=.8, zorder=-1
        ))

    else:
        # Fase 3: três partes (frente, trás, frente)

        # Parte 1 (frente)
        verts = []
        for t in phi[:t1_index+1]:
            verts.append(xy[1] + c32([r*np.cos(t), r*np.sin(t), 0]))
        verts.append(xy[1] + c32([0, 0, h]))
        verts.append((0, 0))

        codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
            (len(verts)-2) + [path.Path.CLOSEPOLY]
        ax1.add_patch(patches.PathPatch(
            path.Path(verts, codes),
            fc=cl[0], ec='none', alpha=.8, zorder=1
        ))

        # Parte 2 (trás)
        verts = []
        for t in phi[t1_index:t2_index+1]:
            verts.append(xy[1] + c32([r*np.cos(t), r*np.sin(t), 0]))
        verts.append(xy[1] + c32([0, 0, h]))
        verts.append((0, 0))

        codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
            (len(verts)-2) + [path.Path.CLOSEPOLY]
        ax1.add_patch(patches.PathPatch(
            path.Path(verts, codes),
            fc=cl[0], ec='none', alpha=.8, zorder=-1
        ))

        # Parte 3 (frente)
        verts = []
        for t in phi[t2_index:i+1]:
            verts.append(xy[1] + c32([r*np.cos(t), r*np.sin(t), 0]))
        verts.append(xy[1] + c32([0, 0, h]))
        verts.append((0, 0))

        codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
            (len(verts)-2) + [path.Path.CLOSEPOLY]
        ax1.add_patch(patches.PathPatch(
            path.Path(verts, codes),
            fc=cl[0], ec='none', alpha=.8, zorder=1
        ))

    # Fatia atual (destacada em cor diferente)
    verts = [
        xy[1],
        xy[1] + c32([r*np.cos(phi[i]), r*np.sin(phi[i]), 0]),
        xy[1] + c32([0, 0, h]),
        (0, 0)
    ]

    codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
        (len(verts)-2) + [path.Path.CLOSEPOLY]
    ax1.add_patch(patches.PathPatch(
        path.Path(verts, codes),
        fc=cl[1], ec='none', lw=2, alpha=.8, zorder=0
    ))

    # ==========================================================================
    # MÉTODO 3: Discos Horizontais (varying z)
    # ==========================================================================
    # Integra empilhando discos de raio r(1-z/h)

    # Raio do disco na altura z[i]
    r_disk = r - z[i]*r/h

    # Disco atual (destacado)
    verts = []
    for t in phi:
        verts.append(xy[2] + c32([r_disk*np.cos(t), r_disk*np.sin(t), z[i]]))
    verts.append((0, 0))

    codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
        (len(verts)-2) + [path.Path.CLOSEPOLY]
    ax1.add_patch(patches.PathPatch(
        path.Path(verts, codes),
        fc=cl[1], ec='none', alpha=.8, zorder=2
    ))

    # Volume acumulado (cone truncado da base até z[i])
    verts = []
    # Topo (disco atual)
    for t in theta + np.pi:
        verts.append(xy[2] + c32([r_disk*np.cos(t), r_disk*np.sin(t), z[i]]))

    # Base (disco completo em z=0) - invertido
    for t in reversed(theta + np.pi):
        verts.append(xy[2] + c32([r*np.cos(t), r*np.sin(t), 0]))

    codes = [path.Path.MOVETO] + [path.Path.LINETO] * \
        (len(verts)-2) + [path.Path.CLOSEPOLY]
    ax1.add_patch(patches.PathPatch(
        path.Path(verts, codes),
        fc=cl[0], ec='none', lw=2, alpha=.8, zorder=1
    ))

    return []


# ==============================================================================
# RENDERIZAÇÃO E SALVAMENTO
# ==============================================================================

# Assinatura
ax.text(np.average(ax.get_xlim()),
        ax.get_ylim()[0]*.99 + ax.get_ylim()[1]*.01,
        r'@Ivan Carlos Lopes',
        size=12, c='.2', alpha=.3, ha='center', va='bottom')

# Cria a animação
anim = animation.FuncAnimation(fig, animate, frames=Nf, interval=20)

# Salva como vídeo MP4
print("Salvando animação...")
anim.save("volume_cone.mp4", writer=animation.FFMpegWriter(fps=60), dpi=200)
print("✓ Animação salva: volume_cone.mp4")

#
