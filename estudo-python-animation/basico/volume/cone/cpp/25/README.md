Para melhorar a qualidade, você tem dois “pontos de controle” principais:

1. **Como o matplotlib gera o PNG** (tamanho e DPI).
2. **Como o FFmpeg codifica o vídeo** (bitrate/CRF, perfil, pixel format).

Ajuste ambos.

---

## 1) Melhorar o PNG (tamanho + DPI)

No `matplotlibcpp`, a forma mais confiável é **definir o tamanho da figura** antes de salvar e **salvar com DPI alto** (quando suportado). Nem toda versão do wrapper expõe DPI diretamente, então eu deixo duas opções.

### Opção A: aumentar resolução pela figura (funciona quase sempre)

```cpp
plt::figure_size(1920, 1080);  // Full HD
```

Coloque isso **antes do loop** (uma vez), ou antes de salvar.

E ao salvar, mantenha:

```cpp
plt::save(frame_name(frame_idx));
```

Isso já aumenta muito a nitidez.

### Opção B: forçar DPI via `rcParams` (quando o wrapper permite `rcparams`)

Algumas versões aceitam:

```cpp
plt::rcparams({{"savefig.dpi", "300"}, {"figure.dpi", "150"}});
```

Se a sua versão não tiver `rcparams`, ignore.

### Opção C: salvar como SVG/PDF (qualidade máxima “vetorial”)

Se seu objetivo for **qualidade de imagem** (não necessariamente vídeo), o melhor é salvar em vetor:

```cpp
// frames/frame_000001.svg
```

Mas para vídeo, você vai acabar rasterizando depois, então PNG grande costuma ser a melhor prática.

---

## 2) Melhorar o vídeo no FFmpeg

Se você já tem PNGs bons, o gargalo passa a ser o encoder.

### Melhor qualidade visual (H.264 excelente)

```bash
ffmpeg -framerate 60 -i frames/frame_%06d.png \
  -c:v libx264 -pix_fmt yuv420p \
  -crf 16 -preset slow \
  output.mp4
```

Recomendações:

* `-crf 16` ou `-crf 14` (quanto menor, melhor; arquivo maior)
* `-preset slow` (melhor compressão com mesma qualidade)

### Qualidade ainda maior (10-bit, se seu player suportar)

```bash
ffmpeg -framerate 60 -i frames/frame_%06d.png \
  -c:v libx265 -pix_fmt yuv420p10le \
  -crf 18 -preset slow \
  output_hevc.mp4
```

HEVC costuma preservar gradientes/linhas finas melhor, mas nem todo dispositivo toca tão bem quanto H.264.

### “Sem perdas” (arquivo enorme)

```bash
ffmpeg -framerate 60 -i frames/frame_%06d.png \
  -c:v libx264 -qp 0 -pix_fmt yuv444p \
  output_lossless.mp4
```

* Isso tende a gerar arquivos muito grandes.
* `yuv444p` mantém mais fidelidade de cor (melhor para texto/linhas), mas compatibilidade pode cair.

---

## 3) Dicas específicas para gráficos (deixa tudo mais nítido)

No C++ (antes de salvar), fixe limites e aumente espessura/legibilidade:

```cpp
plt::xlim(0, n * n);
plt::ylim(-1.1, 1.1);

// Se seu wrapper aceitar kwargs:
plt::plot(x, y_sin, {{"linewidth", "2.5"}});
```

Se `linewidth` não funcionar no seu wrapper, ainda assim a melhora grande vem de `figure_size`.

---

## Receita pronta recomendada (equilíbrio ideal)

1. No C++:

* `plt::figure_size(1920, 1080);`
* Salvar PNG.

2. No FFmpeg:

* `-crf 16 -preset slow`

Isso normalmente dá vídeo bem limpo, sem estourar o tamanho.

---

Se você me disser sua resolução alvo (1080p, 1440p, 4K) e o FPS, eu te passo os valores exatos de `figure_size` e um comando FFmpeg já calibrado para isso.

