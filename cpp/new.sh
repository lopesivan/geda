#!/usr/bin/env bash
set -euo pipefail

src="0X-exemplo"
base="${src#0X-}"
usar_ultimo=0

while getopts "c" opt; do
    case "$opt" in
        c) usar_ultimo=1 ;;
        *)
            echo "uso: $0 [-c]" >&2
            exit 1
            ;;
    esac
done

if [ "$usar_ultimo" -eq 1 ]; then
    ultimo=""
    ultimo_n=0
    for d in [0-9][0-9]-"$base"; do
        [ -e "$d" ] || continue
        n="${d%%-*}"
        n=$((10#$n))
        if [ "$n" -gt "$ultimo_n" ]; then
            ultimo_n="$n"
            ultimo="$d"
        fi
    done

    if [ -z "$ultimo" ]; then
        echo "erro: nenhum diretório no formato NN-${base} encontrado" >&2
        exit 1
    fi

    origem="$ultimo"
    n=$((ultimo_n + 1))
else
    if [ ! -e "$src" ]; then
        echo "erro: '$src' não existe" >&2
        exit 1
    fi
    origem="$src"
    n=1
    while :; do
        dest=$(printf "%02d-%s" "$n" "$base")
        [ -e "$dest" ] || break
        n=$((n + 1))
    done
fi

dest=$(printf "%02d-%s" "$n" "$base")

echo cp -r "$origem" "$dest"
cp -r "$origem" "$dest"
echo "$dest"
