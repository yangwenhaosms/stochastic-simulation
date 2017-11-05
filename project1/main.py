import numpy as np
from project1.model import Isingmodel
from project1.server import Server
from project1.worker import Worker


def main(d, n, j, h, k, t, num_worker, iters, url_worker):
    workers = [Worker(url_worker, Isingmodel(d, n, j, h, k, t), i, iters) for i in range(num_worker)]
    [w.start() for w in workers]

    sever = Server(url_worker, num_worker)
    result = sever.collect(maxlen=100)

    return result


if __name__ == '__main__':
    num_worker = 16
    result = main(2, 100, 1, 0, 1, 300, num_worker, 100000, 'ipc://homework')
