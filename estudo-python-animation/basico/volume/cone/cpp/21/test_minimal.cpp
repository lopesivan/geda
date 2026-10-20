#include "matplotlibcpp.h"
#include <iostream>
#include <vector>

namespace plt = matplotlibcpp;

int main() {
    std::cout << "Teste 1: Configurando backend..." << std::endl;
    try {
        plt::backend("Agg");
        std::cout << "✓ Backend configurado" << std::endl;
    } catch(const std::exception& e) {
        std::cerr << "✗ Erro no backend: " << e.what() << std::endl;
        return 1;
    }

    std::cout << "\nTeste 2: Criando plot simples..." << std::endl;
    try {
        std::vector<double> x = {1, 2, 3, 4};
        std::vector<double> y = {1, 4, 9, 16};
        plt::plot(x, y);
        std::cout << "✓ Plot criado" << std::endl;
    } catch(const std::exception& e) {
        std::cerr << "✗ Erro no plot: " << e.what() << std::endl;
        return 1;
    }

    std::cout << "\nTeste 3: Salvando imagem..." << std::endl;
    try {
        plt::save("test.png");
        std::cout << "✓ Imagem salva: test.png" << std::endl;
    } catch(const std::exception& e) {
        std::cerr << "✗ Erro ao salvar: " << e.what() << std::endl;
        
        // Tenta obter mais informações
        std::cout << "\nTentando diagnosticar..." << std::endl;
        std::cout << "Verificando se o diretório tem permissão de escrita..." << std::endl;
        
        return 1;
    }

    std::cout << "\n✓✓✓ Todos os testes passaram!" << std::endl;
    return 0;
}
