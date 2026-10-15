#!/usr/bin/env bash
set -e # Encerra em caso de erro
set -u # Trata variáveis não definidas como erro
set -o pipefail

PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig pkg-config --modversion libgeda
PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig pkg-config --modversion libgedacairo

PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig pkg-config --cflags libgeda
PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig pkg-config --libs libgeda

PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig pkg-config --cflags libgedacairo
PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig pkg-config --libs libgedacairo

exit 0
