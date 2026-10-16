.PHONY: configure build run clean

configure: ## ⚙️  Configura o CMake com o preset default
	PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig \
		cmake --preset default

build: ## 🛠️  Compila o projeto na pasta build
	PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig \
		cmake --build build

# make run                              # app exemplo.sch
# make run ARGS="--sim exemplo.sch"     # netlist + ngspice
# make run ARGS="outro.sch"
# Sem passar pelo Makefile também funciona:
# ARGS="--sim exemplo.sch" cmake --build build --target run
run: ## 🚀 Executa a aplicação (make run ARGS="--sim exemplo.sch")
	ARGS="$(ARGS)" $(MAKE) -C build run

sim:
	PYENV_VERSION=2.7.18 build/app --sim exemplo.sch

svg:
	build/app --render saida.svg  exemplo.sch
png:
	build/app --render saida.png  exemplo.sch
pdf:
	build/app --render saida.pdf  exemplo.sch

clean: ## 🧹 Limpa os arquivos de build
	rm -rf build saida.* exemplo.dat
