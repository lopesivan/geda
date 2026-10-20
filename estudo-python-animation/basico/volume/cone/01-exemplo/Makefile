
#	 PYENV_VERSION=jupyter python volume_cone.py                          # tudo padrão
#	 PYENV_VERSION=jupyter python volume_cone.py -n 100                   # teste rápido
#	 PYENV_VERSION=jupyter python volume_cone.py -n 1200 --fps 120        # mais frames e mais rápido
#	 PYENV_VERSION=jupyter python volume_cone.py -n 300 -o teste.mp4      # saída personalizada
#	 PYENV_VERSION=jupyter python volume_cone.py --dpi 100                # renderização mais leve
#	 PYENV_VERSION=jupyter python volume_cone.py -h                       # ajuda
build:
	PYENV_VERSION=jupyter python volume_cone.py -n 100                    # teste rápido
show:
	ffplay volume_cone.mp4
clean:
	rm volume_cone.mp4
help:
	 PYENV_VERSION=jupyter python volume_cone.py -h                       # ajuda
