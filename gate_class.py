import matplotlib.pyplot as plt
import numpy as np
import qutip as qt

options = {"store_final_state":True}

gate_coeff = {'X':[1,1], 'x':[0.5,0.5], 'Y':[-1,1], 'y':[-0.5,0.5]}

class GateEvo:
    def __init__(self, time_range, qpsi0, gate_list, args):
        self.args = args
        self.time_range = time_range
        self.W = args['W']
        self.W_d = args['W_d']
        self.A = args['A']
        self.b = args['b']
        self.sigma = args['sigma']
        self.t_0 = 3*args['sigma']
        self.alpha = args['alpha']
        self.q = args['q']
        self.gate_list = gate_list
        self.kappa = (0.0025**0.5)*args['A']
        self.qpsi0 = qpsi0
        self.num_gates = 10
        self.pmatrices = [qt.basis(args['q'],0)*qt.basis(args['q'],0).dag(),
                        qt.basis(args['q'],1)*qt.basis(args['q'],1).dag(),
                        qt.basis(args['q'],2)*qt.basis(args['q'],2).dag(),
                        qt.basis(args['q'],3)*qt.basis(args['q'],3).dag()]
    
    def create_diagonal(self):
        if self.q<2:
            print('dimension must be greater or equal to 2')
            exit

        E_list = [0, self.W-self.W_d]
        for i in range(2,self.q):
            x = (self.W-self.W_d)*i-self.alpha*(2*i-3)
            E_list.append(x)

        diag_ele = qt.Qobj(np.diag(E_list))
        return diag_ele

    def create_off_terms(self):
        sm1=qt.destroy(self.q)
        X1 = sm1+sm1.dag()
        Y1 =-1.0j*sm1+1.0j*sm1.dag()
        return X1, Y1
    
    def ex(self, gate):
        return gate_coeff[gate][0]

    def ey(self, gate):
        return gate_coeff[gate][1]

    def gauss_wave(self, t):
        func = 0
        t_0 = self.t_0
        for i in self.gate_list:
            func += self.ex(i)*0.5*self.A*np.exp(-0.5*((t-t_0)/self.sigma)**2)
            t_0 += 2*self.t_0
        return func

    def gauss_deriv(self, t):
        func = 0
        t_0 = self.t_0
        for i in self.gate_list:
            func += -self.ey(i)*0.5*(self.b*self.A/(self.sigma**2))*(t-t_0)*np.exp(-0.5*((t-t_0)/self.sigma)**2)
            t_0 += 2*self.t_0
        return func

    def make_collapse_ops(self):
        x = np.sqrt(np.arange(1,self.q))
        matrix = []
        phase_loss = [0]
        for i in range(self.q-1):
            values = np.zeros(self.q-1)
            values[i] = x[i]
            matrix.append(qt.Qobj(self.kappa*np.diag(values, k=1)))
            phase_loss.append(x[i])
        matrix.append(qt.Qobj(self.kappa*np.diag(phase_loss)))
        return matrix

    def make_result(self):
        X1, Y1 = self.create_off_terms()
        H1 = self.create_diagonal()
        H = qt.QobjEvo([H1, [X1, self.gauss_wave], [Y1, self.gauss_deriv]], args=self.args)
        c_ops = self.make_collapse_ops()
        return qt.mesolve(H, self.qpsi0, self.time_range, c_ops, self.pmatrices, options=options)

    def final_value(self):
        result = self.make_result().states
        return result[-1]