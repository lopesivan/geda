1. Visualização em Colunas (O Mapa Mental)
Quando você vê ([X], [Y], [Z]), o computador "enxerga" isso:

| Ponto               | X (Profundidade) | Y (Largura) | Z (Altura) |
| :---                | :---             | :---        | :---       | :---                     |
| P1                  | 0                | 0           | 0          | Pousa na origem          |
| P2                  | 1                | 0           | 0          | Risca para frente        |
| P3                  | 1                | 1           | 0          | Risca para a direita     |
| P4                  | 0                | 1           | 0          | Risca para trás          |
| P5                  | 0                | 0           | 0          | Fecha o quadrado no chão |



pelo que entendi a representacao é a seguinte


uma mosca que vá para os seuintes pontos:

A (0,0,0)
B (0,0,1)
C (0,0,3)
E (0,5,0)
D (0,7,12)

    eu representaria assim:
    posicao_mosca=[
    (
[0, 0, 0, 0, 0],
[ 0, 0, 0, 5, 7],
[0, 1, 3, 0, 12 ]

     )
    ]
