import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = np.loadtxt('./RW-EIG-N-5000.txt')
    plt.hist(x, 500)
    fig = plt.gcf()
    fig.savefig('./RW-EIG-N-5000.eps')
