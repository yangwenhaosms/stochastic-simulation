import zmq
import msgpack
import msgpack_numpy
from multiprocessing import Process

msgpack_numpy.patch()


class Worker(Process):
    def __init__(self, url, work, i):
        super(Worker, self).__init__()
        self.url = url
        self.work = work
        self.id = i

    def run(self):
        context = zmq.Context()
        # zmq type 3 means REQ model
        socket = context.socket(3)
        socket.connect(self.url)
        while True:
            res_hat, res = self.work.simulate()
            socket.send(msgpack.dumps((res_hat, res)))
            message = socket.recv()
            if message == b'break':
                break