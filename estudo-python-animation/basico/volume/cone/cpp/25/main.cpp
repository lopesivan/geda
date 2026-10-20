#define _USE_MATH_DEFINES
#include <cmath>
#include <vector>
#include <string>
#include <sstream>
#include <iomanip>
#include <cstdlib>  // std::system
#include "matplotlibcpp.h"

namespace plt = matplotlibcpp;

static std::string frame_name(int frame_idx)
{
    std::ostringstream oss;
    oss << "frames/frame_" << std::setw(6) << std::setfill('0')
        << frame_idx << ".png";
    return oss.str();
}

int main()
{
    // Cria pasta para frames (Linux)
    (void)std::system("mkdir -p frames");

    // Aumenta a resolução do PNG (qualidade percebida).
    // Troque para 2560x1440 ou 3840x2160 se quiser ainda mais.
    plt::figure_size(1920, 1080);

    const int n = 1000;

    std::vector<double> x;
    std::vector<double> y_sin;
    std::vector<double> y_cos;

    x.reserve(n);
    y_sin.reserve(n);
    y_cos.reserve(n);

    int frame_idx = 0;

    for(int i = 0; i < n; ++i)
    {
        const double di = static_cast<double>(i);

        // Mesma ideia do seu código: x = i^2
        x.push_back(di * di);

        // Ângulo em radianos
        const double theta = 2.0 * M_PI * di / 360.0;
        y_sin.push_back(std::sin(theta));
        y_cos.push_back(std::cos(theta));

        // Salva 1 frame a cada 10 amostras
        if(i % 10 == 0)
        {
            plt::clf();

            // Nesta versão do matplotlib-cpp, o 4º argumento é
            // "format string". Exemplos: "r-" (vermelho linha),
            // "b--" (azul tracejado), "k-" (preto).
            plt::named_plot("sin(2pi*i/360)", x, y_sin, "r-");
            plt::named_plot("cos(2pi*i/360)", x, y_cos, "b-");

            // Fixar limites evita “tremedeira” no vídeo
            plt::xlim(0.0,
                      static_cast<double>(n) *
                          static_cast<double>(n));
            plt::ylim(-1.1, 1.1);

            plt::title("Seno e Cosseno (frames PNG)");
            plt::legend();

            // Salva PNG
            plt::save(frame_name(frame_idx));
            ++frame_idx;
        }
    }

    return 0;
}
