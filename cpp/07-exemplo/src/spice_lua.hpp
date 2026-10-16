#ifndef SPICE_LUA_HPP
#define SPICE_LUA_HPP

#include <string>

// Carrega o netlist na libngspice (ignora blocos .control/.endc),
// executa a simulação e roda o script Lua.
//
// Funções disponíveis no Lua:
//   rms("no")   -> valor RMS do sinal (integração no tempo)
//   peak("no")  -> maior valor absoluto do sinal
//   vec("no")   -> tabela Lua com as amostras (use vec("time") para o tempo)
//
// Retorna 0 em caso de sucesso.
int spice_lua_analyze(const std::string& netlist, const std::string& script);

#endif
