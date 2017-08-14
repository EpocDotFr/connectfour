from autobahn.asyncio.websocket import WebSocketServerFactory, WebSocketServerProtocol, WebSocketClientFactory, WebSocketClientProtocol
import json
import asyncio
import logging
import threading
import settings


class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()

        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class Engine(StoppableThread):
    def __init__(self, mode, ip):
        super(Engine, self).__init__()

        self.mode = mode
        self.ip = ip
        self.daemon = True
        self.name = str(mode)

        logging.info('Running network engine on {}'.format(ip))

        self.start()

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        if self.mode == settings.NETWORK_ENGINE_MODE.HOST:
            self.factory = WebSocketServerFactory()
            self.factory.protocol = ConnectFourServerProtocol

            self.coro = self.loop.create_server(self.factory, self.ip, 80)
        elif self.mode == settings.NETWORK_ENGINE_MODE.JOIN:
            self.factory = WebSocketClientFactory()
            self.factory.protocol = ConnectFourClientProtocol

            self.coro = self.loop.create_connection(self.factory, self.ip, 80)

        self.connection = self.loop.run_until_complete(self.coro)
        self.loop.run_forever()

    def stop(self):
        self.connection.close()
        self.loop.close()

        super(Engine, self).stop()


class ConnectFourServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        logging.info('WebSocket connection open')

    def onConnect(self, request):
        logging.info('New client: {}'.format(request.peer))

    def onClose(self, wasClean, code, reason):
        logging.info('Client quits: {}'.format(reason))

    def onMessage(self, payload, isBinary=False):
        payload = json.loads(payload.decode('utf8'))

        print(payload)

    def sendMessage(self, payload, isBinary=False):
        payload = json.dumps(payload, ensure_ascii=False).encode('utf8')

        super(WebSocketServerProtocol, self).sendMessage(payload, isBinary)


class ConnectFourClientProtocol(WebSocketClientProtocol):
    def onOpen(self):
        logging.info('WebSocket connection open')

    def onConnect(self, request):
        logging.info('Connected to host: {}'.format(request.peer))

        self.sendMessage({'coucou': True})

    def onMessage(self, payload, isBinary=False):
        payload = json.loads(payload.decode('utf8'))

        print(payload)

    def sendMessage(self, payload, isBinary=False):
        payload = json.dumps(payload, ensure_ascii=False).encode('utf8')

        super(WebSocketClientProtocol, self).sendMessage(payload, isBinary)
