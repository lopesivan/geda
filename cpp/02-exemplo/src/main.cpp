#include <iostream>

extern "C"
{
#include <libgeda/libgeda.h>
#include <libgedacairo/libgedacairo.h>
}

int main(int argc, char* argv[])
{
    std::cout << "gEDA C++ Application\n";
    std::cout << "====================\n";
    std::cout << "libgeda: headers disponíveis\n";
    std::cout << "libgedacairo: headers disponíveis\n";

    if(argc > 1)
    {
        std::cout << "Arquivo solicitado: " << argv[1] << '\n';
    }

    return 0;
}
