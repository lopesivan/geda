# Makefile - Gera PDF, PNG, SVG e EPS a partir do arquivo .tex
# Uso: make          -> gera todos os formatos
#      make pdf      -> apenas PDF
#      make png      -> apenas PNG
#      make svg      -> apenas SVG
#      make eps      -> apenas EPS
#      make clean    -> remove arquivos gerados

TEX      = exemplo-01-aa78eeee90.tex
BASE     = $(basename $(TEX))
LATEX    = pdflatex
LATEXOPT = -interaction=nonstopmode -halt-on-error -shell-escape

# Permite operações de transparência no Ghostscript (PSTricks/opacity)
export GS_OPTIONS = -dALLOWPSTRANSPARENCY

# Ferramentas externas (poppler-utils, librsvg)
PDFTOCAIRO = pdftocairo
PDFTOSVG   = pdftocairo -svg
PDFTOEPS   = pdftops

.PHONY: all pdf png svg eps clean distclean show help

all: pdf png svg eps

pdf: $(BASE).pdf

$(BASE).pdf: $(TEX)
	$(LATEX) $(LATEXOPT) $(TEX)
	$(LATEX) $(LATEXOPT) $(TEX)

png: $(BASE).png

$(BASE).png: $(BASE).pdf
	$(PDFTOCAIRO) -png -r 300 -singlefile $(BASE).pdf $(BASE)

svg: $(BASE).svg

$(BASE).svg: $(BASE).pdf
	$(PDFTOSVG) $(BASE).pdf $(BASE).svg

eps: $(BASE).eps

$(BASE).eps: $(BASE).pdf
	$(PDFTOEPS) $(BASE).pdf $(BASE).eps

clean:
	rm -f $(BASE).aux $(BASE).log $(BASE).out
	rm -f $(BASE)-autopp.* $(BASE)-pics.pdf
	rm -f $(BASE).pdf $(BASE).png $(BASE).svg $(BASE).eps

distclean: clean
	rm -f $(BASE).fls $(BASE).fdb_latexmk $(BASE).synctex.gz

show: $(BASE).png
	eog $(BASE).png

help:
	@echo "Alvos: all pdf png svg eps clean distclean show help"
