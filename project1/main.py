import numpy as np
from project1.model import Isingmodel
from project1.server import Server
from project1.worker import Worker
import matplotlib.pyplot as plt

def main(d, n, j, h, k, t, num_worker, iters, url_worker):
    workers = [Worker(url_worker, Isingmodel(d, n, j, h, k, t), i, iters) for i in range(num_worker)]
    [w.start() for w in workers]

    sever = Server(url_worker, num_worker)
    result = sever.collect(maxlen=100)

    return result

if __name__ == '__main__':
    num_worker = 32
    T = np.arange(10, 500, 10)
    U = np.zeros(T.shape)
    C = np.zeros(T.shape)
    for i in range(len(T)):
        res = main(2, 100, 1, 0, 1, T[i], num_worker, 100000, 'ipc://homework')
        U[i] = np.mean(res) / (100 * 100)
        C[i] = np.var(res) / (1 * T[i] * T[i] * 100 * 100)
    plt.plot(T, U)
    plt.xlabel("Temperature")
    plt.ylabel("U")
    fig = plt.gcf()
    fig.savefig('1.eps', format='eps')
    plt.plot(T, C)
    plt.xlabel("Temperature")
    plt.ylabel("C")
    fig = plt.gcf()
    fig.savefig('2.eps', format='eps')
