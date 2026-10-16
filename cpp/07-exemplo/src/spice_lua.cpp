#include "spice_lua.hpp"

#include <ngspice/sharedspice.h>

#include <lua.hpp>

#include <algorithm>
#include <cctype>
#include <cmath>
#include <cstring>
#include <fstream>
#include <iostream>
#include <memory>
#include <span>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

std::vector<double> g_time;

// ------------------------------------------------------------
// ngspice
// ------------------------------------------------------------

int send_char(char* text, int, void*)
{
    // Mostra só erros do ngspice; o resto é ruído.
    if(text && std::strncmp(text, "stderr", 6) == 0)
        std::cerr << text << '\n';

    return 0;
}

int controlled_exit(int status, bool, bool, int, void*)
{
    if(status != 0)
        std::cerr << "ngspice terminou com status " << status << '\n';

    return 0;
}

void ng_init_once()
{
    static bool done = false;

    if(done)
        return;

    if(ngSpice_Init(send_char,
                    nullptr,
                    controlled_exit,
                    nullptr,
                    nullptr,
                    nullptr,
                    nullptr) != 0)
    {
        throw std::runtime_error("Falha inicializando ngspice");
    }

    done = true;
}

void ng_command(const std::string& command)
{
    std::vector<char> buffer(command.begin(), command.end());

    buffer.push_back('\0');

    if(ngSpice_Command(buffer.data()) != 0)
        throw std::runtime_error("Erro ngspice: " + command);
}

std::vector<double> get_vector(const std::string& name)
{
    std::vector<char> buffer(name.begin(), name.end());

    buffer.push_back('\0');

    pvector_info info = ngGet_Vec_Info(buffer.data());

    if(!info || !info->v_realdata)
        throw std::runtime_error("Vetor nao encontrado: " + name);

    return {info->v_realdata, info->v_realdata + info->v_length};
}

// Carrega o netlist linha a linha, descartando .control ... .endc
// (comandos como "plot" abririam janelas e não servem em modo embutido).
void load_netlist(const std::string& path)
{
    std::ifstream in(path);

    if(!in)
        throw std::runtime_error("Nao foi possivel abrir " + path);

    std::vector<std::string> lines;

    std::string line;

    bool in_control = false;

    while(std::getline(in, line))
    {
        if(!line.empty() && line.back() == '\r')
            line.pop_back();

        std::string low = line;

        low.erase(low.begin(),
                  std::find_if(low.begin(), low.end(), [](unsigned char c) {
                      return !std::isspace(c);
                  }));

        std::transform(low.begin(), low.end(), low.begin(), [](unsigned char c) {
            return static_cast<char>(std::tolower(c));
        });

        if(low.rfind(".control", 0) == 0)
        {
            in_control = true;
            continue;
        }

        if(low.rfind(".endc", 0) == 0)
        {
            in_control = false;
            continue;
        }

        if(!in_control)
            lines.push_back(line);
    }

    std::vector<char*> ptrs;

    for(auto& l : lines)
        ptrs.push_back(l.data());

    ptrs.push_back(nullptr);

    if(ngSpice_Circ(ptrs.data()) != 0)
        throw std::runtime_error("Falha carregando netlist " + path);
}

// ------------------------------------------------------------
// RMS usando integração no tempo
// ------------------------------------------------------------

double rms(std::span<const double> time, std::span<const double> signal)
{
    if(time.size() != signal.size() || time.size() < 2)
        throw std::runtime_error("Vetores incompativeis");

    double integral = 0.0;

    for(std::size_t i = 1; i < signal.size(); ++i)
    {
        const double dt = time[i] - time[i - 1];

        const double x0 = signal[i - 1];

        const double x1 = signal[i];

        integral += dt / 3.0 * (x0 * x0 + x0 * x1 + x1 * x1);
    }

    const double duration = time.back() - time.front();

    return std::sqrt(integral / duration);
}

double peak(std::span<const double> signal)
{
    double p = 0.0;

    for(double x : signal)
        p = std::max(p, std::fabs(x));

    return p;
}

// ------------------------------------------------------------
// Funções visíveis para Lua
//
// Nunca deixa objeto C++ vivo na hora do lua_error (longjmp):
// a exceção é capturada, a mensagem é copiada para a pilha Lua
// e só depois o erro é lançado.
// ------------------------------------------------------------

template <class F>
bool guarded(lua_State* L, F&& f)
{
    try
    {
        f();
        return true;
    }
    catch(const std::exception& e)
    {
        lua_pushstring(L, e.what());
        return false;
    }
}

int lua_rms(lua_State* L)
{
    const char* name = luaL_checkstring(L, 1);

    double value = 0.0;

    if(!guarded(L, [&] {
           const auto signal = get_vector(name);
           value = rms(g_time, signal);
       }))
    {
        return lua_error(L);
    }

    lua_pushnumber(L, value);

    return 1;
}

int lua_peak(lua_State* L)
{
    const char* name = luaL_checkstring(L, 1);

    double value = 0.0;

    if(!guarded(L, [&] {
           const auto signal = get_vector(name);
           value = peak(signal);
       }))
    {
        return lua_error(L);
    }

    lua_pushnumber(L, value);

    return 1;
}

int lua_vec(lua_State* L)
{
    const char* name = luaL_checkstring(L, 1);

    std::vector<double> signal;

    if(!guarded(L, [&] { signal = get_vector(name); }))
        return lua_error(L);

    lua_createtable(L, static_cast<int>(signal.size()), 0);

    for(std::size_t i = 0; i < signal.size(); ++i)
    {
        lua_pushnumber(L, signal[i]);
        lua_rawseti(L, -2, static_cast<lua_Integer>(i + 1));
    }

    return 1;
}

using LuaState = std::unique_ptr<lua_State, decltype(&lua_close)>;

} // namespace

// ------------------------------------------------------------

int spice_lua_analyze(const std::string& netlist, const std::string& script)
{
    try
    {
        ng_init_once();

        load_netlist(netlist);

        ng_command("run");

        g_time = get_vector("time");

        std::cout << "Simulacao ok: " << g_time.size() << " pontos\n";

        LuaState L(luaL_newstate(), &lua_close);

        if(!L)
            throw std::runtime_error("Falha criando Lua");

        luaL_openlibs(L.get());

        lua_register(L.get(), "rms", lua_rms);
        lua_register(L.get(), "peak", lua_peak);
        lua_register(L.get(), "vec", lua_vec);

        if(luaL_dofile(L.get(), script.c_str()) != LUA_OK)
        {
            std::cerr << lua_tostring(L.get(), -1) << '\n';

            return 1;
        }

        return 0;
    }
    catch(const std::exception& e)
    {
        std::cerr << "Erro: " << e.what() << '\n';

        return 1;
    }
}
