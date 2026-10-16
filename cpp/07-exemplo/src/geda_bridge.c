#include "geda_bridge.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <glib.h>
#include <cairo.h>
#include <cairo-pdf.h>
#include <cairo-svg.h>
#include <libgeda/libgeda.h>
#include <libgedacairo/libgedacairo.h>

#define GEDA_PREFIX "/opt/geda"

/* Renderer só para medir textos; vive até o fim do processo. */
static EdaRenderer *measure_renderer = NULL;

static int text_bounds_cb(void *user_data, OBJECT *o,
                          int *min_x, int *min_y,
                          int *max_x, int *max_y) {
    EdaRenderer *renderer = (EdaRenderer *)user_data;
    double l, t, r, b;

    if (!eda_renderer_get_user_bounds(renderer, o, &l, &t, &r, &b))
        return 0;

    *min_x = (int)floor(MIN(l, r));
    *max_x = (int)ceil(MAX(l, r));
    *min_y = (int)floor(MIN(t, b));
    *max_y = (int)ceil(MAX(t, b));
    return 1;
}

static void geda_init_once(void) {
    static int inited = 0;
    if (!inited) {
        cairo_surface_t *surf;
        cairo_t *cr;

        libgeda_init();

        surf = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, 1, 1);
        cr = cairo_create(surf);
        measure_renderer = eda_renderer_new(cr, NULL);
        inited = 1;
    }
}

static void set_color(COLOR *map, int idx, int r, int g, int b) {
    map[idx].r = (guint8)r;
    map[idx].g = (guint8)g;
    map[idx].b = (guint8)b;
    map[idx].a = 255;
    map[idx].enabled = TRUE;
}

/* Mapa claro: fundo branco, linhas escuras. Todas as cores habilitadas. */
static GArray *make_color_map(void) {
    GArray *colors = g_array_sized_new(FALSE, TRUE, sizeof(COLOR), MAX_COLORS);
    COLOR *m;
    int i;

    g_array_set_size(colors, MAX_COLORS);
    m = (COLOR *)colors->data;

    for (i = 0; i < MAX_COLORS; i++)
        set_color(m, i, 0, 0, 0);

    set_color(m, BACKGROUND_COLOR,          255, 255, 255);
    set_color(m, OUTPUT_BACKGROUND_COLOR,   255, 255, 255);
    set_color(m, PIN_COLOR,                   0,   0,   0);
    set_color(m, NET_ENDPOINT_COLOR,        200,   0,   0);
    set_color(m, GRAPHIC_COLOR,               0, 110,   0);
    set_color(m, NET_COLOR,                   0,   0, 190);
    set_color(m, ATTRIBUTE_COLOR,             0,   0,   0);
    set_color(m, LOGIC_BUBBLE_COLOR,          0, 110, 110);
    set_color(m, DETACHED_ATTRIBUTE_COLOR,  200,   0,   0);
    set_color(m, TEXT_COLOR,                  0,   0,   0);
    set_color(m, BUS_COLOR,                   0, 150,   0);
    set_color(m, JUNCTION_COLOR,            200,   0, 200);
    set_color(m, STROKE_COLOR,                0,   0,   0);
    set_color(m, LOCK_COLOR,                120, 120, 120);

    return colors;
}

static TOPLEVEL *geda_open_page(const char *filename, PAGE **out_page) {
    TOPLEVEL *toplevel;
    PAGE *page;
    GError *err = NULL;

    geda_init_once();

    toplevel = s_toplevel_new();
    i_vars_libgeda_set(toplevel);
    g_rc_parse(toplevel, "geda_bridge", "gafrc", NULL);

    /* Antes do f_open: o libgeda mede textos durante a leitura. */
    o_text_set_rendered_bounds_func(toplevel, text_bounds_cb, measure_renderer);

    page = s_page_new(toplevel, (gchar *)filename);
    if (!f_open(toplevel, page, filename, &err)) {
        fprintf(stderr, "f_open: %s\n", err ? err->message : "erro");
        g_clear_error(&err);
        s_toplevel_delete(toplevel);
        return NULL;
    }
    *out_page = page;
    return toplevel;
}

