#include <cmath>
#include "matplotlibcpp.h"
#include <vector>

namespace plt = matplotlibcpp;

int main()
{
    int                 n = 500;
    std::vector<double> x(n), y(n);

    for(int i = 0; i < n; ++i)
    {
        x[i] = i;
        y[i] = std::sin(2 * M_PI * i / 360.0);
    }

    // Set a title
    plt::title("Sample Sine Wave Plot");

    // Plot the data
    plt::plot(x, y, "r-");  // "r-" specifies a red line style

    // Enable a grid
    plt::grid(true);

    // Show the plot and block the program until the window is
    // closed
    plt::show();

    return 0;
}
