v 20201216 2
C 40000 40000 0 0 0 title-B.sym
C 47900 45200 1 0 0 vsin-1.sym
{
T 48600 45850 5 10 1 1 0 0 1
refdes=V1
T 48600 46050 5 10 0 0 0 0 1
device=vsin
T 48600 46250 5 10 0 0 0 0 1
footprint=none
T 48600 45650 5 10 1 1 0 0 1
value=SIN(0 {A} {f})
}
C 49600 47400 1 0 0 resistor-1.sym
{
T 49900 47800 5 10 0 0 0 0 1
device=RESISTOR
T 49600 47900 5 10 1 1 0 0 1
refdes=R1
T 49800 47200 5 10 1 1 0 0 1
value=10k
}
C 51800 45800 1 90 0 capacitor-1.sym
{
T 51100 46000 5 10 0 0 90 0 1
device=CAPACITOR
T 52200 46300 5 10 1 1 180 0 1
refdes=C1
T 50900 46000 5 10 0 0 90 0 1
symversion=0.1
T 51300 46000 5 10 1 1 0 0 1
value=1u
}
C 48000 44300 1 0 0 ground.sym
N 48200 45200 48200 44600 4
N 48200 46400 48200 47500 4
{
T 48300 47700 5 10 1 1 180 0 1
netname=in
}
N 48200 47500 49600 47500 4
N 51600 46700 51600 47500 4
N 50500 47500 51600 47500 4
{
T 51300 47600 5 10 1 1 0 0 1
netname=out
}
N 51600 45800 51600 44900 4
N 51600 44900 48200 44900 4
{
T 48400 44650 5 10 1 1 0 6 1
netname=0
}
C 42500 48900 1 0 0 spice-directive-1.sym
{
T 42600 49200 5 10 0 1 0 0 1
device=directive
T 42600 49300 5 10 1 1 0 0 1
refdes=A1
T 42600 49000 5 10 0 2 0 0 1
file=unknown
T 42500 47500 5 10 1 1 0 0 9
value=
.param A        = 10
.param f         = 1k
.param n        = 3
.param np      = 100
.param T        = {1/f}
.param tstart  = {T/100}
.param tstop  = {n*T}
.param tstep  = {(tstop-tstart)/(np-1)}
}
C 42500 45600 1 0 0 spice-directive-1.sym
{
T 42600 45900 5 10 0 1 0 0 1
device=directive
T 42600 46000 5 10 1 1 0 0 1
refdes=A2
T 42600 45700 5 10 0 2 0 0 1
file=unknown
T 42500 45600 5 10 1 1 0 0 1
value=.tran {tstep} {tstop} {tstart}
}
T 50000 40900 9 20 1 0 0 0 1
Circuito RC com fonte senoidal
T 50000 40350 9 10 1 0 0 0 1
exemplo.sch
T 53900 40350 9 10 1 0 0 0 1
1.0
T 50000 40100 9 10 1 0 0 0 1
1
T 51500 40100 9 10 1 0 0 0 1
1
T 53900 40100 9 10 1 0 0 0 1
Ivan Carlos da Silva Lopes
