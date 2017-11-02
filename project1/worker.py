import zmq
import msgpack
import msgpack_numpy
from multiprocessing import Process

msgpack_numpy.patch()

class Worker(Process):
    def __init__(self, url, work, i, iters=100000):
        super(Worker, self).__init__()
        self.url = url
        self.work = work
        self.iters = iters
        self.id = i

    def run(self):
        context = zmq.Context()
        ## zmq type 4 means REP model
        socket = context.socket(4)
        socket.connect(self.url)
        while True:
            message = socket.recv()
            print('This is worker ' + str(self.id))
            if message == b'break':
                break
            result = self.work.simulate(self.iters)
            socket.send(msgpack.dumps(result))
            self.work._init_board()

