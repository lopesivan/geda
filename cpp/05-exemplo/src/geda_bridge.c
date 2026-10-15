#include <string.h>
#include <cairo.h>
#include <cairo-pdf.h>
#include <cairo-svg.h>

static int has_ext(const char *name, const char *ext) {
    size_t n = strlen(name), e = strlen(ext);
    return n >= e && g_ascii_strcasecmp(name + n - e, ext) == 0;
}

int geda_bridge_render(const char *filename, const char *outfile) {
    static int inited = 0;
    TOPLEVEL *toplevel;
    PAGE *page;
    GError *err = NULL;
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

    /* CONFIRMAR: assinatura de world_get_object_glist_bounds */
    if (!world_get_object_glist_bounds(toplevel, s_page_objects(page),
                                       &l, &t, &r, &b)) {
        fprintf(stderr, "pagina vazia\n");
        s_toplevel_delete(toplevel);
        return 1;
    }
    xmin = MIN(l, r);  xmax = MAX(l, r);
    ymin = MIN(t, b);  ymax = MAX(t, b);

    /* Unidades do gEDA: 1000 por polegada.
       PDF/SVG: 72 pt por polegada. PNG: 200 dpi. */
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

    /* Fundo branco */
    cairo_set_source_rgb(cr, 1, 1, 1);
    cairo_paint(cr);

    /* Mundo gEDA: y para cima. Inverte y e ajusta a origem. */
    cairo_translate(cr, margin, margin + h);
    cairo_scale(cr, s, -s);
    cairo_translate(cr, -xmin, -ymin);

    renderer = eda_renderer_new(cr, NULL);

    /* CONFIRMAR: criacao do mapa de cores (veja o grep abaixo).
       Para fundo branco, o ideal e o mapa "light"/"bw". */
    colors = g_array_new(FALSE, FALSE, sizeof(COLOR));
    s_color_map_defaults(colors);
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
