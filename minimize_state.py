import matplotlib.pyplot as plt
import numpy as np
import qutip as qt
from scipy.optimize import minimize
import gate_class
import old_gate_class

def const(x):
    return x[0]

gate_list = ['X']*9
args = {'W':4.5, 'W_d':4.5, 'A':0.04, 'b':0.4, 'sigma':130, 't_0': 390, 'alpha':0.2, 'q':4}
time_range = np.linspace(0,3*args['sigma']+6*args['sigma']*len(gate_list),200)
qpsi0 = qt.basis(args['q'],0)
constraints = {'type':'ineq', 'fun':const}

P0=qt.basis(args['q'],0)*qt.basis(args['q'],0).dag()
P1=qt.basis(args['q'],1)*qt.basis(args['q'],1).dag()
P2=qt.basis(args['q'],2)*qt.basis(args['q'],2).dag()
P3=qt.basis(args['q'],3)*qt.basis(args['q'],3).dag()

params = [args['A'], args['sigma']]

def minimize_func(x):
    args['A'] = x[0]
    args['sigma'] = x[1]
    obj = old_gate_class.GateEvoTail(time_range, qpsi0, gate_list, args).make_result().expect[1][-1]
    return np.abs(1-obj)

res = minimize(minimize_func, x0=[0.01567,80], constraints=constraints)
print(res.x[0],res.x[1])

# 'X','Y' : 0.0682 , 0.4 , 130