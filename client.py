from tornado.ioloop import IOLoop, PeriodicCallback
from tornado import gen
from tornado.websocket import websocket_connect

class Client(object):
    def __init__(self, url, timeout):
        self.binary = False
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        PeriodicCallback(self.keep_alive, 1000).start()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        print("trying to connect")
        try:
            self.ws = yield websocket_connect(self.url)
        except:
            print("connection error")
        else:
            print("connected")
            self.run()

    @gen.coroutine
    def run(self):
        while True:
            msg = yield self.ws.read_message()
            print(msg)
            if msg is None:
                print("connection closed")
                self.ws = None
                break

    def keep_alive(self):
        print('keep alive')
        if self.ws is None:
            self.connect()
        else:
            self.ws.write_message("keep alive", self.binary)
            self.binary = not self.binary

if __name__ == "__main__":
    client = Client("ws://localhost:8001", 5)
