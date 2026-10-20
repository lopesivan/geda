#include "matplotlibcpp.h"
#include <cmath>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <vector>
#include <string>

namespace plt = matplotlibcpp;

const double PI = 3.14159265358979323846;
const int N_POINTS = 300;

// ============================================================
// ANIMAÇÃO 1: Onda viajante simples
// ============================================================
void animation_traveling_wave(int n_frames = 60)
{
    std::cout << "\n=== Animação 1: Onda Viajante ===" << std::endl;
    plt::backend("Agg");
    system("mkdir -p frames/anim1");

    std::vector<double> x(N_POINTS), y(N_POINTS);

    for(int frame = 0; frame < n_frames; ++frame)
    {
        double phase = 2.0 * PI * frame / n_frames;

        for(int i = 0; i < N_POINTS; ++i)
        {
            x[i] = 4.0 * PI * i / (N_POINTS - 1);
            y[i] = std::sin(x[i] - phase);
        }

        plt::clf();
        plt::plot(x, y, "b-");
        plt::xlim(0.0, 4.0 * PI);
        plt::ylim(-1.5, 1.5);
        plt::grid(true);
        plt::title("Onda Viajante: sin(x - t)");

        std::ostringstream fname;
        fname << "frames/anim1/frame_" << std::setfill('0')
              << std::setw(4) << frame << ".png";
        plt::save(fname.str());

        if(frame % 10 == 0) std::cout << "  Frame " << frame << std::endl;
    }
    std::cout << "✓ Frames salvos em frames/anim1/" << std::endl;
}

// ============================================================
// ANIMAÇÃO 2: Múltiplas frequências (batimento)
// ============================================================
void animation_beating(int n_frames = 60)
{
    std::cout << "\n=== Animação 2: Batimento (f1 + f2) ===" << std::endl;
    plt::backend("Agg");
    system("mkdir -p frames/anim2");

    std::vector<double> x(N_POINTS), y(N_POINTS);
    double f1 = 1.0, f2 = 1.1;  // Frequências ligeiramente diferentes

    for(int frame = 0; frame < n_frames; ++frame)
    {
        double phase = 2.0 * PI * frame / n_frames;

        for(int i = 0; i < N_POINTS; ++i)
        {
            x[i] = 4.0 * PI * i / (N_POINTS - 1);
            y[i] = std::sin(f1 * x[i] - phase) + std::sin(f2 * x[i] - phase);
        }

        plt::clf();
        plt::plot(x, y, "m-");
        plt::xlim(0.0, 4.0 * PI);
        plt::ylim(-2.5, 2.5);
        plt::grid(true);
        plt::title("Batimento: sin(x - t) + sin(1.1x - t)");

        std::ostringstream fname;
        fname << "frames/anim2/frame_" << std::setfill('0')
              << std::setw(4) << frame << ".png";
        plt::save(fname.str());

        if(frame % 10 == 0) std::cout << "  Frame " << frame << std::endl;
    }
    std::cout << "✓ Frames salvos em frames/anim2/" << std::endl;
}

// ============================================================
// ANIMAÇÃO 3: Amplitude crescente
// ============================================================
void animation_growing_amplitude(int n_frames = 60)
{
    std::cout << "\n=== Animação 3: Amplitude Crescente ===" << std::endl;
    plt::backend("Agg");
    system("mkdir -p frames/anim3");

    std::vector<double> x(N_POINTS), y(N_POINTS);

    for(int frame = 0; frame < n_frames; ++frame)
    {
        // Amplitude cresce e decresce
        double amp = 0.5 + 0.5 * std::sin(2.0 * PI * frame / n_frames);

        for(int i = 0; i < N_POINTS; ++i)
        {
            x[i] = 4.0 * PI * i / (N_POINTS - 1);
            y[i] = amp * std::sin(x[i]);
        }

        plt::clf();
        plt::plot(x, y, "r-");
        plt::xlim(0.0, 4.0 * PI);
        plt::ylim(-1.5, 1.5);
        plt::grid(true);
        plt::title("Amplitude Variavel: A(t) * sin(x)");

        std::ostringstream fname;
        fname << "frames/anim3/frame_" << std::setfill('0')
              << std::setw(4) << frame << ".png";
        plt::save(fname.str());

        if(frame % 10 == 0) std::cout << "  Frame " << frame << std::endl;
    }
    std::cout << "✓ Frames salvos em frames/anim3/" << std::endl;
}

