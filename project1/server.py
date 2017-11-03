import zmq
import msgpack
import msgpack_numpy
msgpack_numpy.patch()

class Server(object):
    def __init__(self, url_worker, num_worker):
        context = zmq.Context()
        ## zmq type 4 means REP model
        self.socket = context.socket(4)
        self.socket.bind(url_worker)
        self.num_worker = num_worker

    def collect(self, maxlen=1000):
        res = []
        while True:
            res.append(msgpack.loads(self.socket.recv()))
            if len(res) == maxlen:
                self.socket.send(b'break')
                for _ in range(self.num_worker - 1):
                    dummy = self.socket.recv()
                    self.socket.send(b'break')
                break
            self.socket.send(b'continue')
        return res
