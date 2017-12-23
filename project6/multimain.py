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
from main import train_mc

def train_mmc(mu, sigma, s0, t0, t1, algorithm, n, url_worker, num_worker, iters):
    workers = [Worker_Multilevel(url_worker, Black_Scholes_Multilevel(mu, sigma, s0, t0, t1, n, method=algorithm), i) for i in range(num_worker)]
    [w.start() for w in workers]

    sever = Server_Multilevel(url_worker, num_worker)
    res_hat, res_hat_com, res = sever.collect(maxlen=iters)
    result_hat = np.exp(-mu) * np.maximum(np.array(res_hat) - 1, 0)
    result_hat_com = np.exp(-mu) * np.maximum(np.array(res_hat_com) - 1, 0)
    result = np.exp(-mu) * np.maximum(np.array(res) - 1, 0)
    return result_hat, result_hat_com, result

def get_variance(mu, sigma, s0, t0, t1, algorithm, url_worker, num_worker, k, iters=int(1e6)):
    var = []
    res, _ = train_mc(mu, sigma, s0, t0, t1, algorithm, 0, url_worker, num_worker, iters)
    var.append(np.var(res))
    for i in tqdm(range(k)):
        res_l, res_l_1, res = train_mmc(mu, sigma, s0, t0, t1, algorithm, i+1, url_worker, num_worker, iters)
        var.append(np.var(res_l - res_l_1))
    return var

def mul_main(mu, sigma, s0, t0, t1, algorithm, url_worker, num_worker, k, epsilon):
    var = np.loadtxt('./result/mmc-var-{}.txt'.format(algorithm))
    # how to define delta in a more generalized form is undone
    delta = (t1 - t0) / (2**np.arange(0, 11, 1))
    num_sample = np.ceil(2 * np.sqrt(var * delta) * np.sum(np.sqrt(var/delta)) / (epsilon ** 2)).astype(np.int32)
    res_hat = 0
    for i in range(k):
        res_l, res_l_1, _ = train_mmc(mu, sigma, s0, t0, t1, algorithm, i+1, url_worker, num_worker, num_sample[i])




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
    parser.add_argument('--epsilon', help='the accuracy', type=float, default=0.01)
    args = parser.parse_args()

    var = get_variance(args.mu, args.sigma, args.s0, args.t0, args.t1, args.algorithm, args.url_worker, args.num_worker, args.k)
    np.savetxt('./result/mmc-var-{}.txt'.format(args.algorithm), np.array([var]), fmt='%f '*(1+args.k))


if __name__ == '__main__':
    t0 = time.time()
    main()
    print('time cost: ' + str(time.time() - t0))
