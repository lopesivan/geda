#include "matplotlibcpp.h"
#include <cmath>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <vector>

namespace plt = matplotlibcpp;

// Constantes
const double PI = 3.14159265358979323846;
const int    Nf = 100;  // Número de frames
const double r  = 0.5;  // raio da base
const double h  = 0.8;  // altura

// Projeção isométrica 3D -> 2D
struct Point2D
{
    double x, y;
};

Point2D c32(double x3d, double y3d, double z3d)
{
    return {y3d - x3d * std::sin(PI / 4.0) / 2.0,
            z3d - x3d * std::cos(PI / 4.0) / 2.0};
}

// Gera array de ângulos uniformemente espaçados
std::vector<double> linspace(double start, double end, int num)
{
    std::vector<double> result(num);
    double              step = (end - start) / (num - 1);
    for(int i = 0; i < num; ++i)
    {
        result[i] = start + i * step;
    }
    return result;
}

// Estrutura para armazenar configuração do cone
struct ConeSetup
{
    double              t1, t2;
    std::vector<double> theta;
    std::vector<double> theta_plus_pi;
    std::vector<double> cos_theta;
    std::vector<double> sin_theta;
    std::vector<double> cos_theta_pi;
    std::vector<double> sin_theta_pi;
    std::vector<double> rho;
    Point2D             xy;

    ConeSetup() : xy{0.0, 0.05}
    {
        // Ângulos de visibilidade
        t1    = PI - std::atan(2.0 * std::sqrt(2.0));
        t2    = t1 + PI;
        theta = linspace(t1, t2, 100);

        // Pré-calcula valores trigonométricos
        theta_plus_pi.resize(theta.size());
        cos_theta.resize(theta.size());
        sin_theta.resize(theta.size());
        cos_theta_pi.resize(theta.size());
        sin_theta_pi.resize(theta.size());

        for(size_t i = 0; i < theta.size(); ++i)
        {
            theta_plus_pi[i] = theta[i] + PI;
            cos_theta[i]     = std::cos(theta[i]);
            sin_theta[i]     = std::sin(theta[i]);
            cos_theta_pi[i]  = std::cos(theta_plus_pi[i]);
            sin_theta_pi[i]  = std::sin(theta_plus_pi[i]);
        }

        // Array de raios para animação
        rho = linspace(0, r, Nf);
    }
};

