cmake_minimum_required(VERSION 3.28)

project(geda_cpp VERSION 0.1.0 LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Nome do executável.
set(PROGRAM "app" CACHE STRING "Nome do executável")

# Localização dos arquivos pkg-config do gEDA.
set(ENV{PKG_CONFIG_PATH} "/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig")

find_package(PkgConfig REQUIRED)

pkg_check_modules(GEDA REQUIRED IMPORTED_TARGET libgeda)
pkg_check_modules(GEDACAIRO REQUIRED IMPORTED_TARGET libgedacairo)

add_executable(${PROGRAM}
    src/main.cpp
    src/geda_bridge.c
)

target_include_directories(${PROGRAM} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

target_link_libraries(${PROGRAM} PRIVATE
    PkgConfig::GEDA
    PkgConfig::GEDACAIRO
)

set_target_properties(${PROGRAM} PROPERTIES
    BUILD_RPATH "/opt/geda/lib"
)

