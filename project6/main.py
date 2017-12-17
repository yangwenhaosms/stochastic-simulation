import numpy as np
import time
from model import Black_Scholes
from server import Server
from worker import Worker
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tqdm import tqdm

def train_mc(mu, sigma, s0, t0, t1, algorithm, n, url_worker, num_worker, iters):
    workers = [Worker(url_worker, Black_Scholes(mu, sigma, s0, t0, t1, n, method=algorithm), i) for i in range(num_worker)]
    [w.start() for w in workers]

    sever = Server(url_worker, num_worker)
    res_hat, res = sever.collect(maxlen=iters)
    result_hat = np.exp(-mu) * np.maximum(np.array(res_hat) - 1, 0)
    result = np.exp(-mu) * np.maximum(np.array(res) - 1, 0)
    return result_hat, result


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--algorithm', help='EM or Milsterin', type=str)
    parser.add_argument('--t0', help='begin time', type=float, default=0.0)
    parser.add_argument('--t1', help='end time', type=float, default=1.0)
    parser.add_argument('--mu', help='drift rate', type=float, default=0.05)
    parser.add_argument('--sigma', help='standard deviation', type=float, default=0.2)
    parser.add_argument('--s0', help='initial value of S', type=float, default=1.0)
    parser.add_argument('--n', help='discretise the time with 2^n', type=int, default=10)
    parser.add_argument('--url_worker', help='the url of worker', type=str, default='ipc://homework')
    parser.add_argument('--num_worker', help='the number of workers', type=int, default=16)
    parser.add_argument('--iters', help='the number of mc', type=int, default=int(1e6))
    parser.add_argument('--strong', help='strong convergence or weak convergence', type=str, default='strong')

    args = parser.parse_args()

    xs = []
    ys = []
    for i in tqdm(range(args.n)):
        res_hat, res = train_mc(args.mu, args.sigma, args.s0, args.t0, args.t1, args.algorithm, i+1, args.url_worker, args.num_worker, args.iters)
        if args.strong == 'strong':
            err = np.mean(np.abs(res_hat - res))
        elif args.strong == 'weak':
            err = np.abs(np.mean(res_hat - res))
        # if args.algorithm == 'Euler-Maruyama':
        #     if args.strong == 'strong':
        #         scale = np.sqrt((args.t1 - args.t0)/2**args.n)
        #     elif args.strong == 'weak':
        #         scale = (args.t1 - args.t0) / 2**args.n
        # elif args.algorithm == 'Milstein':
        #     scale = (args.t1 - args.t0) / 2**args.n
        # else:
        #     raise NotImplemented
        xs.append(i+1)
        ys.append(err)
    plt.plot(xs, ys)
    plt.xlabel('n')
    plt.ylabel('error')
    fig = plt.gcf()
    fig.savefig('./result/mc-{}-{}.eps'.format(args.algorithm, args.strong))
    np.savetxt('./result/mc-{}-{}.txt'.format(args.algorithm, args.strong), np.array([ys]), fmt='%f '*args.n)


if __name__ == '__main__':
    t0 = time.time()
    main()
    print('time cost: ' + str(time.time() - t0))
