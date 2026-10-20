from matplotlib import pyplot, animation, cm
import numpy as np

# Configuração de fontes para matemática renderizar melhor
pyplot.rcParams.update({"font.family": "sans-serif", "mathtext.fontset": "cm"})


def hex(ax, a, xy=(0, 0), color='k'):
    """
    Desenha um hexágono regular usando números complexos

    Args:
        ax: eixo do matplotlib
        a: raio (distância do centro aos vértices)
        xy: posição do centro (x, y)
        color: cor da linha

    Matemática:
        - Hexágono tem 6 vértices separados por 60° (π/3 radianos)
        - Usa fórmula de Euler: e^(iθ) = cos(θ) + i·sin(θ)
        - Multiplica por 'a' para escalar o raio
        - Começa em -π/6 (-30°) e vai até 11π/6 (330°) com 7 pontos
          (7 pontos para fechar o polígono, não 6)
    """
    # Gera 7 pontos angulares igualmente espaçados (fecha o hexágono)
    pts = a * np.exp(1j * np.linspace(-np.pi/6, 11*np.pi/6, 7)
                     ) + xy[0] + 1j*xy[1]

    # Plota o hexágono usando parte real (x) e imaginária (y)
    ax.plot(pts.real, pts.imag, color=color, lw=2)
    return


def hex_star(ax, a, xy=(0, 0)):
    """
    Desenha uma estrela de 3 pontas (Y) dentro do hexágono

    Matemática:
        - Pega 3 vértices alternados do hexágono (separados por 120°)
        - Conecta o centro a cada um desses vértices
        - Cria divisões principais em 3 cores diferentes
    """
    # 3 pontos espaçados 120° (2π/3), começando em 30° (π/6)
    pts = a * np.exp(1j * np.linspace(np.pi/6, 9*np.pi/6, 3))

    # Desenha 3 linhas do centro para cada vértice
    for k in range(3):
        p = pts[k]
        ax.plot([xy[0], xy[0] + p.real],
                [xy[1], xy[1] + p.imag],
                lw=2, c=cl[k], zorder=-1)  # zorder=-1 coloca atrás
    return


def hex_grid(ax, a, xy=(0, 0), n=6):
    """
    Desenha uma grade interna no hexágono com linhas paralelas

    Args:
        n: número de subdivisões (quanto maior, mais linhas)

    Matemática:
        - Usa os mesmos 3 vértices da estrela
        - Para cada direção, desenha (n-1) linhas paralelas
        - As linhas começam nos lados adjacentes e vão na direção do vértice oposto
    """
    # Mesmos 3 pontos da estrela (vértices principais)
    pts = a * np.exp(1j * np.linspace(np.pi/6, 9*np.pi/6, 3))

    # Para cada uma das 3 direções
    for k in range(3):
        p = pts[k]  # Vetor direção

        # Desenha n-1 linhas paralelas (l vai de 1 até n-1)
        for l in range(1, n):
            # Ponto inicial: interpolação no lado adjacente
            # pts[(k+1) % 3]/n*l move ao longo do lado adjacente
            xy1 = xy[0] + 1j*xy[1] + pts[(k+1) % 3]/n * l

            # Desenha linha paralela na direção p
            ax.plot([xy1.real, (xy1 + p).real],
                    [xy1.imag, (xy1 + p).imag],
                    # zorder=-2 vai mais atrás ainda
                    lw=1.2, c=cl[k], zorder=-2)
    return


# Paleta de cores (10 cores do matplotlib)
cl = list(cm.tab10.colors)

# Configuração da figura
fig = pyplot.figure(figsize=([9, 9]))
xlim = ylim = [-1, 1]

# Cálculo da grade de hexágonos
nc = 12  # Número de colunas
w = (xlim[1] - xlim[0]) / nc  # Largura de cada célula

# Raio do hexágono inscrito no círculo
# cos(30°) = cos(π/6) relaciona raio com largura
r = w / np.cos(np.pi/6) / 2

# Número de linhas necessárias para preencher a tela
nr = int(np.ceil(1/r)) + 2

# Cria eixo sem bordas
ax = fig.add_axes([0, 0, 1, 1], xlim=xlim, ylim=ylim, fc='none')
ax.axis('off')


def animate(i):
    """
    Função de animação - desenha hexágonos progressivamente

    Estratégia de animação em 3 fases:
        - Fase 0 (kk=0): Desenha os hexágonos vazios
        - Fase 1 (kk=1): Adiciona as estrelas (divisões Y)
        - Fase 2 (kk=2): Adiciona as grades internas

    Args:
        i: frame atual (vai de 0 até 3*nc*nr - 1)
    """
    if i % 50 == 0:
        print(i)  # Debug a cada 50 frames

    # Determina a fase (0, 1 ou 2)
    kk = i // (nc * nr)

    # Dentro de cada fase, determina qual hexágono desenhar
    ii = i % (nc * nr)

    # k = índice da linha, l = índice da coluna
    k = ii // nc
    l = ii % nc

    # Calcula a posição xy do hexágono atual
    # - Offset horizontal: w*(.5 + l + .5*(k % 2))
    #   O termo .5*(k % 2) faz linhas alternadas ficarem deslocadas (padrão hexagonal)
    # - Offset vertical: r*(1 + k*1.5)
    #   Multiplicador 1.5 compacta verticalmente (hexágonos se encaixam)
    hex_x = xlim[0] + w * (.5 + l + .5 * (k % 2))
    hex_y = ylim[0] + r * (1 + k * 1.5)

    # Fase 0: Desenha hexágonos com cores alternadas (3 cores)
    if kk == 0:
        hex(ax, r, color=cl[(k*nc + l) % 3], xy=(hex_x, hex_y))

    # Fase 1: Adiciona estrelas de 3 pontas
    if kk == 1:
        hex_star(ax, r, xy=(hex_x, hex_y))

    # Fase 2: Adiciona grades internas
    if kk == 2:
        hex_grid(ax, r, xy=(hex_x, hex_y))

    return


# Marca d'água
ax.text(np.average(ax.get_xlim()),
        ax.get_ylim()[0]*.99 + ax.get_ylim()[1]*.01,
        r'@Ivan Carlos Lopes',
        size=12, c='.2', alpha=.3, ha='center', va='bottom')

# Cria animação
# frames = 3*nc*nr porque são 3 fases, cada uma desenha nc*nr hexágonos
anim = animation.FuncAnimation(fig, animate, frames=3*nc*nr, interval=20)

# Salva como vídeo MP4
anim.save("hexagons.mp4", writer=animation.FFMpegWriter(fps=40), dpi=200)

#
