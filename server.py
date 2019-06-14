from tornado import websocket
import tornado.ioloop

class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        print("Websocket Opened")

    def on_message(self, message):
        print(type(message))
        if isinstance(message, str):
            print(message)
            self.write_message(u"You said: %s" % message)
        else:
            print(len(message))
            self.write_message(u"You said: %d" % len(message))

    def on_close(self):
        print("Websocket closed")

application = tornado.web.Application([(r"/", EchoWebSocket),])

if __name__ == "__main__":
    application.listen(8001)
    tornado.ioloop.IOLoop.instance().start()
