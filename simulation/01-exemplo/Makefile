NGSPICE := /home/linuxbrew/.linuxbrew/Cellar/ivan/ngspice/bin/ngspice
SCHEM   := exemplo.sch
NETLIST := exemplo.sp
DATA    := exemplo.dat
PLOT    := plot.py
PYTHON  := PYENV_VERSION=jupyter python3

.PHONY: all run plot clean

all: plot

$(NETLIST):
	./gera_netlist.sh $(SCHEM) $(NETLIST)

run: $(NETLIST)
	$(NGSPICE) -b $(NETLIST)

plot: run
	$(PYTHON) $(PLOT) $(DATA)

clean:
	rm -f $(DATA) $(NETLIST) *~
