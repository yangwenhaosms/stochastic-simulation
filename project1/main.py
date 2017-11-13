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
    res = np.zeros(T.shape)
    for i in range(len(T)):
        res[i] = main(2, 100, 1, 0, 1, T, num_worker, 100000, 'ipc://homework')
    plt.plot(T, res)
    plt.xlabel("Temperature")
    plt.ylabel("U")
    fig = plt.gcf()
    fig.savefig('1.eps', format='eps')

