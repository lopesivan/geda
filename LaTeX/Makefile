# Makefile — geração da galeria de imagens main.png

PYTHON ?= python3
BROWSER ?= xdg-open

.PHONY: all galeria show png clean help

# Alvo padrão: gera a galeria e abre no navegador
all: png galeria show

# Gera galeria.html a partir dos */main.png
galeria:
	$(PYTHON) ./galeria.py

# Abre a galeria no navegador
show:
	$(BROWSER) galeria.html

# Executa `make png` em cada subpasta que tenha um Makefile
png:
	./png.sh

# Remove artefatos gerados
clean:
	rm -f galeria.html
	./clean.sh

# Ajuda
help:
	@echo "Alvos disponíveis:"
	@echo "  all      -> galeria + show (padrão)"
	@echo "  galeria  -> gera galeria.html"
	@echo "  show     -> abre galeria.html no navegador"
	@echo "  png      -> executa 'make png' em cada */Makefile"
	@echo "  clean    -> remove galeria.html"
	@echo "  help     -> mostra esta ajuda"
	@echo ""
	@echo "Variáveis:"
	@echo "  PYTHON   (padrão: python3)"
	@echo "  BROWSER  (padrão: xdg-open)"
