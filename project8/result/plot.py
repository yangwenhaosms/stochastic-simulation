import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = np.loadtxt('./mmc-err-Euler-Maruyama.txt')
    y = np.loadtxt('./mmc-err-Milstein.txt')
    a = np.arange(1, 5, 1)
    plt.plot(a, x)
    plt.plot(a, y)
    plt.xlabel('-log(Epsilon)')
    plt.ylabel('Absolute mean error')
    label = ['Euler-Maruyama', 'Milstein']
    plt.legend(label, loc = 'upper right')
    fig = plt.gcf()
    fig.savefig('./mmc-err.eps')
