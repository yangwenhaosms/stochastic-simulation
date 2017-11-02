import numpy as np
from project1.model import Isingmodel
from project1.server import Server
from project1.worker import Worker

def main(d, N, J, h, k, T, num_worker, iters, url_worker):
    for i in range(num_worker):
        model = Isingmodel(d, N, J, h, k, T)
        w = Worker(url_worker, model, i, iters)
        w.daemon = True
        w.start()

    sever = Server(url_worker, num_worker)
    result = sever.collect(maxlen=100)

    return result

if __name__ == '__main__':
    num_worker = 2
    result = main(2, 100, 1, 0, 1, 300, num_worker, 10000, 'ipc://homework')