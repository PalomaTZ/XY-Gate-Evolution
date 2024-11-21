import matplotlib.pyplot as plt
import numpy as np
import qutip as qt
import gate_class
import random

gate_type = ['X', 'Y', 'x', 'y']
gate_list = random.choices(gate_type, k=10)
print(gate_list)

# I set t_0 to be 3*sigma (three standard deviations)
args = {'W':4.5, 'W_d':4.5, 'A':0.01568, 'b':0.4, 'sigma':80, 'alpha':-0.2, 'q':4}
#can only change the step count of the time range
time_range = np.linspace(0,6*args['sigma']*len(gate_list),200)
qpsi0 = qt.basis(args['q'],0)

my_GateEvo = gate_class.GateEvo(time_range, qpsi0, gate_list, args)
result = my_GateEvo.make_result()

#print(my_GateEvo.create_diagonal())

fig, ax = plt.subplots()

ax.plot(time_range, result.expect[0], label = 'ground state')
ax.plot(time_range, result.expect[1], label = '1st excited')
ax.plot(time_range, result.expect[2], label = '2nd excited')
ax.plot(time_range, result.expect[3], label = '3rd excited')
ax.set_xlabel('Time')
ax.set_ylabel('Population')

ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=4)

plt.show()

input("\nPress enter to exit")