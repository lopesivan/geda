.PHONY: configure build run clean

configure: ## ⚙️  Configura o CMake com o preset default
	cmake --preset default

build: ## 🛠️  Compila o projeto na pasta build
	cmake --build build

run: ## 🚀 Executa a aplicação
	$(MAKE) -C build run

clean: ## 🧹 Limpa os arquivos de build
	rm -rf build
