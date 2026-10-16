.PHONY: configure build run clean

configure: ## ⚙️  Configura o CMake com o preset default
	PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig \
		cmake --preset default

build: ## 🛠️  Compila o projeto na pasta build
	PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig \
		cmake --build build

SCHEM   := ../exemplo.sch
NETLIST := exemplo.sp
DATA    := exemplo.dat

SVG     := saida.svg
PNG     := saida.png
PDF     := saida.pdf

deploy: configure build svg png pdf

sim:
	build/app --sim $(SCHEM)

svg:
	build/app --render $(SVG) $(SCHEM)

png:
	build/app --render $(PNG) $(SCHEM)

pdf:
	build/app --render $(PDF) $(SCHEM)

clean: ## 🧹 Limpa os arquivos de build
	rm -rf build ../$(SVG) ../$(PNG) ../$(PDF)

