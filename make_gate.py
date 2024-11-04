import matplotlib.pyplot as plt
import numpy as np
import qutip as qt

# parameters for each pulse
args = {'W':4.5, 'W_d':4.5, 'A':0.04, 'b':0.4, 'sigma':90, 't_0': 360, 'alpha':-0.2, 'gate':'Y', 'q':4}
# When constructing the functions for the pulses in gauss_wave and gauss_deriv, this dictionary
# stores the coeff depending on the gate, determined by the 'gate' in args dictionery
gate_coeff = {'X':[1,1], 'x':[0.5,0.5], 'Y':[-1,1], 'y':[-0.5,0.5]}

def create_diagonal(q, w, w_d, a):
  if q<2:
    print('dimension must be greater or equal to 2')
    exit

  E_list = [0, w-w_d]
  for i in range(2,q):
    x = (w-w_d)*i-a*(2*i-3)
    E_list.append(x)

  diag_ele = qt.Qobj(np.diag(E_list))
  return diag_ele

def create_off_terms(q):
  sm1=qt.destroy(q)
  X1 = sm1+sm1.dag()
  Y1 =-1.0j*sm1+1.0j*sm1.dag()
  return X1, Y1

ex = gate_coeff[args['gate']][0]
ey = gate_coeff[args['gate']][1]

def gauss_wave(t, args):
  return ex*0.5*args['A']*np.exp(-0.5*((t-args['t_0'])/args['sigma'])**2)

def gauss_deriv(t, args):
  return -ey*0.5*(args['b']*args['A']/(args['sigma']**2))*(t-args['t_0'])*np.exp(-0.5*((t-args['t_0'])/args['sigma'])**2)

# Range over which the pulse will propogate
time_range = np.linspace(0,2000,300)

X1, Y1 = create_off_terms(args['q'])

H1 = create_diagonal(args['q'], args['W'], args['W_d'], args['alpha'])

H = qt.QobjEvo([H1, [X1, gauss_wave], [Y1, gauss_deriv]], args=args)

qpsi0=qt.basis(args['q'],0)
kappa = (0.0025**0.5)*args['A']

def make_collapse_ops(q):
  x = np.sqrt(np.arange(1,q))
  matrix = []
  phase_loss = [0]
  for i in range(q-1):
    values = np.zeros(q-1)
    values[i] = x[i]
    matrix.append(qt.Qobj(kappa*np.diag(values, k=1)))
    phase_loss.append(x[i])
  #matrix.append(qt.Qobj(kappa*np.diag(phase_loss)))
  return matrix

c_ops = make_collapse_ops(args['q'])
P0=qt.basis(args['q'],0)*qt.basis(args['q'],0).dag()
P1=qt.basis(args['q'],1)*qt.basis(args['q'],1).dag()
P2=qt.basis(args['q'],2)*qt.basis(args['q'],1).dag()
P3=qt.basis(args['q'],3)*qt.basis(args['q'],1).dag()

result = qt.mesolve(H, qpsi0, time_range, c_ops)

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