#include "geda_bridge.h"

#include <stdio.h>
#include <libgeda/libgeda.h>
#include <libgedacairo/libgedacairo.h>

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

        printf("%-10s %-12s %s\n",
               refdes ? refdes : "?",
               value ? value : "-",
               o->complex_basename ? o->complex_basename : "-");

        g_free(refdes);
        g_free(value);
    }

    s_toplevel_delete(toplevel);
    return 0;
}
