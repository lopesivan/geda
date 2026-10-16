
cmake_minimum_required(VERSION 3.28)

project(geda_cpp VERSION 0.1.0 LANGUAGES C CXX)

# Configuração do C.
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)

# Configuração do C++.
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Nome do executável.
set(PROGRAM "app" CACHE STRING "Nome do executável")

# Diretório de instalação do gEDA.
set(GEDA_PREFIX "/opt/geda" CACHE PATH "Diretório do gEDA")

# Adiciona o pkg-config do gEDA sem descartar os caminhos existentes.
list(PREPEND CMAKE_PREFIX_PATH "${GEDA_PREFIX}")

find_package(PkgConfig REQUIRED)

set(ENV{PKG_CONFIG_PATH} "${GEDA_PREFIX}/lib/pkgconfig:$ENV{PKG_CONFIG_PATH}")

# Bibliotecas do gEDA.
pkg_check_modules(GEDA REQUIRED IMPORTED_TARGET libgeda)
pkg_check_modules(GEDACAIRO REQUIRED IMPORTED_TARGET libgedacairo)

# Localiza o executável do ngspice.
find_program(NGSPICE_EXECUTABLE
    NAMES ngspice
    HINTS
        "/home/linuxbrew/.linuxbrew/Cellar/ivan/ngspice/bin"
        "/home/linuxbrew/.linuxbrew/bin"
    REQUIRED
)

# Executável da aplicação.
add_executable(${PROGRAM}
    src/main.cpp
    src/geda_bridge.c
)

# Headers locais.
target_include_directories(${PROGRAM} PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

# Bibliotecas.
target_link_libraries(${PROGRAM} PRIVATE
    PkgConfig::GEDA
    PkgConfig::GEDACAIRO
)

# Disponibiliza o caminho do ngspice ao código C/C++.
target_compile_definitions(${PROGRAM} PRIVATE
    NGSPICE_EXECUTABLE="${NGSPICE_EXECUTABLE}"
)

# Localização das bibliotecas compartilhadas durante a execução.
set_target_properties(${PROGRAM} PROPERTIES
    BUILD_RPATH "${GEDA_PREFIX}/lib"
)

# Informações da configuração.
message(STATUS "Programa: ${PROGRAM}")
message(STATUS "gEDA: ${GEDA_PREFIX}")
message(STATUS "ngspice: ${NGSPICE_EXECUTABLE}")
message(STATUS "libgeda: ${GEDA_VERSION}")
message(STATUS "libgedacairo: ${GEDACAIRO_VERSION}")
