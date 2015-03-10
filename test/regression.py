from scipy import optimize
import numpy as np

def fitfunc(p, x):
	return p[0] + p[1] * (x ** p[2])
def errfunc(p, x, y):
	return y - fitfunc(p, x)

xdata = np.array([ 0.1667,  0.2,  0.25,  0.3333, 0.5, 1, 2, 3, 4, 5, 6, 7])
ydata = np.array([ 6, 5, 4, 3, 2, 1, 0.5, 0.3333, 0.25, 0.2, 0.1667, 0.1429])

N = 1000
xprime = xdata * N

print(xprime)

qout,success = optimize.leastsq(errfunc, [0, 1, -1], args=(xprime, ydata),maxfev=3000)

out = qout[:]
out[0] = qout[0]
out[1] = qout[1] * (N**qout[2])
out[2] = qout[2]
print("%g + %g*x^%g"%(out[0],out[1],out[2]))