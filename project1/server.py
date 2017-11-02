import zmq
import msgpack
import msgpack_numpy
msgpack_numpy.patch()

class Server(object):
    def __init__(self, url_worker, num_worker):
        context = zmq.Context()
        ## zmq type 3 means REQ model
        self.socket = context.socket(3)
        self.socket.bind(url_worker)
        self.num_worker = num_worker

    def collect(self, maxlen=1000):
        res = []
        while True:
            self.socket.send(b'continue')
            res.append(msgpack.loads(self.socket.recv()))
            if len(res) == maxlen:
                for _ in range(self.num_worker):
                    self.socket.send(b'break')
                    if _ == self.num_worker - 1:
                        break
                    dummy = self.socket.recv()
                break
        return res
