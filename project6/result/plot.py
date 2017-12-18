import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = np.loadtxt('./mmc-var-Euler-Maruyama.txt')
    y = np.loadtxt('./mmc-var-Milstein.txt')
    a = np.arange(1, 11, 1)
    plt.plot(a, x)
    plt.plot(a, y)
    label = ['Euler-Maruyama', 'Milstein']
    plt.legend(label, loc = 'upper right')
    fig = plt.gcf()
    fig.savefig('./mmc-var.eps')
