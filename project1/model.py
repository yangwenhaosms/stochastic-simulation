import numpy as np


class Isingmodel(object):
    def __init__(self, d, N, J, h, k, T, propasal_type='singleflip', decisision_type='metropolis'):
        self.d = d
        self.N = N
        self.J = J
        self.h = h
        self.k = k
        self.T = T
        self.beta = 1.0 / (k * T)
        self.proposal_type = propasal_type
        self.decision_type = decisision_type
        self.board = None
        self._init_board()

    def _init_board(self):
        self.board = np.random.choice(
            (-1, 1), size=[self.N for _ in range(self.d)])

    def _compute_H(self, board):
        board_copy = board.copy()
        h1 = np.sum(board_copy)
        h2 = 0
        axes = np.array([i for i in range(self.d)])
        for _ in range(self.d):
            new = np.concatenate(
                (np.array([np.zeros(board_copy[-1].shape, dtype=np.int64)]), board_copy[:-1]))
            h2 += np.sum(new * board_copy)
            board_copy = np.transpose(board_copy, np.roll(axes, 1))
        H = - self.J * h2 - self.h * h1
        return H

    def simulate(self, iters):
        H_record = np.zeros((iters,))
        for i in range(iters):
            self.decision()
            H_record[i] = self._compute_H(self.board)
        return np.mean(H_record)

    def proposal(self):
        if self.proposal_type == 'singleflip':
            index1 = np.random.randint(self.N)
            index2 = np.random.randint(self.N)
            board_new = self.board.copy()
            board_new[index1, index2] *= -1
            return board_new
        elif self.proposal_type == 'equiprob':
            while True:
                board_new = np.random.choice(
                    (-1, 1), size=[self.N for _ in range(self.d)])
                if not np.all(board_new == self.board):
                    return board_new
        else:
            return NotImplementedError

    def decision(self):
        if self.decision_type == 'metropolis':
            new_board = self.proposal()
            H1 = self._compute_H(self.board)
            H2 = self._compute_H(new_board)
            if H2 - H1 <= 0:
                self.board = new_board
            else:
                prob = np.random.uniform()
                if prob <= np.exp(-self.beta * (H2 - H1)):
                    self.board = new_board
