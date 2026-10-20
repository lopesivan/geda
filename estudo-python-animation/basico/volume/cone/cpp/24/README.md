Você pode, sim: a ideia é **em vez de `pause()`**, você **salva uma imagem PNG por iteração** (ou a cada 10, como você já faz), e depois usa **FFmpeg** para juntar tudo em um vídeo.

Abaixo vai um modelo completo e direto.

---

## 1) C++: salvar cada frame em uma pasta

Pontos importantes:

* use `plt::save("frames/frame_000123.png")`
* garanta que a pasta exista (`mkdir -p frames`)
* mantenha um contador de frame independente do `i`

```cpp
#define _USE_MATH_DEFINES
#include <cmath>
#include <vector>
#include <string>
#include <sstream>
#include <iomanip>
#include <cstdlib>
#include "matplotlibcpp.h"

namespace plt = matplotlibcpp;

static std::string frame_name(int frame_idx)
{
    std::ostringstream oss;
    oss << "frames/frame_" << std::setw(6) << std::setfill('0') << frame_idx << ".png";
    return oss.str();
}

int main()
{
    // Crie a pasta antes (Linux). Alternativas: std::filesystem em C++17.
    std::system("mkdir -p frames");

    int n = 1000;
    std::vector<double> x, y_sin, y_cos;

    int frame_idx = 0;

    for(int i = 0; i < n; i++)
    {
        double xi = i * i;
        x.push_back(xi);

        y_sin.push_back(std::sin(2 * M_PI * i / 360.0));
        y_cos.push_back(std::cos(2 * M_PI * i / 360.0));

        if(i % 10 == 0)
        {
            plt::clf();

            plt::named_plot("sin(2πi/360)", x, y_sin);
            plt::named_plot("cos(2πi/360)", x, y_cos);

            plt::xlim(0, n * n);
            plt::ylim(-1.1, 1.1); // fixo para não “pular” o enquadramento
            plt::title("Seno e Cosseno");
            plt::legend();

            // Salva PNG do frame
            plt::save(frame_name(frame_idx));

            frame_idx++;
        }
    }

    return 0;
}
```

### Observações práticas

* `plt::ylim(-1.1, 1.1)` evita que o autoscale mude o enquadramento e gere “tremedeira” no vídeo.
* Se quiser 60 fps no vídeo final, você controla isso no FFmpeg (abaixo).

---

## 2) FFmpeg: juntar os PNGs em vídeo

Se seus arquivos estão como:
`frames/frame_000000.png`, `frames/frame_000001.png`, ...

Use:

```bash
ffmpeg -framerate 60 -i frames/frame_%06d.png \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium \
  output.mp4
```

### O que significa

* `-framerate 60`: interpreta a sequência como 60 quadros por segundo
* `frame_%06d.png`: `%06d` combina com 6 dígitos (000000, 000001, ...)
* `-pix_fmt yuv420p`: compatibilidade alta (players/celular)
* `-crf 18`: qualidade alta (menor = melhor, maior = mais compressão)

---

## 3) Como escolher FPS coerente com seu “i % 10 == 0”

Você está salvando **1 frame a cada 10 iterações**.
Se `n = 1000`, então você terá ~100 frames.

* Se você fizer `-framerate 30`, o vídeo terá ~3,3 s.
* Se você fizer `-framerate 60`, o vídeo terá ~1,7 s.

Se quiser um vídeo mais longo, ou:

* salve mais frames (ex.: `i % 5 == 0`)
* ou diminua `-framerate` (ex.: 24)

---

Se você me disser:

1. quanto tempo você quer que o vídeo tenha (ex.: 10 s), e
2. qual `n`, e se você salva a cada 10 ou a cada 1,

eu te devolvo a combinação exata (passo + fps) para bater exatamente na duração desejada.


