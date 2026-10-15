#include <cstring>
#include <iostream>
#include "geda_bridge.h"

int main(int argc, char **argv) {
    if (!geda_bridge_check()) {
        std::cerr << "Falha na camada de integracao.\n";
        return 1;
    }
    if (argc < 2) {
        std::cerr << "uso: " << argv[0] << " [--sim] arquivo.sch\n";
        return 1;
    }
    if (argc >= 3 && std::strcmp(argv[1], "--sim") == 0)
        return geda_bridge_simulate(argv[2]);

    return geda_bridge_list_components(argv[1]);
}
