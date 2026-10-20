#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>

const double PI = 3.14159265358979323846;
const int Nf = 100;
const double r = 0.5;
const double h = 0.8;

void generatePythonScript(int frame_num, double rho_val) {
  std::ostringstream script;

  script << "import matplotlib\n";
  script << "matplotlib.use('Agg')\n";
  script << "import matplotlib.pyplot as plt\n";
  script << "import numpy as np\n\n";

  script << "def c32(x, y, z):\n";
  script << "    return np.array([y - x * np.sin(np.pi/4) / 2, z - x * "
            "np.cos(np.pi/4) / 2])\n\n";

  script << "r = " << r << "\n";
  script << "h = " << h << "\n";
  script << "rho = " << rho_val << "\n";
  script << "xy = np.array([0.0, 0.05])\n\n";

  script << "t1 = np.pi - np.arctan(2*np.sqrt(2))\n";
  script << "t2 = t1 + np.pi\n";
  script << "theta = np.linspace(t1, t2, 100)\n";
  script << "theta_pi = theta + np.pi\n\n";

  script << "fig, ax = plt.subplots(figsize=(9, 9))\n";
  script << "ax.set_xlim(-0.9, 0.9)\n";
  script << "ax.set_ylim(-0.35, 1.15)\n";
  script << "ax.axis('off')\n\n";

  // Base visível (tracejada)
  script << "base_vis = c32(r*np.cos(theta), r*np.sin(theta), "
            "np.zeros_like(theta))\n";
  script << "ax.plot(xy[0] + base_vis[0], xy[1] + base_vis[1], '--', c='blue', "
            "lw=1.2, alpha=0.6)\n\n";

  // Base oculta
  script << "base_hid = c32(-r*np.cos(theta), -r*np.sin(theta), "
            "np.zeros_like(theta))\n";
  script << "ax.plot(xy[0] + base_hid[0], xy[1] + base_hid[1], '-', c='blue', "
            "lw=2, alpha=0.6)\n\n";

  // Arestas
  script << "for i in range(2):\n";
  script << "    angle = t1 + np.pi * i\n";
  script << "    base_pt = xy + c32(r*np.cos(angle), r*np.sin(angle), 0)\n";
  script << "    apex_pt = xy + c32(0, 0, h)\n";
  script << "    ax.plot([base_pt[0], apex_pt[0]], [base_pt[1], apex_pt[1]], "
            "c='blue', lw=1, alpha=0.6)\n\n";

  // Casca e volume (se rho > 0)
  if (rho_val > 1e-6) {
    script << "if rho > 1e-6:\n";
    script << "    z_top = h * (1 - rho / r)\n\n";

    // Casca cilíndrica
    script << "    shell_base = c32(rho*np.cos(theta_pi), "
              "rho*np.sin(theta_pi), np.zeros_like(theta_pi))\n";
    script << "    shell_top = c32(rho*np.cos(theta_pi[::-1]), "
              "rho*np.sin(theta_pi[::-1]), np.full_like(theta_pi, z_top))\n";
    script << "    shell_x = np.concatenate([xy[0] + shell_base[0], xy[0] + "
              "shell_top[0]])\n";
    script << "    shell_y = np.concatenate([xy[1] + shell_base[1], xy[1] + "
              "shell_top[1]])\n";
    script << "    ax.fill(shell_x, shell_y, color='orange', alpha=0.6, "
              "zorder=1)\n\n";

    // Círculo superior
    script << "    top_circle = c32(rho*np.cos(theta), rho*np.sin(theta), "
              "np.full_like(theta, z_top))\n";
    script << "    ax.plot(xy[0] + top_circle[0], xy[1] + top_circle[1], '--', "
              "c='orange', lw=1.2, zorder=-2)\n\n";

    // Volume acumulado
    script << "    apex = xy + c32(0, 0, h)\n";
    script << "    vol_x = np.append(xy[0] + shell_top[0], apex[0])\n";
    script << "    vol_y = np.append(xy[1] + shell_top[1], apex[1])\n";
    script << "    ax.fill(vol_x, vol_y, color='lightblue', alpha=0.7, "
              "zorder=1)\n\n";
  }

  script << "plt.savefig('frames/frame_" << std::setfill('0') << std::setw(4)
         << frame_num << ".png', dpi=200, bbox_inches='tight')\n";
  script << "plt.close()\n";

  // Salva script temporário
  std::ofstream outfile("temp_plot.py");
  outfile << script.str();
  outfile.close();
}

int main() {
  std::cout << "Gerando frames do cone usando Python..." << std::endl;

  system("mkdir -p frames");

  for (int i = 0; i < Nf; ++i) {
    if (i % 10 == 0) {
      std::cout << "Frame " << i << "/" << Nf << std::endl;
    }

    double rho_val = r * i / (Nf - 1.0);
    generatePythonScript(i, rho_val);

    // Executa script Python
    int ret = system("PYENV_VERSION=jupyter python temp_plot.py");
    if (ret != 0) {
      std::cerr << "Erro ao gerar frame " << i << std::endl;
      return 1;
    }
  }

  system("rm -f temp_plot.py");

  std::cout << "\n✓ Frames gerados em ./frames/" << std::endl;
  std::cout << "\nPara criar vídeo:" << std::endl;
  std::cout << "ffmpeg -framerate 30 -i frames/frame_%04d.png -c:v libx264 "
               "-pix_fmt yuv420p cone.mp4"
            << std::endl;

  return 0;
}