// Desenha estrutura estática do cone
void drawStaticStructure(const ConeSetup& setup)
{
    const double xm = 0.8, ym = 0.8, zm = 0.9;

    // Contorno da base (parte visível - tracejada)
    std::vector<double> base_vis_x, base_vis_y;
    for(size_t i = 0; i < setup.theta.size(); ++i)
    {
        Point2D pt =
            c32(r * setup.cos_theta[i], r * setup.sin_theta[i], 0);
        base_vis_x.push_back(setup.xy.x + pt.x);
        base_vis_y.push_back(setup.xy.y + pt.y);
    }

    std::map<std::string, std::string> keywords_vis;
    keywords_vis["linestyle"] = "--";
    keywords_vis["color"]     = "blue";
    keywords_vis["linewidth"] = "1.2";
    keywords_vis["alpha"]     = "0.6";
    plt::plot(base_vis_x, base_vis_y, keywords_vis);

    // Contorno da base (parte oculta - contínua)
    std::vector<double> base_hid_x, base_hid_y;
    for(size_t i = 0; i < setup.theta.size(); ++i)
    {
        Point2D pt = c32(
            -r * setup.cos_theta[i], -r * setup.sin_theta[i], 0);
        base_hid_x.push_back(setup.xy.x + pt.x);
        base_hid_y.push_back(setup.xy.y + pt.y);
    }

    std::map<std::string, std::string> keywords_hid;
    keywords_hid["color"]     = "blue";
    keywords_hid["linewidth"] = "2";
    keywords_hid["alpha"]     = "0.6";
    plt::plot(base_hid_x, base_hid_y, keywords_hid);

    // Arestas laterais
    for(int i = 0; i < 2; ++i)
    {
        double  angle = setup.t1 + PI * i;
        Point2D base_pt =
            c32(r * std::cos(angle), r * std::sin(angle), 0);
        Point2D apex_pt = c32(0, 0, h);

        std::vector<double> edge_x = {setup.xy.x + base_pt.x,
                                      setup.xy.x + apex_pt.x};
        std::vector<double> edge_y = {setup.xy.y + base_pt.y,
                                      setup.xy.y + apex_pt.y};

        std::map<std::string, std::string> edge_kw;
        edge_kw["color"]     = "blue";
        edge_kw["linewidth"] = "1";
        edge_kw["alpha"]     = "0.6";
        plt::plot(edge_x, edge_y, edge_kw);
    }

    // Linha do raio
    Point2D r_end =
        c32(r * std::cos(setup.t1), r * std::sin(setup.t1), 0);
    std::vector<double> r_line_x = {setup.xy.x,
                                    setup.xy.x + r_end.x};
    std::vector<double> r_line_y = {setup.xy.y,
                                    setup.xy.y + r_end.y};

    std::map<std::string, std::string> r_kw;
    r_kw["linestyle"] = "--";
    r_kw["color"]     = "black";
    r_kw["linewidth"] = "1.2";
    plt::plot(r_line_x, r_line_y, r_kw);

    // Label 'r'
    plt::text((setup.xy.x + r_end.x) / 2,
              (setup.xy.y + r_end.y) / 2,
              "$r$");

    // Label 'h'
    plt::text(setup.xy.x - 0.05, setup.xy.y + h / 2, "$h$");
}

// Desenha casca cilíndrica para frame i
void drawShell(const ConeSetup& setup, int i)
{
    double rho_i = setup.rho[i];

    if(rho_i < 1e-6)
        return;  // Evita raio zero

    double z_top = h * (1.0 - rho_i / r);

    // Casca cilíndrica - base
    std::vector<double> shell_x, shell_y;

    // Base (círculo inferior)
    for(size_t j = 0; j < setup.theta_plus_pi.size(); ++j)
    {
        Point2D pt = c32(rho_i * setup.cos_theta_pi[j],
                         rho_i * setup.sin_theta_pi[j],
                         0);
        shell_x.push_back(setup.xy.x + pt.x);
        shell_y.push_back(setup.xy.y + pt.y);
    }

    // Topo (círculo superior) - ordem reversa
    for(int j = setup.theta_plus_pi.size() - 1; j >= 0; --j)
    {
        Point2D pt = c32(rho_i * setup.cos_theta_pi[j],
                         rho_i * setup.sin_theta_pi[j],
                         z_top);
        shell_x.push_back(setup.xy.x + pt.x);
        shell_y.push_back(setup.xy.y + pt.y);
    }

    // Fecha o polígono
    shell_x.push_back(shell_x[0]);
    shell_y.push_back(shell_y[0]);

    // Desenha a casca preenchida
    std::map<std::string, std::string> shell_kw;
    shell_kw["color"] = "orange";
    shell_kw["alpha"] = "0.6";
    plt::fill(shell_x, shell_y, shell_kw);

    // Círculo superior (tracejado)
    std::vector<double> top_x, top_y;
    for(size_t j = 0; j < setup.theta.size(); ++j)
    {
        Point2D pt = c32(rho_i * setup.cos_theta[j],
                         rho_i * setup.sin_theta[j],
                         z_top);
        top_x.push_back(setup.xy.x + pt.x);
        top_y.push_back(setup.xy.y + pt.y);
    }

    std::map<std::string, std::string> top_kw;
    top_kw["linestyle"] = "--";
    top_kw["color"]     = "orange";
    top_kw["linewidth"] = "1.2";
    plt::plot(top_x, top_y, top_kw);

    // Volume acumulado (cone interno)
    std::vector<double> vol_x, vol_y;

    for(size_t j = 0; j < setup.theta_plus_pi.size(); ++j)
    {
        Point2D pt = c32(rho_i * setup.cos_theta_pi[j],
                         rho_i * setup.sin_theta_pi[j],
                         z_top);
        vol_x.push_back(setup.xy.x + pt.x);
        vol_y.push_back(setup.xy.y + pt.y);
    }

    // Vértice do cone
    Point2D apex = c32(0, 0, h);
    vol_x.push_back(setup.xy.x + apex.x);
    vol_y.push_back(setup.xy.y + apex.y);

    // Fecha
    vol_x.push_back(vol_x[0]);
    vol_y.push_back(vol_y[0]);

    std::map<std::string, std::string> vol_kw;
    vol_kw["color"] = "lightblue";
    vol_kw["alpha"] = "0.7";
    plt::fill(vol_x, vol_y, vol_kw);
}

