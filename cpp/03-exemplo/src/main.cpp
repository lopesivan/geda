#include <iostream>
#include <libguile.h>
#include "geda_bridge.h"

static void* run(void* data)
{
    char** argv = static_cast<char**>(data);
    return reinterpret_cast<void*>(static_cast<intptr_t>(
        geda_bridge_list_components(argv[1])));
}

int main(int argc, char** argv)
{
    if(argc < 2)
    {
        std::cerr << "uso: " << argv[0] << " arquivo.sch\n";
        return 1;
    }
    void* r = scm_with_guile(run, argv);
    return static_cast<int>(reinterpret_cast<intptr_t>(r));
}
