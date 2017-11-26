import numpy as np
import matplotlib.pyplot as plt

class Black_Scholes(object):
    def __init__(self, mu, sigma, s0, t0, t1, n, method='Euler-Maruyama'):
        self.mu = mu
        self.sigma = sigma
        self.s0 = s0
        self.t0 = t0
        self.t1 = t1
        self.n = 2**n
        self.method = method
        self.record_s = [self.s0]

    def simulate(self):
        if self.method == 'Euler-Maruyama':
            for _ in range(self.n):
                delta_w = np.random.normal(0.0, np.sqrt((self.t1 - self.t0)/self.n))
                s = self.record_s[-1] + self.mu * self.record_s[-1] * (self.t1 - self.t0)/self.n \
                    + self.sigma * self.record_s[-1] * delta_w
                self.record_s.append(s)
        elif self.method == 'Milstein':
            for _ in range(self.n):
                delta_w = np.random.normal(0.0, np.sqrt((self.t1 - self.t0) / self.n))
                s = self.record_s[-1] + self.mu * self.record_s[-1] * (self.t1 - self.t0) / self.n \
                    + self.sigma * self.record_s[-1] * delta_w \
                    + 0.5 * self.sigma * self.sigma * self.record_s[-1] * (delta_w ** 2 - (self.t1 - self.t0) / self.n)
                self.record_s.append(s)
        res = self.record_s[-1]
        self.record_s = [self.s0]
        return res


