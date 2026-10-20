#include "matplotlibcpp.h"
#include <cmath>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <vector>

namespace plt = matplotlibcpp;

const double PI = 3.14159265358979323846;
const int    Nf = 100;  // Número de frames
const double r  = 0.5;  // raio da base
const double h  = 0.8;  // altura

struct Point2D {
    double x, y;
};

// Projeção isométrica 3D -> 2D
Point2D c32(double x3d, double y3d, double z3d) {
    return {y3d - x3d * std::sin(PI / 4.0) / 2.0,
            z3d - x3d * std::cos(PI / 4.0) / 2.0};
}

std::vector<double> linspace(double start, double end, int num) {
    std::vector<double> result(num);
    double step = (end - start) / (num - 1);
    for(int i = 0; i < num; ++i) {
        result[i] = start + i * step;
    }
    return result;
}

struct ConeSetup {
    double t1, t2;
    std::vector<double> theta;
    std::vector<double> theta_plus_pi;
    std::vector<double> cos_theta;
    std::vector<double> sin_theta;
    std::vector<double> cos_theta_pi;
    std::vector<double> sin_theta_pi;
    std::vector<double> rho;
    Point2D xy;

    ConeSetup() : xy{0.0, 0.05} {
        t1 = PI - std::atan(2.0 * std::sqrt(2.0));
        t2 = t1 + PI;
        theta = linspace(t1, t2, 100);

        theta_plus_pi.resize(theta.size());
        cos_theta.resize(theta.size());
        sin_theta.resize(theta.size());
        cos_theta_pi.resize(theta.size());
        sin_theta_pi.resize(theta.size());

        for(size_t i = 0; i < theta.size(); ++i) {
            theta_plus_pi[i] = theta[i] + PI;
            cos_theta[i] = std::cos(theta[i]);
            sin_theta[i] = std::sin(theta[i]);
            cos_theta_pi[i] = std::cos(theta_plus_pi[i]);
            sin_theta_pi[i] = std::sin(theta_plus_pi[i]);
        }

        rho = linspace(0, r, Nf);
    }
};

void drawStaticStructure(const ConeSetup& setup) {
    // Contorno da base (parte visível - tracejada)
    std::vector<double> base_vis_x, base_vis_y;
    for(size_t i = 0; i < setup.theta.size(); ++i) {
        Point2D pt = c32(r * setup.cos_theta[i], r * setup.sin_theta[i], 0);
        base_vis_x.push_back(setup.xy.x + pt.x);
        base_vis_y.push_back(setup.xy.y + pt.y);
    }

    std::map<std::string, std::string> kw_vis;
    kw_vis["linestyle"] = "--";
    kw_vis["color"] = "blue";
    kw_vis["linewidth"] = "1.2";
    kw_vis["alpha"] = "0.6";
    plt::plot(base_vis_x, base_vis_y, kw_vis);

    // Contorno da base (parte oculta - contínua)
    std::vector<double> base_hid_x, base_hid_y;
    for(size_t i = 0; i < setup.theta.size(); ++i) {
        Point2D pt = c32(-r * setup.cos_theta[i], -r * setup.sin_theta[i], 0);
        base_hid_x.push_back(setup.xy.x + pt.x);
        base_hid_y.push_back(setup.xy.y + pt.y);
    }

    std::map<std::string, std::string> kw_hid;
    kw_hid["color"] = "blue";
    kw_hid["linewidth"] = "2";
    kw_hid["alpha"] = "0.6";
    plt::plot(base_hid_x, base_hid_y, kw_hid);

    // Arestas laterais
    for(int i = 0; i < 2; ++i) {
        double angle = setup.t1 + PI * i;
        Point2D base_pt = c32(r * std::cos(angle), r * std::sin(angle), 0);
        Point2D apex_pt = c32(0, 0, h);

        std::vector<double> edge_x = {setup.xy.x + base_pt.x, setup.xy.x + apex_pt.x};
        std::vector<double> edge_y = {setup.xy.y + base_pt.y, setup.xy.y + apex_pt.y};

        std::map<std::string, std::string> kw_edge;
        kw_edge["color"] = "blue";
        kw_edge["linewidth"] = "1";
        kw_edge["alpha"] = "0.6";
        plt::plot(edge_x, edge_y, kw_edge);
    }
}