int geda_bridge_check(void) {
    return 1;
}

int geda_bridge_list_components(const char *filename) {
    TOPLEVEL *toplevel;
    PAGE *page;
    const GList *iter;

    toplevel = geda_open_page(filename, &page);
    if (!toplevel)
        return 1;

    for (iter = s_page_objects(page); iter != NULL; iter = g_list_next(iter)) {
        OBJECT *o = (OBJECT *)iter->data;
        if (o->type != OBJ_COMPLEX)
            continue;

        char *refdes = o_attrib_search_attached_attribs_by_name(o, "refdes", 0);
        char *value  = o_attrib_search_attached_attribs_by_name(o, "value", 0);

        if (refdes) {
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

static int has_ext(const char *name, const char *ext) {
    size_t n = strlen(name), e = strlen(ext);
    return n >= e && g_ascii_strcasecmp(name + n - e, ext) == 0;
}

int geda_bridge_render(const char *filename, const char *outfile) {
    TOPLEVEL *toplevel;
    PAGE *page;
    const GList *iter;
    cairo_surface_t *surface;
    cairo_t *cr;
    EdaRenderer *renderer;
    GArray *colors;
    int l, t, r, b;
    int xmin, ymin, xmax, ymax;
    double s, w, h;
    const double margin = 20.0;
    int is_png = has_ext(outfile, ".png");
    int is_pdf = has_ext(outfile, ".pdf");
    int is_svg = has_ext(outfile, ".svg");

    if (!is_png && !is_pdf && !is_svg) {
        fprintf(stderr, "extensao nao suportada: use .png, .pdf ou .svg\n");
        return 1;
    }

    toplevel = geda_open_page(filename, &page);
    if (!toplevel)
        return 1;

    if (!world_get_object_glist_bounds(toplevel, s_page_objects(page),
                                       &l, &t, &r, &b)) {
        fprintf(stderr, "pagina vazia\n");
        s_toplevel_delete(toplevel);
        return 1;
    }
    xmin = MIN(l, r);  xmax = MAX(l, r);
    ymin = MIN(t, b);  ymax = MAX(t, b);

    /* gEDA: 1000 unidades por polegada. PDF/SVG: 72 pt/pol. PNG: 200 dpi. */
    s = is_png ? 0.2 : 0.072;
    w = (xmax - xmin) * s;
    h = (ymax - ymin) * s;

    if (is_png)
        surface = cairo_image_surface_create(CAIRO_FORMAT_ARGB32,
                                             (int)(w + 2 * margin),
                                             (int)(h + 2 * margin));
    else if (is_pdf)
        surface = cairo_pdf_surface_create(outfile, w + 2 * margin,
                                           h + 2 * margin);
    else
        surface = cairo_svg_surface_create(outfile, w + 2 * margin,
                                           h + 2 * margin);

    cr = cairo_create(surface);

    /* Fundo branco. */
    cairo_set_source_rgb(cr, 1, 1, 1);
    cairo_paint(cr);

    /* Mundo gEDA tem y para cima: inverte y e ajusta a origem. */
    cairo_translate(cr, margin, margin + h);
    cairo_scale(cr, s, -s);
    cairo_translate(cr, -xmin, -ymin);

    renderer = eda_renderer_new(cr, NULL);
    colors = make_color_map();
    eda_renderer_set_color_map(renderer, colors);

    for (iter = s_page_objects(page); iter != NULL; iter = g_list_next(iter))
        eda_renderer_draw(renderer, (OBJECT *)iter->data);

    eda_renderer_destroy(renderer);
    cairo_destroy(cr);

    if (is_png) {
        cairo_status_t st = cairo_surface_write_to_png(surface, outfile);
        if (st != CAIRO_STATUS_SUCCESS)
            fprintf(stderr, "png: %s\n", cairo_status_to_string(st));
    }
    cairo_surface_finish(surface);
    cairo_surface_destroy(surface);

    s_toplevel_delete(toplevel);
    printf("OK: %s\n", outfile);
    return 0;
}
