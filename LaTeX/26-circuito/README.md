# Makefile para compilar o diagrama Circuitikz

```makefile
# Makefile - Gera PDF, PNG, SVG e EPS a partir do arquivo .tex
# Uso: make          -> gera todos os formatos
#      make pdf      -> apenas PDF
#      make png      -> apenas PNG
#      make svg      -> apenas SVG
#      make eps      -> apenas EPS
#      make clean    -> remove arquivos gerados

TEX      = diagrama.tex
BASE     = $(basename $(TEX))
LATEX    = pdflatex
LATEXOPT = -interaction=nonstopmode -halt-on-error

# Ferramentas externas (poppler-utils, librsvg)
PDFTOCAIRO = pdftocairo
PDFTOSVG   = pdftocairo -svg
PDFTOEPS   = pdftops

.PHONY: all pdf png svg eps clean

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
	rm -f $(BASE).pdf $(BASE).png $(BASE).svg $(BASE).eps

distclean: clean
	rm -f $(BASE).fls $(BASE).fdb_latexmk $(BASE).synctex.gz
```

## Como usar

1. Salve o código do seu diagrama em um arquivo chamado
`diagrama.tex` (ou ajuste a variável `TEX` no Makefile).
2. Rode:

```bash
make          # gera todos os formatos
make pdf      # apenas PDF
make png      # apenas PNG (300 dpi)
make svg      # apenas SVG
make eps      # apenas EPS
make clean    # limpa tudo
```

## Dependências necessárias

No **Linux (Debian/Ubuntu)**:

```bash
sudo apt install texlive-latex-base texlive-pictures texlive-science \
                 poppler-utils
```

No **macOS (Homebrew)**:

```bash
brew install --cask mactex
brew install poppler
```

No **Windows**: use WSL ou instale MiKTeX + poppler, e execute `make` via Git Bash.

## Observações

- O documento usa a classe `standalone`, que já corta a
saída exatamente no tamanho do diagrama — ideal para os
quatro formatos.
- O `pdflatex` é rodado **duas vezes** para garantir que
referências internas do TikZ fiquem corretas.
- `pdftocairo -svg` gera um SVG **vetorial** (melhor qualidade
que usar `dvisvgm` com bitmap embutido).
- Se quiser PNG com fundo transparente, adicione `-transp`
ao comando `pdftocairo -png`.

## Alternativa: conversão direta para SVG com `dvisvgm` (sem PDF)

Se preferir manter o pipeline puramente TeX → SVG:

```makefile
svg:
	latex $(TEX)
	dvisvgm --no-fonts $(BASE).dvi -o $(BASE).svg
```

Mas atenção: nesse caso o PNG continua vindo do PDF,
então o pipeline misto (via PDF) costuma dar resultados
mais consistentes.
