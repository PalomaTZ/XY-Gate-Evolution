import matplotlib.pyplot as plt
import numpy as np
import qutip as qt
import gate_class

gate_list = ['X', 'X', 'X']

args = {'W':4.5, 'W_d':4.5, 'A':0.01567785, 'b':0.4, 'sigma':80, 'alpha':-0.2, 'q':4, 't_0':480}
end = 3*args['sigma']+6*args['sigma']*len(gate_list)
time_range = np.linspace(0,end,200)
qpsi0 = qt.basis(args['q'],0)

my_GateEvo = gate_class.GateEvo(time_range, qpsi0, gate_list, args)
result = [my_GateEvo.gauss_wave(t) for t in time_range]

#superimpose all the gates
def piecex(t, gate_list, args):
    condlist = []
    funclist = []
    t_0 = args['t_0']
    for i in gate_list:
        condlist.append((t_0 - 0.5*args['t_0'] < t) & (t <= t_0 + 0.5*args['t_0']))
        #funclist.append(lambda t: -1*0.5*(args['b']*args['A']/(args['sigma']**2))*(t-t_0)*np.exp(-0.5*((t-t_0)/args['sigma'])**2))
        funclist.append(lambda t: np.exp(0.5*(t-t_0)**2/args['sigma']))
        #func += -self.ey(i)*0.5*(self.b*self.A/(self.sigma**2))*(t-t_0)*np.exp(-0.5*((t-t_0)/self.sigma)**2)
        t_0 += args['t_0']
    return np.piecewise(t, condlist=condlist, funclist=funclist)


fig, ax = plt.subplots()

ax.plot()

ax.plot(time_range, piecex(time_range, gate_list, args))
# ax.plot(time_range, result.expect[0])
# ax.plot(time_range, result.expect[1])
# ax.plot(time_range, result.expect[2])
# ax.plot(time_range, result.expect[3])

plt.show()

input("\nPress enter to exit")