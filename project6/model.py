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
        self.record_w = 0

    def simulate(self):
        if self.method == 'Euler-Maruyama':
            for _ in range(self.n):
                delta_w = np.random.normal(0.0, np.sqrt((self.t1 - self.t0)/self.n))
                self.record_w += delta_w
                s = self.record_s[-1] + self.mu * self.record_s[-1] * (self.t1 - self.t0)/self.n \
                    + self.sigma * self.record_s[-1] * delta_w
                self.record_s.append(s)
        elif self.method == 'Milstein':
            for _ in range(self.n):
                delta_w = np.random.normal(0.0, np.sqrt((self.t1 - self.t0) / self.n))
                self.record_w += delta_w
                s = self.record_s[-1] + self.mu * self.record_s[-1] * (self.t1 - self.t0) / self.n \
                    + self.sigma * self.record_s[-1] * delta_w \
                    + 0.5 * self.sigma * self.sigma * self.record_s[-1] * (delta_w ** 2 - (self.t1 - self.t0) / self.n)
                self.record_s.append(s)
        res_hat = self.record_s[-1]
        res = self.s0 * np.exp((self.mu - 0.5 * self.sigma**2) * (self.t1 - self.t0) + self.sigma * self.record_w)
        self.record_w = 0
        self.record_s = [self.s0]
        return res_hat, res

class Black_Scholes_Multilevel(object):
    def __init__(self, mu, sigma, s0, t0, t1, n, method='Euler-Maruyama'):
        self.mu = mu
        self.sigma = sigma
        self.s0 = s0
        self.t0 = t0
        self.t1 = t1
        self.n = 2**n
        self.method = method
        self.record_s = [self.s0]
        self.record_s_com = [self.s0]
        self.record_w = 0

    def simulate(self):
        delta_w_com = 0
        if self.method == 'Euler-Maruyama':
            for i in range(self.n):
                delta_w = np.random.normal(0.0, np.sqrt((self.t1 - self.t0)/self.n))
                self.record_w += delta_w
                delta_w_com += delta_w
                if i % 2 == 1:
                    s_com = self.record_s_com[-1] + self.mu * self.record_s_com[-1] * 2 * (self.t1 - self.t0)/self.n \
                            + self.sigma * self.record_s_com[-1] * delta_w_com
                    delta_w_com = 0
                    self.record_s_com.append(s_com)
                s = self.record_s[-1] + self.mu * self.record_s[-1] * (self.t1 - self.t0)/self.n \
                    + self.sigma * self.record_s[-1] * delta_w
                self.record_s.append(s)
        elif self.method == 'Milstein':
            for _ in range(self.n):
                delta_w = np.random.normal(0.0, np.sqrt((self.t1 - self.t0) / self.n))
                self.record_w += delta_w
                delta_w_com += delta_w
                if _ % 2 == 1:
                    s_com = self.record_s_com[-1] + self.mu * self.record_s_com[-1] * 2 * (self.t1 - self.t0) / self.n \
                    + self.sigma * self.record_s_com[-1] * delta_w_com \
                    + 0.5 * self.sigma * self.sigma * self.record_s_com[-1] * (delta_w_com ** 2 - 2 * (self.t1 - self.t0) / self.n)
                    delta_w_com = 0
                    self.record_s_com.append(s_com)
                s = self.record_s[-1] + self.mu * self.record_s[-1] * (self.t1 - self.t0) / self.n \
                    + self.sigma * self.record_s[-1] * delta_w \
                    + 0.5 * self.sigma * self.sigma * self.record_s[-1] * (delta_w ** 2 - (self.t1 - self.t0) / self.n)
                self.record_s.append(s)
        res_hat = self.record_s[-1]
        res_hat_com = self.record_s_com[-1]
        res = self.s0 * np.exp((self.mu - 0.5 * self.sigma**2) * (self.t1 - self.t0) + self.sigma * self.record_w)
        self.record_w = 0
        self.record_s = [self.s0]
        self.record_s_com = [self.s0]
        return res_hat, res_hat_com, res
