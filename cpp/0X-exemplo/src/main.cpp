
#include <iostream>
#include "geda_bridge.h"

int main() {
    std::cout << "gEDA C++ Application\n";
    std::cout << "====================\n";

    if (!geda_bridge_check()) {
        std::cerr << "Falha na camada de integracao.\n";
        return 1;
    }

    std::cout << "Camada C compilada e acessivel.\n";
    return 0;
}

