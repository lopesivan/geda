.PHONY: configure build run clean

configure: ## ⚙️  Configura o CMake com o preset default
	PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig \
		cmake --preset default

build: ## 🛠️  Compila o projeto na pasta build
	PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig \
		cmake --build build

run: ## 🚀 Executa a aplicação (make run ARGS="--sim exemplo.sch")
	$(MAKE) -C build run

clean: ## 🧹 Limpa os arquivos de build
	rm -rf build


NAME    := exemplo
SCHEM   := $(NAME).sch
NETLIST := $(NAME).sp
DATA    := $(NAME).dat
RAW     := $(NAME).raw
PDF     := $(NAME).pdf
PLOT    := plot.py
PYTHON  := PYENV_VERSION=jupyter python3
GSCHEM  := /opt/geda/bin/gschem
NGSPICE := /home/linuxbrew/.linuxbrew/Cellar/ivan/ngspice/bin/ngspice

schem:
	$(GSCHEM) -r gschemrc $(SCHEM)
