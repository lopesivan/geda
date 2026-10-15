NAME    := exemplo
SCHEM   := $(NAME).sch
NETLIST := $(NAME).sp
DATA    := $(NAME).dat
RAW     := $(NAME).raw
PLOT    := plot.py
PYTHON  := PYENV_VERSION=jupyter python3
GSCHEM  := /opt/geda/bin/gschem
NGSPICE := /home/linuxbrew/.linuxbrew/Cellar/ivan/ngspice/bin/ngspice

.PHONY: all run plot clean schem

all: $(NETLIST)

$(NETLIST):
	./gera_netlist.sh $(SCHEM) $(NETLIST)

schem:
	$(GSCHEM) -r gschemrc $(SCHEM)

run: $(NETLIST)
	$(NGSPICE) -b $(NETLIST)

plot: run
	$(PYTHON) $(PLOT) $(DATA)

clean:
	rm -f -- "$(DATA)" "$(NETLIST)" "$(SCHEM)~" plot.log title $(RAW)
