import numpy as np
import matplotlib.pyplot as plt

class GOE(object):
    def __init__(self, order, n):
        self.order = order
        self.n = n
        self.gen()

    def gen(self):
        objs = np.random.normal(0, 1, (self.n, self.order, self.order))
        self.objs = (objs + np.transpose(objs, axes=[0, 2, 1])) / np.sqrt(2)

    def get_eigen_values(self):
        return np.sort(np.linalg.eigvals(self.objs), axis=1)

class GUE(object):
    def __init__(self, order, n):
        self.order = order
        self.n = n
        self.gen()

    def gen(self):
        re = np.random.normal(0, 1, (self.n, self.order, self.order))
        im = np.random.normal(0, 1, (self.n, self.order, self.order))
        self.objs = (re + np.transpose(re, axes=[0, 2, 1]))/2 + (im - np.transpose(im, axes=[0, 2, 1]))/2 * 1j

    def get_eigen_values(self):
        return np.sort(np.linalg.eigvals(self.objs).astype(np.float32), axis=1)

class GOE_EIG(object):
    def __init__(self, order):
        self.order = order
        self.gen()

    def gen(self):
        objs = np.random.normal(0, 1, (self.order, self.order))
        self.objs = ((objs + np.transpose(objs)) / np.sqrt(2)) * np.sqrt(2/self.order)

    def get_eigen_values(self):
        return np.linalg.eigvals(self.objs)

class GUE_EIG(object):
    def __init__(self, order):
        self.order = order
        self.gen()

    def gen(self):
        re = np.random.normal(0, 1, (self.order, self.order))
        im = np.random.normal(0, 1, (self.order, self.order))
        self.objs = ((re + np.transpose(re))/2 + (im - np.transpose(im))/2 * 1j) * np.sqrt(2/self.order)

    def get_eigen_values(self):
        return np.linalg.eigvals(self.objs)



