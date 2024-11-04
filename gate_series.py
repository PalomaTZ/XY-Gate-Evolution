import matplotlib.pyplot as plt
import numpy as np
import qutip as qt
import gate_class

args = {'W':4.5, 'W_d':4.5, 'A':0.04, 'b':0.4, 'sigma':90, 't_0': 360, 'alpha':-0.2, 'gate':'Y', 'q':4}
time_range = np.linspace(0,2000,300)

my_GateEvo = gate_class.GateEvo(time_range, args)
result = my_GateEvo.result()

fig, ax = plt.subplots()

m = [np.absolute((i*P0).tr())**2 for i in result.states]
n = [np.absolute((i*P1).tr())**2 for i in result.states]
l = [np.absolute((i*P2).tr())**2 for i in result.states]
p = [np.absolute((i*P3).tr())**2 for i in result.states]

ax.plot(time_range, m)
ax.plot(time_range, n)
ax.plot(time_range, l)
ax.plot(time_range, p)

plt.show()

input("\nPress enter to exit")