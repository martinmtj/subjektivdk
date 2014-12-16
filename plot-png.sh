#!/bin/bash

gnuplot << EOF

set title 'Temperatur'
set ylabel 'Celcius'
set xlabel 'Tid'
set grid
set term png
set output 'temperature.png'
set datafile separator '|'
set xdata time
set timefmt '%Y-%m-%d %H:%M:%S'

plot '< sqlite3 datalog.db "SELECT * FROM temp"' using 1:3 smooth bezier with lines title 'Indoor'

EOF
