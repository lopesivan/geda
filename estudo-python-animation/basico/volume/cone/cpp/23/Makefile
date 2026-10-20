# Makefile (pyenv venv jupyter + matplotlib-cpp)
# Uso:
#   make clean
#   make
#   make run

CXX      := g++
CXXFLAGS := -std=c++17 -O3 -Wall -Wextra

TARGET := main
SRC    := main.cpp
OBJ    := $(SRC:.cpp=.o)

# Nome do venv no pyenv
PYENV_ENV := jupyter

# Prefixo do venv
VENV_PREFIX := $(shell pyenv prefix $(PYENV_ENV))
PYTHON      := $(VENV_PREFIX)/bin/python

# Descobre a versão curta (ex: 3.12)
PY_VER := $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')")

# Diretório correto onde está Python.h (do Python base por trás do venv)
PY_INC := $(shell $(PYTHON) -c "import sysconfig; print(sysconfig.get_path('include'))")

# Diretório da libpython (para link + rpath)
PY_LIBDIR := $(shell $(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))")

# Include do NumPy no venv
NUMPY_INC := $(shell $(PYTHON) -c "import numpy; print(numpy.get_include())")

# matplotlib-cpp
MPLCPP_INC := ./matplotlib-cpp

INCLUDES := -I$(PY_INC) -I$(NUMPY_INC) -I$(MPLCPP_INC)

# Linka com libpython e dependências comuns
LDFLAGS := -L$(PY_LIBDIR) -Wl,-rpath,$(PY_LIBDIR)
LDLIBS  := -lpython$(PY_VER) -lcrypt -lpthread -ldl -lutil -lm

.PHONY: all run clean info

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS) $(LDLIBS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

run: $(TARGET)
	# Garante imports do venv (numpy/matplotlib)
	PYTHONPATH="$(VENV_PREFIX)/lib/python$(PY_VER)/site-packages" ./$(TARGET)

info:
	@echo "VENV_PREFIX = $(VENV_PREFIX)"
	@echo "PYTHON      = $(PYTHON)"
	@echo "PY_VER      = $(PY_VER)"
	@echo "PY_INC      = $(PY_INC)"
	@echo "PY_LIBDIR   = $(PY_LIBDIR)"
	@echo "NUMPY_INC   = $(NUMPY_INC)"

show:
	sxiv *.png

output.mp4:
	ffmpeg -framerate 60 -i frames/frame_%06d.png -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium output.mp4

clean:
	rm -f $(OBJ) $(TARGET)
	rm -rf frames
	rm output.mp4