// ============================================================
// ANIMAÇÃO 4: Onda estacionária
// ============================================================
void animation_standing_wave(int n_frames = 60)
{
    std::cout << "\n=== Animação 4: Onda Estacionária ===" << std::endl;
    plt::backend("Agg");
    system("mkdir -p frames/anim4");

    std::vector<double> x(N_POINTS), y(N_POINTS);

    for(int frame = 0; frame < n_frames; ++frame)
    {
        double phase = 2.0 * PI * frame / n_frames;

        for(int i = 0; i < N_POINTS; ++i)
        {
            x[i] = 4.0 * PI * i / (N_POINTS - 1);
            // Onda estacionária: produto de sin(x) * cos(t)
            y[i] = std::sin(x[i]) * std::cos(phase);
        }

        plt::clf();
        plt::plot(x, y, "g-");
        plt::xlim(0.0, 4.0 * PI);
        plt::ylim(-1.5, 1.5);
        plt::grid(true);
        plt::title("Onda Estacionaria: sin(x) * cos(t)");

        std::ostringstream fname;
        fname << "frames/anim4/frame_" << std::setfill('0')
              << std::setw(4) << frame << ".png";
        plt::save(fname.str());

        if(frame % 10 == 0) std::cout << "  Frame " << frame << std::endl;
    }
    std::cout << "✓ Frames salvos em frames/anim4/" << std::endl;
}

// ============================================================
// ANIMAÇÃO 5: Envoltória modulada (pacote de ondas)
// ============================================================
void animation_wave_packet(int n_frames = 60)
{
    std::cout << "\n=== Animação 5: Pacote de Ondas ===" << std::endl;
    plt::backend("Agg");
    system("mkdir -p frames/anim5");

    std::vector<double> x(N_POINTS), y(N_POINTS);

    for(int frame = 0; frame < n_frames; ++frame)
    {
        double phase = 2.0 * PI * frame / n_frames;

        for(int i = 0; i < N_POINTS; ++i)
        {
            x[i] = 4.0 * PI * i / (N_POINTS - 1);
            double carrier = std::sin(3.0 * x[i] - phase);
            double envelope = std::exp(-std::pow((x[i] - 2.0*PI) / 3.0, 2));
            y[i] = envelope * carrier;
        }

        plt::clf();
        plt::plot(x, y, "c-");
        plt::xlim(0.0, 4.0 * PI);
        plt::ylim(-1.5, 1.5);
        plt::grid(true);
        plt::title("Pacote de Ondas: exp(-(x-c)^2) * sin(kx - t)");

        std::ostringstream fname;
        fname << "frames/anim5/frame_" << std::setfill('0')
              << std::setw(4) << frame << ".png";
        plt::save(fname.str());

        if(frame % 10 == 0) std::cout << "  Frame " << frame << std::endl;
    }
    std::cout << "✓ Frames salvos em frames/anim5/" << std::endl;
}

// ============================================================
// MAIN
// ============================================================
int main(int argc, char* argv[])
{
    std::cout << "\n╔════════════════════════════════════════════╗" << std::endl;
    std::cout << "║  Gerador de Animações de Ondas Senoidais  ║" << std::endl;
    std::cout << "╚════════════════════════════════════════════╝\n" << std::endl;

    int choice = 0;
    if(argc > 1)
    {
        choice = std::atoi(argv[1]);
    }
    else
    {
        std::cout << "Escolha uma animação:" << std::endl;
        std::cout << "  1 - Onda viajante simples" << std::endl;
        std::cout << "  2 - Batimento (duas frequências)" << std::endl;
        std::cout << "  3 - Amplitude crescente" << std::endl;
        std::cout << "  4 - Onda estacionária" << std::endl;
        std::cout << "  5 - Pacote de ondas" << std::endl;
        std::cout << "  6 - Todas as animações" << std::endl;
        std::cout << "\nOpção: ";
        std::cin >> choice;
    }

    int n_frames = 60;

    switch(choice)
    {
        case 1:
            animation_traveling_wave(n_frames);
            break;
        case 2:
            animation_beating(n_frames);
            break;
        case 3:
            animation_growing_amplitude(n_frames);
            break;
        case 4:
            animation_standing_wave(n_frames);
            break;
        case 5:
            animation_wave_packet(n_frames);
            break;
        case 6:
            animation_traveling_wave(n_frames);
            animation_beating(n_frames);
            animation_growing_amplitude(n_frames);
            animation_standing_wave(n_frames);
            animation_wave_packet(n_frames);
            break;
        default:
            std::cout << "Opção inválida!" << std::endl;
            return 1;
    }

    std::cout << "\n╔════════════════════════════════════════════╗" << std::endl;
    std::cout << "║  Frames gerados com sucesso!               ║" << std::endl;
    std::cout << "╚════════════════════════════════════════════╝\n" << std::endl;

    std::cout << "Para criar vídeos/GIFs, use:" << std::endl;
    std::cout << "\nAnimação 1:" << std::endl;
    std::cout << "  ffmpeg -framerate 30 -i frames/anim1/frame_%04d.png "
                 "-c:v libx264 -pix_fmt yuv420p anim1.mp4" << std::endl;
    std::cout << "\nAnimação 2:" << std::endl;
    std::cout << "  ffmpeg -framerate 30 -i frames/anim2/frame_%04d.png "
                 "-c:v libx264 -pix_fmt yuv420p anim2.mp4" << std::endl;
    std::cout << "\n(e assim por diante...)\n" << std::endl;

    return 0;
}