void drawShell(const ConeSetup& setup, int i) {
    double rho_i = setup.rho[i];
    if(rho_i < 1e-6) return;

    double z_top = h * (1.0 - rho_i / r);

    // Casca cilíndrica
    std::vector<double> shell_x, shell_y;

    // Base (círculo inferior)
    for(size_t j = 0; j < setup.theta_plus_pi.size(); ++j) {
        Point2D pt = c32(rho_i * setup.cos_theta_pi[j],
                         rho_i * setup.sin_theta_pi[j], 0);
        shell_x.push_back(setup.xy.x + pt.x);
        shell_y.push_back(setup.xy.y + pt.y);
    }

    // Topo (círculo superior) - ordem reversa
    for(int j = setup.theta_plus_pi.size() - 1; j >= 0; --j) {
        Point2D pt = c32(rho_i * setup.cos_theta_pi[j],
                         rho_i * setup.sin_theta_pi[j], z_top);
        shell_x.push_back(setup.xy.x + pt.x);
        shell_y.push_back(setup.xy.y + pt.y);
    }

    shell_x.push_back(shell_x[0]);
    shell_y.push_back(shell_y[0]);

    // Desenha casca preenchida
    std::map<std::string, std::string> kw_shell;
    kw_shell["color"] = "orange";
    kw_shell["alpha"] = "0.6";
    plt::fill(shell_x, shell_y, kw_shell);

    // Círculo superior (tracejado)
    std::vector<double> top_x, top_y;
    for(size_t j = 0; j < setup.theta.size(); ++j) {
        Point2D pt = c32(rho_i * setup.cos_theta[j],
                         rho_i * setup.sin_theta[j], z_top);
        top_x.push_back(setup.xy.x + pt.x);
        top_y.push_back(setup.xy.y + pt.y);
    }

    std::map<std::string, std::string> kw_top;
    kw_top["linestyle"] = "--";
    kw_top["color"] = "orange";
    kw_top["linewidth"] = "1.2";
    plt::plot(top_x, top_y, kw_top);

    // Volume acumulado (cone interno)
    std::vector<double> vol_x, vol_y;

    for(size_t j = 0; j < setup.theta_plus_pi.size(); ++j) {
        Point2D pt = c32(rho_i * setup.cos_theta_pi[j],
                         rho_i * setup.sin_theta_pi[j], z_top);
        vol_x.push_back(setup.xy.x + pt.x);
        vol_y.push_back(setup.xy.y + pt.y);
    }

    Point2D apex = c32(0, 0, h);
    vol_x.push_back(setup.xy.x + apex.x);
    vol_y.push_back(setup.xy.y + apex.y);
    vol_x.push_back(vol_x[0]);
    vol_y.push_back(vol_y[0]);

    std::map<std::string, std::string> kw_vol;
    kw_vol["color"] = "lightblue";
    kw_vol["alpha"] = "0.7";
    plt::fill(vol_x, vol_y, kw_vol);
}

int main() {
    std::cout << "Gerando frames do cone..." << std::endl;

    // Configura backend não-interativo
    plt::backend("Agg");

    ConeSetup setup;
    system("mkdir -p frames");

    for(int i = 0; i < Nf; ++i) {
        if(i % 10 == 0) {
            std::cout << "Frame " << i << "/" << Nf << std::endl;
        }

        plt::clf();
        plt::xlim(-0.9, 0.9);
        plt::ylim(-0.35, 1.15);
        plt::axis("off");

        drawStaticStructure(setup);
        drawShell(setup, i);

        std::ostringstream filename;
        filename << "frames/frame_" << std::setfill('0')
                 << std::setw(4) << i << ".png";
        plt::save(filename.str());
    }

    std::cout << "\n✓ Frames gerados em ./frames/" << std::endl;
    std::cout << "\nPara criar video:" << std::endl;
    std::cout << "ffmpeg -framerate 30 -i frames/frame_%04d.png "
                 "-c:v libx264 -pix_fmt yuv420p cone.mp4" << std::endl;

    return 0;
}
