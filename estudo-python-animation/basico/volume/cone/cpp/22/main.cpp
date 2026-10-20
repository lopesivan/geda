#define _USE_MATH_DEFINES
#include <cmath>
#include <vector>
#include "matplotlibcpp.h"

namespace plt = matplotlibcpp;

int main()
{
    int n = 1000;

    std::vector<double> x, y_sin, y_cos;

    for(int i = 0; i < n; i++)
    {
        // variável independente
        double xi = i * i;   // x = i²

        x.push_back(xi);

        // seno e cosseno
        y_sin.push_back(std::sin(2 * M_PI * i / 360.0));
        y_cos.push_back(std::cos(2 * M_PI * i / 360.0));

        if(i % 10 == 0)
        {
            plt::clf();

            // seno
            plt::named_plot("sin(2πi/360)", x, y_sin);

            // cosseno
            plt::named_plot("cos(2πi/360)", x, y_cos);

            plt::xlim(0, n * n);
            plt::title("Seno e Cosseno");
            plt::legend();
            plt::pause(0.01);
        }
    }
}

