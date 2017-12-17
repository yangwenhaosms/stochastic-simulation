import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = np.loadtxt('./mc-Euler-Maruyama-weak.txt')
    y = np.loadtxt('./mc-Milstein-weak.txt')
    a = np.arange(1, 11, 1)
    plt.plot(a, x)
    plt.plot(a, y)
    label = ['Euler-Maruyama', 'Milstein']
    plt.legend(label, loc = 'upper right')
    fig = plt.gcf()
    fig.savefig('./mc-weak.eps')
