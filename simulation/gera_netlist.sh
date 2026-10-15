#!/usr/bin/env bash
set -e
set -u
set -o pipefail

# ---------------------------------------------------------------
# Uso: ./gerar_netlist.sh <arquivo.sch> <arquivo.sp>
# ---------------------------------------------------------------
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <arquivo.sch> <arquivo.sp>" >&2
    exit 1
fi

arquivo="$1"
saida="$2"

# Verifica se o esquemático existe
if [ ! -f "$arquivo" ]; then
    echo "Erro: arquivo '$arquivo' não encontrado." >&2
    exit 1
fi

rm -f "$saida"

# Extrai o título do titleblock (T 50000 40900 ...)
titulo=$(awk '
    /^T[[:space:]]+50000[[:space:]]+40900[[:space:]]/ { pega=1; next }
    pega { print; exit }
' "$arquivo")

echo "Título: $titulo"

# Gera o netlist SPICE
PYENV_VERSION=2.7.18 gnetlist -g spice-sdb -O sort_mode -o "$saida" "$arquivo"

# Remove as 8 primeiras linhas e adiciona o título como primeira linha
{
    echo "* $titulo"
    echo
    tail -n +9 "$saida"
} > "$saida.tmp" && mv "$saida.tmp" "$saida"

cat "$saida"

exit 0
