#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>

#include <libguile.h>

#include "geda_bridge.h"
#include "spice_lua.hpp"

#define GEDA_PREFIX "/opt/geda"

struct Args
{
    int    argc;
    char** argv;
};

static bool ends_with(const std::string& s,
                      const std::string& suffix)
{
    return s.size() >= suffix.size() &&
           s.compare(s.size() - suffix.size(),
                     suffix.size(),
                     suffix) == 0;
}

// .sch -> gera saida.cir com o gnetlist; outro arquivo (.sp/.cir) é
// usado direto.
static int analyze(const std::string& input,
                   const std::string& script)
{
    std::string netlist = input;

    if(ends_with(input, ".sch"))
    {
        netlist = "saida.cir";

        const std::string cmd =
            std::string(GEDA_PREFIX
                        "/bin/gnetlist -g spice-sdb -o '") +
            netlist + "' '" + input + "'";

        std::cout << "$ " << cmd << '\n';

        if(std::system(cmd.c_str()) != 0)
        {
            std::cerr << "gnetlist falhou\n";
            return 1;
        }
    }

    return spice_lua_analyze(netlist, script);
}

static void usage(const char* prog)
{
    std::cerr
        << "uso:\n"
        << "  " << prog << " arquivo.sch\n"
        << "  " << prog << " --sim arquivo.sch\n"
        << "  " << prog
        << " --render saida.{png,pdf,svg} arquivo.sch\n"
        << "  " << prog
        << " --analyze {arquivo.sch|circuito.sp} analise.lua\n";
}

static void* guile_main(void* data)
{
    Args*    a  = static_cast<Args*>(data);
    intptr_t rc = 1;

    if(!geda_bridge_check())
    {
        std::cerr << "Falha na camada de integracao.\n";
        return reinterpret_cast<void*>(rc);
    }

    if(a->argc < 2)
    {
        usage(a->argv[0]);
        return reinterpret_cast<void*>(rc);
    }

    const std::string mode = a->argv[1];

    if(mode == "--sim" && a->argc >= 3)
        rc = geda_bridge_simulate(a->argv[2]);
    else if(mode == "--render" && a->argc >= 4)
        rc = geda_bridge_render(a->argv[3], a->argv[2]);
    else if(mode == "--analyze" && a->argc >= 4)
        rc = analyze(a->argv[2], a->argv[3]);
    else if(mode.rfind("--", 0) == 0)
        usage(a->argv[0]);
    else
        rc = geda_bridge_list_components(a->argv[1]);

    return reinterpret_cast<void*>(rc);
}

int main(int argc, char** argv)
{
    Args  a{argc, argv};
    void* r = scm_with_guile(guile_main, &a);
    return static_cast<int>(reinterpret_cast<intptr_t>(r));
}
