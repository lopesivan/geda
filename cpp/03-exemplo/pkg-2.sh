#!/usr/bin/env bash
set -e # Encerra em caso de erro
set -u # Trata variáveis não definidas como erro
set -o pipefail

#!/bin/bash

# Lista de pacotes
pacotes=("libgeda" "libgedacairo")

# Opções do pkg-config
opcoes=("--modversion" "--cflags" "--libs")

for pacote in "${pacotes[@]}"; do
    for opcao in "${opcoes[@]}"; do
        echo "=== pkg-config $opcao $pacote ==="
        PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig \
            pkg-config "$opcao" "$pacote"
        echo
    done
done

exit 0
