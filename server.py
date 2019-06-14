from tornado import ioloop, web, websocket
import concurrent.futures
import time
import threading

def log(msg):
    print(threading.currentThread().getName() + ": " + msg)

def worker():
    log('Enters worker')
    time.sleep(2)
    log('Exit worker')
    return "Extra"

class EchoWebSocket(websocket.WebSocketHandler):
    def open(self):
        log("Websocket Opened")

    async def on_message(self, message):
        log(type(message).__name__)
        try:
            if isinstance(message, str):
                log(message)
                await self.write_message(u"You said: %s" % message)
            else:
                log(str(len(message)))
                await self.write_message(u"You said: %d" % len(message))
        except:
            print('<<<')

        ret = await ioloop.IOLoop.current().run_in_executor(self.application.executor, worker)

        try:
            if isinstance(message, str):
                await self.write_message(u"%s %s" % (ret, message))
            else:
                await self.write_message(u"%s %d" % (ret, len(message)))
        except:
            print('>>>')

    def on_close(self):
        log("Websocket closed")

class EchoApplication(web.Application):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

if __name__ == "__main__":
    application = EchoApplication([(r"/", EchoWebSocket),])
    application.listen(8001)
    ioloop.IOLoop.instance().start()
