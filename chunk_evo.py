import matplotlib.pyplot as plt
import numpy as np
import qutip as qt
import random
import gate_class

args = {'W':4.5, 'W_d':4.5, 'A':0.068, 'b':0.4, 'sigma':130, 't_0': 390, 'alpha':-0.2, 'gate':'x', 'q':4}
time_range = np.linspace(0,2*args['t_0'],2)
qpsi0 = qt.basis(args['q'],0)
choice = ['X', 'Y']

my_GateEvo = gate_class.GateEvo(time_range, qpsi0, args)
result = my_GateEvo.make_result()
c_val = result.final_state*qt.qeye(4)

for i in range(10):
    args['gate'] = random.choice(choice)
    my_GateEvo = gate_class.GateEvo(time_range, qpsi0, args)
    result = my_GateEvo.make_result()
    c_val = [[result.expect[0][-1]], [result.expect[1][-1]], [result.expect[2][-1]], [result.expect[3][-1]]]
    print(c_val)
    qpsi0 = qt.Qobj(c_val)

fig, ax = plt.subplots()

ax.plot(time_range, result.expect[0])
ax.plot(time_range, result.expect[1])
ax.plot(time_range, result.expect[2])
ax.plot(time_range, result.expect[3])

plt.show()

input("\nPress enter to exit")