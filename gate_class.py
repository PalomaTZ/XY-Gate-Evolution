import matplotlib.pyplot as plt
import numpy as np
import qutip as qt

class GateEvo:
    def __init__(self, time_range, args):
        self.time_range = time_range
        self.W = args['W']
        self.W_d = args['W_d']
        self.A = args['A']
        self.b = args['b']
        self.sigma = args['sigma']
        self.t_0 = args['t_0']
        self.alpha = args['alpha']
        self.gate = args['gate']
        self.q = args['q']
        # gate_coeff can probably be brought outside the class
        self.gate_coeff = {'X':[1,1], 'x':[0.5,0.5], 'Y':[-1,1], 'y':[-0.5,0.5]}
        self.ex = gate_coeff[args['gate']][0]
        self.ey = gate_coeff[args['gate']][1]
        self.kappa = (0.0025**0.5)*args['A']
        self.qpsi0 = qt.basis(args['q'],0)
        self.result = []
    
    def create_diagonal(self):
        if self.q<2:
            print('dimension must be greater or equal to 2')
            exit

        E_list = [0, self.W-self.W_d]
        for i in range(2,self.q):
            x = (self.W-self.W_d)*i-self.A*(2*i-3)
            E_list.append(x)

        diag_ele = qt.Qobj(np.diag(E_list))
        return diag_ele

    def create_off_terms(self):
        sm1=qt.destroy(self.q)
        X1 = sm1+sm1.dag()
        Y1 =-1.0j*sm1+1.0j*sm1.dag()
        return X1, Y1

    def gauss_wave(self, t):
        return self.ex*0.5*self.A*np.exp(-0.5*((t-self.t_0)/self.sigma)**2)

    def gauss_deriv(self, t):
        return -self.ey*0.5*(self.b*self.A/(self.sigma**2))*(t-self.t_0)*np.exp(-0.5*((t-self.t_0)/self.sigma)**2)

    X1, Y1 = self.create_off_terms()

    H1 = self.create_diagonal()

    H = qt.QobjEvo([H1, [X1, gauss_wave], [Y1, gauss_deriv]], args=args)

    def make_collapse_ops(self):
        x = np.sqrt(np.arange(1,self.q))
        matrix = []
        phase_loss = [0]
        for i in range(self.q-1):
            values = np.zeros(self.q-1)
            values[i] = x[i]
            matrix.append(qt.Qobj(kappa*np.diag(values, k=1)))
            phase_loss.append(x[i])
        #matrix.append(qt.Qobj(kappa*np.diag(phase_loss)))
        return matrix

    c_ops = self.make_collapse_ops()
    P0=qt.basis(args['q'],0)*qt.basis(args['q'],0).dag()
    P1=qt.basis(args['q'],1)*qt.basis(args['q'],1).dag()
    P2=qt.basis(args['q'],2)*qt.basis(args['q'],1).dag()
    P3=qt.basis(args['q'],3)*qt.basis(args['q'],1).dag()

    self.result = qt.mesolve(H, qpsi0, time_range, c_ops)
