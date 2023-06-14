set term post eps enh color font "Times-Roman, 26"
set enc iso

set out 'composition_estimate.eps'

a = 5.6
b = 5.84

unset key

set xlab "Time (s)"
set ylab "x in CsPbBr_{3-x}Cl_x"

c = 0.993096
d = 1.54959
e = 0.5
f(x) = d*tanh(1e-2*c*x)**(e)

# don't refit until commenting outliers out again
#fit f(x) 'cell.dat' u 1:(3*(1-($2-a)/(b-a)))  via c,d

plot [-10:310][-0.05:3.05] 'cell.dat' u 1:(3*(1-($2-a)/(b-a))) pt 7 ps 2 w p, f(x)






