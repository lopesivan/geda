Funcionou. O `?` em `title-B.sym` e `ground.sym` é normal: esses símbolos não têm `refdes`. O `A2` mostra o `value` da diretiva `.control` com as quebras de linha.

Próximo passo: gerar o netlist com o `gnetlist` do seu `/opt/geda` e rodar o ngspice em batch, direto do app. As APIs de nets/pinos do libgeda variam por versão, então o caminho via `gnetlist` é o mais seguro.

`src/geda_bridge.h`:
```c
#ifndef GEDA_BRIDGE_H
#define GEDA_BRIDGE_H

#ifdef __cplusplus
extern "C" {
#endif

int geda_bridge_check(void);
int geda_bridge_list_components(const char *filename);
int geda_bridge_simulate(const char *filename);

#ifdef __cplusplus
}
#endif

#endif
```

`src/geda_bridge.c`:
```c
#include "geda_bridge.h"

#include <stdio.h>
#include <stdlib.h>
#include <libgeda/libgeda.h>
#include <libgedacairo/libgedacairo.h>

#define GEDA_PREFIX "/opt/geda"

int geda_bridge_check(void) {
    return 1;
}

int geda_bridge_list_components(const char *filename) {
    static int inited = 0;
    TOPLEVEL *toplevel;
    PAGE *page;
    GError *err = NULL;
    const GList *iter;

    if (!inited) {
        libgeda_init();
        inited = 1;
    }

    toplevel = s_toplevel_new();
    i_vars_libgeda_set(toplevel);
    g_rc_parse(toplevel, "geda_bridge", "gafrc", NULL);

    page = s_page_new(toplevel, (gchar *)filename);
    if (!f_open(toplevel, page, filename, &err)) {
        fprintf(stderr, "f_open: %s\n", err ? err->message : "erro");
        g_clear_error(&err);
        s_toplevel_delete(toplevel);
        return 1;
    }

    for (iter = s_page_objects(page); iter != NULL; iter = g_list_next(iter)) {
        OBJECT *o = (OBJECT *)iter->data;
        if (o->type != OBJ_COMPLEX)
            continue;

        char *refdes = o_attrib_search_attached_attribs_by_name(o, "refdes", 0);
        char *value  = o_attrib_search_attached_attribs_by_name(o, "value", 0);

        if (refdes) { /* ignora title, ground etc. */
            printf("%-10s %-12s %s\n", refdes, value ? value : "-",
                   o->complex_basename ? o->complex_basename : "-");
        }

        g_free(refdes);
        g_free(value);
    }

    s_toplevel_delete(toplevel);
    return 0;
}

int geda_bridge_simulate(const char *filename) {
    char *cmd;
    int rc;

    cmd = g_strdup_printf(
        GEDA_PREFIX "/bin/gnetlist -g spice-sdb -o saida.cir '%s'", filename);
    printf("$ %s\n", cmd);
    rc = system(cmd);
    g_free(cmd);
    if (rc != 0) {
        fprintf(stderr, "gnetlist falhou (%d)\n", rc);
        return 1;
    }

    printf("$ ngspice -b -o saida.log saida.cir\n");
    rc = system("ngspice -b -o saida.log saida.cir");
    if (rc != 0) {
        fprintf(stderr, "ngspice falhou (%d)\n", rc);
        return 1;
    }

    printf("OK: saida.cir, saida.log\n");
    return 0;
}
```

`src/main.cpp`:
```cpp
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
```

Rodar:
```bash
build/app exemplo.sch          # lista componentes
build/app --sim exemplo.sch    # netlist + ngspice
```

Detalhes:
- No `exemplo.sch`, o `.control` tem `plot v(in) v(out)`, que não funciona em batch (`-b`). Para a simulação headless, troque por `write saida.raw v(in) v(out)` no diretivo `A2`.
- Confirme se o binário existe: `ls /opt/geda/bin/gnetlist`. Se o caminho for outro, ajuste `GEDA_PREFIX`.
- O `gnetlist` precisa dos símbolos e backends do mesmo prefixo. Se reclamar, rode com `export GEDADATA=/opt/geda/share/gEDA`.

Próximo passo: ler o `.raw` e plotar na sua própria GUI, ou renderizar o esquemático em PNG com `libgedacairo`? Para o PNG, mande a saída de:

```bash
grep -n "eda_renderer\|eda_cairo" /opt/geda/include/libgedacairo/*.h
```
