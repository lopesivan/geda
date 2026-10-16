# =====================================================================
#  Makefile — build, simulação e renderização do projeto
# =====================================================================
#  Estrutura geral:
#    - configure / build : compilam o projeto via CMake
#    - schem / sim       : abrem o esquemático e rodam a simulação
#    - svg / png / pdf   : renderizam a saída em diferentes formatos
#    - analise           : roda a análise via script Lua
#    - deploy            : atalho para configure + build + render
#    - run               : executa o binário final
#    - clean             : limpa artefatos gerados
# =====================================================================

.PHONY: configure build run clean

# ---------------------------------------------------------------------
# ⚙️  configure — Configura o projeto com o preset "default" do CMake
# ---------------------------------------------------------------------
configure: ## ⚙️  Configura o CMake com o preset default
	PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig \
		cmake --preset default

# ---------------------------------------------------------------------
# 🛠️  build — Compila o projeto na pasta ./build
# ---------------------------------------------------------------------
build: ## 🛠️  Compila o projeto na pasta build
	PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig \
		cmake --build build

# =====================================================================
#  Variáveis de configuração do projeto
# =====================================================================
NAME       := exemplo
SCHEM      := $(NAME).sch
NETLIST    := $(NAME).sp
DATA       := $(NAME).dat
RAW        := $(NAME).raw
PDF        := $(NAME).pdf
LUA_SCRIPT := analise.lua
PLOT       := plot.py
PYTHON     := PYENV_VERSION=jupyter python3
GSCHEM     := /opt/geda/bin/gschem
NGSPICE    := /home/linuxbrew/.linuxbrew/Cellar/ivan/ngspice/bin/ngspice
SVG        := saida.svg
PNG        := saida.png
PDF        := saida.pdf

# ---------------------------------------------------------------------
# 📐 schem — Abre o esquemático no gschem
# ---------------------------------------------------------------------
schem:
	$(GSCHEM) -r gschemrc $(SCHEM)

# ---------------------------------------------------------------------
# 🚀 deploy — Pipeline completo: configura, compila e renderiza tudo
# ---------------------------------------------------------------------
deploy: configure build svg png pdf

# ---------------------------------------------------------------------
# ▶️  sim — Executa a simulação a partir do esquemático
# ---------------------------------------------------------------------
sim:
	PYENV_VERSION=2.7.18 build/app --sim $(SCHEM)

# ---------------------------------------------------------------------
# 🖼️  svg — Renderiza a saída em SVG
# ---------------------------------------------------------------------
svg:
	build/app --render $(SVG) $(SCHEM)

# ---------------------------------------------------------------------
# 🖼️  png — Renderiza a saída em PNG
# ---------------------------------------------------------------------
png:
	build/app --render $(PNG) $(SCHEM)

# ---------------------------------------------------------------------
# 📄 pdf — Renderiza a saída em PDF
# ---------------------------------------------------------------------
pdf:
	build/app --render $(PDF) $(SCHEM)

# ---------------------------------------------------------------------
# 🔬 analise — Roda a análise via script Lua (ambiente Python 2.7)
# ---------------------------------------------------------------------
analise:
	PYENV_VERSION=2.7.18 ./build/app --analyze $(SCHEM) $(LUA_SCRIPT)

# ---------------------------------------------------------------------
# 🧹 clean — Remove a pasta de build e arquivos temporários
# ---------------------------------------------------------------------
clean: ## 🧹 Limpa os arquivos de build
	rm -rf build
	rm saida.* $(SCHEM)~

# ---------------------------------------------------------------------
# 🌙 Luaenv — detecta o prefixo da instalação Lua 5.4.6
# ---------------------------------------------------------------------
LUAENV := $(shell luaenv prefix 5.4.6)

# ---------------------------------------------------------------------
# ▶️  run — Executa o binário, apontando para as libs do Luaenv
# ---------------------------------------------------------------------
run:
	LD_LIBRARY_PATH=$(LUAENV)/lib ./build/app $(SCHEM)

# eof
