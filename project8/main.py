import numpy as np
import time
from model import GOE, GUE, GOE_EIG, GUE_EIG
from server import Server
from worker import Worker
import argparse
from tqdm import tqdm

def get_spacing(type, order, number):
    if type == 'GOE':
        matrice = GOE(order, number)
        eigenvals = matrice.get_eigen_values()
        diff = np.diff(eigenvals, axis=1)
        diff_scale = diff / np.mean(diff, axis=0)
        np.savetxt('./result/GOE-N-{}.txt'.format(order), diff_scale)
    elif type == 'GUE':
        matrice = GUE(order, number)
        eigenvals = matrice.get_eigen_values()
        diff = np.diff(eigenvals, axis=1)
        diff_scale = diff / np.mean(diff, axis=0)
        np.savetxt('./result/GUE-N-{}.txt'.format(order), diff_scale)

def get_eigenvalue(type, order):
    if type == 'GOE':
        matrix = GOE_EIG(order)
        eigenvals = matrix.get_eigen_values()
        np.savetxt('./result/GOE-EIG-N-{}.txt'.format(order), eigenvals)
    elif type == 'GUE':
        matrix = GUE_EIG(order)
        eigenvals = matrix.get_eigen_values()
        np.savetxt('./result/GUE-EIG-N-{}.txt'.format(order), eigenvals)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--type', help='ensemble type', type=str, default='GOE')
    parser.add_argument('--order', help='size of matrix', type=int, default=2)
    parser.add_argument('--number', help='number of matrice', type=int, default=int(1e6))
    args = parser.parse_args()

    #get_spacing(args.type, args.order, args.number)
    get_eigenvalue(args.type, args.order)


if __name__ == '__main__':
    t0 = time.time()
    main()
    print('time cost: ' + str(time.time() - t0))
