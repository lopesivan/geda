cmake_minimum_required(VERSION 3.28)

project(geda_cpp VERSION 0.2.0 LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS ON)

# std::span exige C++20.
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Nome do executável.
set(PROGRAM "app" CACHE STRING "Nome do executável")

# ------------------------------------------------------------
# pkg-config: gEDA, Guile e Lua 5.4 (luaenv)
# ------------------------------------------------------------
execute_process(
    COMMAND luaenv prefix 5.4.6
    OUTPUT_VARIABLE LUAENV_PREFIX
    OUTPUT_STRIP_TRAILING_WHITESPACE
    ERROR_QUIET
    RESULT_VARIABLE LUAENV_RC
)

set(_pkg_path "/usr/lib/x86_64-linux-gnu/pkgconfig:/opt/geda/lib/pkgconfig")
if(LUAENV_RC EQUAL 0 AND LUAENV_PREFIX)
    set(_pkg_path "${LUAENV_PREFIX}/pkgconfig:${_pkg_path}")
endif()
if(DEFINED ENV{PKG_CONFIG_PATH} AND NOT "$ENV{PKG_CONFIG_PATH}" STREQUAL "")
    set(_pkg_path "$ENV{PKG_CONFIG_PATH}:${_pkg_path}")
endif()
set(ENV{PKG_CONFIG_PATH} "${_pkg_path}")

find_package(PkgConfig REQUIRED)

pkg_check_modules(GEDA      REQUIRED IMPORTED_TARGET libgeda)
pkg_check_modules(GEDACAIRO REQUIRED IMPORTED_TARGET libgedacairo)
pkg_check_modules(GUILE     REQUIRED IMPORTED_TARGET guile-2.2)
pkg_check_modules(LUA       REQUIRED IMPORTED_TARGET lua54)

# ------------------------------------------------------------
# libngspice (mesmo caminho do Makefile do exemplo; sobrescreva com
# -DNGSPICE_PREFIX=/caminho se estiver em outro lugar)
# ------------------------------------------------------------
set(NGSPICE_PREFIX "" CACHE PATH "Prefixo do ngspice (contendo include/ e lib/)")

if(NOT NGSPICE_PREFIX)
    execute_process(
        COMMAND brew --prefix
        OUTPUT_VARIABLE BREW_PREFIX
        OUTPUT_STRIP_TRAILING_WHITESPACE
        ERROR_QUIET
        RESULT_VARIABLE BREW_RC
    )
    if(BREW_RC EQUAL 0 AND BREW_PREFIX)
        set(NGSPICE_PREFIX "${BREW_PREFIX}/Cellar/ivan/ngspice"
            CACHE PATH "Prefixo do ngspice (contendo include/ e lib/)" FORCE)
    endif()
endif()

find_path(NGSPICE_INCLUDE_DIR ngspice/sharedspice.h
    HINTS "${NGSPICE_PREFIX}/include")
find_library(NGSPICE_LIBRARY ngspice
    HINTS "${NGSPICE_PREFIX}/lib")

if(NOT NGSPICE_INCLUDE_DIR OR NOT NGSPICE_LIBRARY)
    message(FATAL_ERROR
        "libngspice nao encontrada. Use -DNGSPICE_PREFIX=/caminho "
        "(precisa de include/ngspice/sharedspice.h e lib/libngspice.so)")
endif()

get_filename_component(NGSPICE_LIB_DIR "${NGSPICE_LIBRARY}" DIRECTORY)

# ------------------------------------------------------------
# Executável
# ------------------------------------------------------------
add_executable(${PROGRAM}
    src/main.cpp
    src/spice_lua.cpp
    src/geda_bridge.c
)

target_include_directories(${PROGRAM} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${NGSPICE_INCLUDE_DIR}
)

target_link_libraries(${PROGRAM} PRIVATE
    PkgConfig::GEDA
    PkgConfig::GEDACAIRO
    PkgConfig::GUILE
    PkgConfig::LUA
    ${NGSPICE_LIBRARY}
    m
)

set_target_properties(${PROGRAM} PROPERTIES
    BUILD_RPATH "/opt/geda/lib;${NGSPICE_LIB_DIR};${LUA_LIBRARY_DIRS}"
)
