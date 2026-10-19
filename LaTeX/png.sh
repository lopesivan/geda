#!/usr/bin/env bash
set -e # Encerra em caso de erro
set -u # Trata variáveis não definidas como erro
set -o pipefail

while IFS= read -r -d '' m; do
    echo == ${m%/*} ==
    make -C ${m%/*} png
done < <(find . -mindepth 2 -type f -name Makefile -print0)

exit 0
