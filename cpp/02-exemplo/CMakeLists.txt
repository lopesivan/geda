cmake_minimum_required(VERSION 3.28)

project(geda_cpp VERSION 0.1.0 LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# === Nome do programa (definido em um único ponto) ===
set(APP_NAME geda-test)

# Força o pkg-config a procurar também em /opt/geda
set(ENV{PKG_CONFIG_PATH} "/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig")

find_package(PkgConfig REQUIRED)

pkg_check_modules(GEDA REQUIRED IMPORTED_TARGET libgeda)
pkg_check_modules(GEDACAIRO REQUIRED IMPORTED_TARGET libgedacairo)

add_executable(${APP_NAME} src/main.cpp)

target_link_libraries(${APP_NAME} PRIVATE
    PkgConfig::GEDA
    PkgConfig::GEDACAIRO
)

set_target_properties(${APP_NAME} PROPERTIES
    BUILD_RPATH "/opt/geda/lib"
)
