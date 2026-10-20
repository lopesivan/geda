# Makefile para animação do cone
CXX      := g++
CXXFLAGS := -std=c++17 -O3 -Wall -Wextra

TARGET := volume_cone
SRC    := volume_cone.cpp
OBJ    := $(SRC:.cpp=.o)

# Pyenv venv
PYENV_ENV := jupyter
VENV_PREFIX := $(shell pyenv prefix $(PYENV_ENV))
PYTHON      := $(VENV_PREFIX)/bin/python
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

.PHONY: all run clean video info

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) $^ -o $@ $(LDFLAGS) $(LDLIBS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

run: $(TARGET)
	PYTHONPATH="$(VENV_PREFIX)/lib/python$(PY_VER)/site-packages" ./$(TARGET)

video:
	@echo "Criando vídeo MP4..."
	ffmpeg -y -framerate 30 -i frames/frame_%04d.png -c:v libx264 -pix_fmt yuv420p cone.mp4
	@echo "✓ Vídeo criado: cone.mp4"

gif:
	@echo "Criando GIF..."
	ffmpeg -y -framerate 15 -i frames/frame_%04d.png -vf "fps=15,scale=800:-1:flags=lanczos" cone.gif
	@echo "✓ GIF criado: cone.gif"

info:
	@echo "VENV_PREFIX = $(VENV_PREFIX)"
	@echo "PYTHON      = $(PYTHON)"
	@echo "PY_VER      = $(PY_VER)"

clean:
	rm -f $(OBJ) $(TARGET)

clean-all:
	rm -f $(OBJ) $(TARGET)
	rm -rf frames
	rm -f cone.mp4 cone.gif

