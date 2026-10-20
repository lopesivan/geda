#include "matplotlibcpp.h"
#include <cmath>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <vector>

namespace plt = matplotlibcpp;

const double PI = 3.14159265358979323846;
const int N_FRAMES = 60;      // Número de frames
const int N_POINTS = 200;     // Pontos na curva

int main()
{
    std::cout << "Gerando animação de onda senoidal..." << std::endl;

    // Configura backend não-interativo
    plt::backend("Agg");

    // Cria diretório para frames
    system("mkdir -p frames");

    // Vetores para x e y
    std::vector<double> x(N_POINTS);
    std::vector<double> y(N_POINTS);

    // Gera cada frame
    for(int frame = 0; frame < N_FRAMES; ++frame)
    {
        if(frame % 10 == 0)
        {
            std::cout << "Frame " << frame << "/" << N_FRAMES << std::endl;
        }

        // Fase da onda (varia de 0 a 2π)
        double phase = 2.0 * PI * frame / N_FRAMES;

        // Gera pontos da onda
        for(int i = 0; i < N_POINTS; ++i)
        {
            x[i] = 4.0 * PI * i / (N_POINTS - 1);  // x de 0 a 4π
            y[i] = std::sin(x[i] - phase);          // onda propagando
        }

        // Limpa figura anterior
        plt::clf();

        // Plota a onda
        plt::plot(x, y, "b-");

        // Configurações do gráfico
        plt::xlim(0.0, 4.0 * PI);
        plt::ylim(-1.5, 1.5);
        plt::xlabel("x");
        plt::ylabel("sin(x - t)");
        plt::title("Onda Senoidal");
        plt::grid(true);

        // Salva frame
        std::ostringstream filename;
        filename << "frames/frame_" << std::setfill('0')
                 << std::setw(4) << frame << ".png";
        plt::save(filename.str());
    }

    std::cout << "\n✓ Frames gerados em ./frames/" << std::endl;
    std::cout << "\nPara criar GIF, execute:" << std::endl;
    std::cout << "ffmpeg -framerate 15 -i frames/frame_%04d.png "
                 "-vf \"fps=15,scale=800:-1:flags=lanczos\" "
                 "sine_wave.gif" << std::endl;
    std::cout << "\nPara criar vídeo MP4:" << std::endl;
    std::cout << "ffmpeg -framerate 30 -i frames/frame_%04d.png "
                 "-c:v libx264 -pix_fmt yuv420p sine_wave.mp4"
              << std::endl;

    return 0;
}
