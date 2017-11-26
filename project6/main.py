import numpy as np
import time
from project6.model import Black_Scholes
from project6.server import Server
from project6.worker import Worker
import argparse
import matplotlib.pyplot as plt

def train_mc(mu, sigma, s0, t0, t1, algorithm, n, url_worker, num_worker, iters):
    workers = [Worker(url_worker, Black_Scholes(mu, sigma, s0, t0, t1, n, method=algorithm), i) for i in range(num_worker)]
    [w.start() for w in workers]

    sever = Server(url_worker, num_worker)
    collection = sever.collect(maxlen=iters)
    result = np.exp(-mu) * np.maximum(np.array(collection) - 1, 0)
    return result

def train_mmc(mu, sigma, s0, t0, t1, algorithm, url_worker, num_worker, iters, k):
    for i in range(k):
        train_mc(mu, sigma, s0, t0, t1, algorithm, 6 + i, url_worker, num_worker, iters)
    pass


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--algorithm', help='EM or Milsterin', type=str)
    parser.add_argument('--method', help='MC or Multilevel MC', type=str)
    parser.add_argument('--t0', help='begin time', type=float, default=0.0)
    parser.add_argument('--t1', help='end time', type=float, default=1.0)
    parser.add_argument('--mu', help='drift rate', type=float, default=0.05)
    parser.add_argument('--sigma', help='standard deviation', type=float, default=0.2)
    parser.add_argument('--s0', help='initial value of S', type=float, default=1.0)
    parser.add_argument('--n', help='discretise the time with 2^n', type=int, default=8)
    parser.add_argument('--url_worker', help='the url of worker', type=str, default='ipc://homework')
    parser.add_argument('--num_worker', help='the number of workers', type=int, default=16)
    parser.add_argument('--iters', help='the number of mc', type=int, default=int(1e5))
    parser.add_argument('--k', help='the number of multilevel mc', type=int, default=2)
    args = parser.parse_args()
    if args.method == 'mc':
        res = train_mc(args.mu, args.sigma, args.s0, args.t0, args.t1, args.algorithm, args.n, args.url_worker, args.num_worker, args.iters)
        plt.hist(res, 50)
        plt.xlabel('P')
        fig = plt.gcf()
        fig.savefig('./result/{}-N:{}.eps'.format(args.algorithm, args.n))
    elif args.method == 'mmc':
        raise NotImplementedError
    else:
        raise NotImplementedError

if __name__ == '__main__':
    t0 = time.time()
    main()
    print('time cost: ' + str(time.time() - t0))