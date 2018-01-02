import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    x = np.loadtxt('./GUE-N-10.txt')[:,-1]
    plt.hist(x, 500)
    mean = np.mean(x)
    var = np.var(x)
    plt.xlabel('scaled spaceing')
    plt.title(r'Histogram: $\mu={:.3f}$, $\sigma={:.3f}$'.format(mean, np.sqrt(var)))
    fig = plt.gcf()
    fig.savefig('./GUE-N-10.eps')
