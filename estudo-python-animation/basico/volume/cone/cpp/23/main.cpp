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