int main()
{
    std::cout
        << "Gerando animação do cone com cascas cilíndricas..."
        << std::endl;

    ConeSetup setup;

    // Cria diretório para frames
    system("mkdir -p frames");

    // Gera cada frame
    for(int i = 0; i < Nf; ++i)
    {
        if(i % 10 == 0)
        {
            std::cout << "Frame " << i << "/" << Nf << std::endl;
        }

        plt::clf();  // Limpa figura

        // Configurações da figura
        plt::xlim(-0.9, 0.9);
        plt::ylim(-0.35, 1.15);
        plt::axis("off");

        // Título
        plt::title("Método das Cascas Cilíndricas");

        // Desenha estrutura estática
        drawStaticStructure(setup);

        // Desenha casca animada
        drawShell(setup, i);

        // Fórmulas matemáticas (usando anotações)
        plt::text(0.0,
                  -0.25,
                  "$dV = 2\\pi\\rho \\cdot "
                  "h\\left(1-\\frac{\\rho}{r}\\right) d\\rho$");
        plt::text(0.0,
                  -0.35,
                  "$V = \\int_0^r 2\\pi\\rho\\left(h - "
                  "\\frac{h}{r}\\rho\\right) "
                  "d\\rho = \\frac{1}{3}\\pi r^2 h$");

        // Salva frame
        std::ostringstream filename;
        filename << "frames/frame_" << std::setfill('0')
                 << std::setw(4) << i << ".png";
        plt::save(filename.str());
    }

    std::cout << "\n✓ Frames gerados em ./frames/" << std::endl;
    std::cout << "\nPara criar vídeo, execute:" << std::endl;
    std::cout << "ffmpeg -framerate 30 -i frames/frame_%04d.png "
                 "-c:v libx264 "
                 "-pix_fmt yuv420p volume_cone.mp4"
              << std::endl;

    return 0;
}

/*
COMPILAÇÃO E EXECUÇÃO:
======================

1. Instalar matplotlib-cpp:
   git clone https://github.com/lava/matplotlib-cpp.git
   sudo apt install python3-matplotlib python3-numpy python3-dev

2. Compilar:
   g++ -std=c++17 -O3 volume_cone.cpp -o volume_cone \
       -I/usr/include/python3.10 \
       -lpython3.10 \
       -I./matplotlib-cpp

3. Executar:
   ./volume_cone

4. Gerar vídeo:
   ffmpeg -framerate 30 -i frames/frame_%04d.png \
          -c:v libx264 -pix_fmt yuv420p volume_cone.mp4

VANTAGENS:
- 10-20x mais rápido que Python puro
- Código C++ nativo
- Mesma qualidade visual

DESVANTAGENS:
- matplotlib-cpp chama Python por baixo (não é 100% nativo)
- Precisa Python instalado
- API mais verbosa que Python
*/
