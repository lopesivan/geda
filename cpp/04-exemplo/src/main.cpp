#include <cstdint>
#include <cstring>
#include <iostream>
#include <libguile.h>
#include "geda_bridge.h"

struct Args {
    int argc;
    char **argv;
};

static void *guile_main(void *data) {
    Args *a = static_cast<Args *>(data);
    intptr_t rc;

    if (!geda_bridge_check()) {
        std::cerr << "Falha na camada de integracao.\n";
        return reinterpret_cast<void *>(static_cast<intptr_t>(1));
    }
    if (a->argc < 2) {
        std::cerr << "uso: " << a->argv[0] << " [--sim] arquivo.sch\n";
        return reinterpret_cast<void *>(static_cast<intptr_t>(1));
    }

    if (a->argc >= 3 && std::strcmp(a->argv[1], "--sim") == 0)
        rc = geda_bridge_simulate(a->argv[2]);
    else
        rc = geda_bridge_list_components(a->argv[1]);

    return reinterpret_cast<void *>(rc);
}

int main(int argc, char **argv) {
    Args a{argc, argv};
    void *r = scm_with_guile(guile_main, &a);
    return static_cast<int>(reinterpret_cast<intptr_t>(r));
}
