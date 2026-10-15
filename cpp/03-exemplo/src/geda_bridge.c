
#include "geda_bridge.h"

#include <libgeda/libgeda.h>
#include <libgedacairo/libgedacairo.h>

/*
 * Primeira função da camada intermediária.
 *
 * Ainda não inicializa o gEDA nem carrega esquemáticos.
 * Sua finalidade inicial é verificar se os headers podem
 * ser compilados em uma unidade de tradução C.
 */
int geda_bridge_check(void) {
    return 1;
}

