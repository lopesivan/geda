set table "exemplo-02-bc135c1b00.plot.table"; set format "%.5f"
 f(x,y) = +1/sqrt((x+1)**2+y**2) + +1/sqrt((x-1)**2+y**2); set xrange [-3:3]; set yrange [-3:3]; set view 0,0; set isosample 400,400; set cont base; set cntrparam levels discrete 0.0,0.1,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.002,2.2,2.4,2.6; unset surface; splot f(x,y) 
