import numpy as np
import time
from model import Black_Scholes_Multilevel
from server import Server_Multilevel
from worker import Worker_Multilevel
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tqdm import tqdm

def train_mc(mu, sigma, s0, t0, t1, algorithm, n, url_worker, num_worker, iters):
    workers = [Worker_Multilevel(url_worker, Black_Scholes_Multilevel(mu, sigma, s0, t0, t1, n, method=algorithm), i) for i in range(num_worker)]
    [w.start() for w in workers]

    sever = Server_Multilevel(url_worker, num_worker)
    res_hat, res_hat_com, res = sever.collect(maxlen=iters)
    result_hat = np.exp(-mu) * np.maximum(np.array(res_hat) - 1, 0)
    result_hat_com = np.exp(-mu) * np.maximum(np.array(res_hat_com) - 1, 0)
    result = np.exp(-mu) * np.maximum(np.array(res) - 1, 0)
    return result_hat, result_hat_com, result

def train_mmc(mu, sigma, s0, t0, t1, algorithm, url_worker, num_worker, i, k):
    res_hat = 0
    res = np.array([])
    level = i+2
    for n in range(level):
        if n == 0:
            iter = 2 ** (level - 1 - n)
        else:
            iter = n * 2 ** (level - 1 - n)
        result_hat, result_hat_com, result = train_mc(mu, sigma, s0, t0, t1, algorithm, k-(i+1)+n, url_worker, num_worker, iter)
        res_hat += np.mean(result_hat - result_hat_com)
        res = np.concatenate([res, result])
    err = np.abs(res_hat-np.mean(res))
    return err

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--algorithm', help='EM or Milsterin', type=str)
    parser.add_argument('--t0', help='begin time', type=float, default=0.0)
    parser.add_argument('--t1', help='end time', type=float, default=1.0)
    parser.add_argument('--mu', help='drift rate', type=float, default=0.05)
    parser.add_argument('--sigma', help='standard deviation', type=float, default=0.2)
    parser.add_argument('--s0', help='initial value of S', type=float, default=1.0)
    parser.add_argument('--k', help='maximum level', type=int, default=10)
    parser.add_argument('--url_worker', help='the url of worker', type=str, default='ipc://homework')
    parser.add_argument('--num_worker', help='the number of workers', type=int, default=16)
    args = parser.parse_args()

    xs = []
    ys = []
    for i in tqdm(range(args.k)):
        err = train_mmc(args.mu, args.sigma, args.s0, args.t0, args.t1, args.algorithm, args.url_worker, args.num_worker, i, args.k)
        xs.append(i+1)
        ys.append(err)
    plt.plot(xs, ys)
    plt.xlabel('n')
    plt.ylabel('scaled error')
    fig = plt.gcf()
    fig.savefig('./result/mmc-{}.eps'.format(args.algorithm))
    np.savetxt('./result/mmc-{}.txt'.format(args.algorithm), np.array([ys]), fmt='%f '*args.n)


if __name__ == '__main__':
    t0 = time.time()
    main()
    print('time cost: ' + str(time.time() - t0))
