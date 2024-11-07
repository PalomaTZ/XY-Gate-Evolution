import matplotlib.pyplot as plt
import numpy as np
import qutip as qt
from scipy.optimize import minimize
import gate_class



args = {'W':4.5, 'W_d':4.5, 'A':-0.24, 'b':0.4, 'sigma':90, 't_0': 360, 'alpha':-0.2, 'gate':'Y', 'q':4}
time_range = np.linspace(0,2*args['t_0'],200)

my_GateEvo = gate_class.GateEvo(time_range, args)
result = my_GateEvo.make_result()

#print(my_GateEvo.create_diagonal())

fig, ax = plt.subplots()

P0=qt.basis(args['q'],0)*qt.basis(args['q'],0).dag()
P1=qt.basis(args['q'],1)*qt.basis(args['q'],1).dag()
P2=qt.basis(args['q'],2)*qt.basis(args['q'],2).dag()
P3=qt.basis(args['q'],3)*qt.basis(args['q'],3).dag()

m = [np.absolute((i*P0).tr())**2 for i in result.states]
n = [np.absolute((i*P1).tr())**2 for i in result.states]
l = [np.absolute((i*P2).tr())**2 for i in result.states]
p = [np.absolute((i*P3).tr())**2 for i in result.states]

# params = [args['A'], args['sigma']]

# def minimize_func(x):
#     args['A'] = x[0]
#     args['sigma'] = x[1]
#     obj = gate_class.GateEvo(time_range, args).make_result().states[-1]
#     return 1-np.absolute((obj*P1).tr())**2

# res = minimize(minimize_func, x0=[0.07,130])
# print(res.x[0],res.x[1])

ax.plot(time_range, m)
ax.plot(time_range, n)
ax.plot(time_range, l)
ax.plot(time_range, p)

plt.show()

input("\nPress enter to exit")