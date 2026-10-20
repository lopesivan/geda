# Makefile para animações senoidais com matplotlib-cpp
CXX      := g++
CXXFLAGS := -std=c++17 -O3 -Wall -Wextra

# Nome do venv no pyenv
PYENV_ENV := jupyter
VENV_PREFIX := $(shell pyenv prefix $(PYENV_ENV))
PYTHON      := $(VENV_PREFIX)/bin/python

# Versão do Python
PY_VER := $(shell $(PYTHON) -c "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')")

# Includes
PY_INC := $(shell $(PYTHON) -c "import sysconfig; print(sysconfig.get_path('include'))")
PY_LIBDIR := $(shell $(PYTHON) -c "import sysconfig; print(sysconfig.get_config_var('LIBDIR'))")
NUMPY_INC := $(shell $(PYTHON) -c "import numpy; print(numpy.get_include())")
MPLCPP_INC := ./matplotlib-cpp

INCLUDES := -I$(PY_INC) -I$(NUMPY_INC) -I$(MPLCPP_INC)

# Linker
LDFLAGS := -L$(PY_LIBDIR) -Wl,-rpath,$(PY_LIBDIR)
LDLIBS  := -lpython$(PY_VER) -lcrypt -lpthread -ldl -lutil -lm

# Targets
TARGET_SIMPLE := sine_simple
TARGET_VARIATIONS := sine_variations

SRC_SIMPLE := sine_animation.cpp
SRC_VARIATIONS := sine_variations.cpp

OBJ_SIMPLE := $(SRC_SIMPLE:.cpp=.o)
OBJ_VARIATIONS := $(SRC_VARIATIONS:.cpp=.o)

.PHONY: all simple variations run-simple run-variations clean info

all: $(TARGET_SIMPLE) $(TARGET_VARIATIONS)

simple: $(TARGET_SIMPLE)

variations: $(TARGET_VARIATIONS)

$(TARGET_SIMPLE): $(OBJ_SIMPLE)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS) $(LDLIBS)

$(TARGET_VARIATIONS): $(OBJ_VARIATIONS)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS) $(LDLIBS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

run-simple: $(TARGET_SIMPLE)
	PYTHONPATH="$(VENV_PREFIX)/lib/python$(PY_VER)/site-packages" ./$(TARGET_SIMPLE)

run-variations: $(TARGET_VARIATIONS)
	PYTHONPATH="$(VENV_PREFIX)/lib/python$(PY_VER)/site-packages" ./$(TARGET_VARIATIONS)

info:
	@echo "VENV_PREFIX = $(VENV_PREFIX)"
	@echo "PYTHON      = $(PYTHON)"
	@echo "PY_VER      = $(PY_VER)"
	@echo "PY_INC      = $(PY_INC)"
	@echo "PY_LIBDIR   = $(PY_LIBDIR)"
	@echo "NUMPY_INC   = $(NUMPY_INC)"

clean:
	rm -f $(OBJ_SIMPLE) $(OBJ_VARIATIONS) $(TARGET_SIMPLE) $(TARGET_VARIATIONS)
	rm -rf frames
	rm *.mp4

clean-frames:
	rm -rf frames

