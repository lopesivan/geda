#!/usr/bin/env python3
"""
Reorganiza arquivos .tex em subpastas de mesmo nome e gera um Makefile
em cada subpasta.

Antes:  ./Thermodynamics/Otto-Cycle.tex
Depois: ./Thermodynamics/Otto-Cycle/Otto-Cycle.tex
        ./Thermodynamics/Otto-Cycle/Makefile
"""

import os
import glob
import shutil

# Conteúdo do Makefile gerado em cada subpasta.
# {base} é substituído pelo nome do .tex (sem extensão).
MAKEFILE_TEMPLATE = """\
# Makefile - Gera PDF, PNG, SVG e EPS a partir do arquivo .tex
# Uso: make          -> gera todos os formatos
#      make pdf      -> apenas PDF
#      make png      -> apenas PNG
#      make svg      -> apenas SVG
#      make eps      -> apenas EPS
#      make clean    -> remove arquivos gerados

TEX      = {base}.tex
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
\t$(LATEX) $(LATEXOPT) $(TEX)
\t$(LATEX) $(LATEXOPT) $(TEX)

png: $(BASE).png

$(BASE).png: $(BASE).pdf
\t$(PDFTOCAIRO) -png -r 300 -singlefile $(BASE).pdf $(BASE)

svg: $(BASE).svg

$(BASE).svg: $(BASE).pdf
\t$(PDFTOSVG) $(BASE).pdf $(BASE).svg

eps: $(BASE).eps

$(BASE).eps: $(BASE).pdf
\t$(PDFTOEPS) $(BASE).pdf $(BASE).eps

clean:
\trm -f $(BASE).aux $(BASE).log $(BASE).out
\trm -f $(BASE)-autopp.* $(BASE)-pics.pdf
\trm -f $(BASE).pdf $(BASE).png $(BASE).svg $(BASE).eps

distclean: clean
\trm -f $(BASE).fls $(BASE).fdb_latexmk $(BASE).synctex.gz

show: $(BASE).png
\teog $(BASE).png

help:
\t@echo "Alvos: all pdf png svg eps clean distclean show help"
"""


def reorganizar(tex_path):
    """Move tex_path para <dir>/<nome>/<nome>.tex e cria Makefile."""
    pasta_origem = os.path.dirname(tex_path)
    nome = os.path.splitext(os.path.basename(tex_path))[0]

    # Se já está dentro de uma pasta com o próprio nome, não faz nada
    if os.path.basename(pasta_origem) == nome:
        print(f"[skip] {tex_path} (já organizado)")
        return

    pasta_destino = os.path.join(pasta_origem, nome)
    destino_tex   = os.path.join(pasta_destino, f"{nome}.tex")
    destino_mk    = os.path.join(pasta_destino, "Makefile")

    if os.path.exists(destino_tex):
        print(f"[skip] {destino_tex} já existe")
        return

    os.makedirs(pasta_destino, exist_ok=True)
    shutil.move(tex_path, destino_tex)
    print(f"[move] {tex_path} -> {destino_tex}")

    with open(destino_mk, "w", encoding="utf-8") as f:
        f.write(MAKEFILE_TEMPLATE.format(base=nome))
    print(f"[make] {destino_mk}")


def main():
    texs = sorted(glob.glob("**/*.tex", recursive=True))
    if not texs:
        print("Nenhum .tex encontrado.")
        return
    for t in texs:
        reorganizar(t)


if __name__ == "__main__":
    main()
