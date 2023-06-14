reset

datafile = "300s.dat"

g(x) = I/(s*sqrt(2*pi))*exp(-0.5*(x-x0)**2/s**2) + bg

x0 = 30.5
I = 300
s = 0.3
bg = 250

#fit [28:33] g(x) datafile via x0,I,s,bg

plot [:] datafile w l, g(x)

print x0, x0_err,I,I_err,s,s_err

