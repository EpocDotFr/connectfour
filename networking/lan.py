import time
import socket
import threading
import settings
import logging


class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()

        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class LanGame(StoppableThread):
    def __init__(self):
        super(LanGame, self).__init__()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.daemon = True
        self.start()

    def stop(self):
        self.socket.close()
        super(LanGame, self).stop()


class Announcer(LanGame):
    def __init__(self):
        logging.info('Running Announcer thread')

        super(Announcer, self).__init__()

        self.name = 'LanAnnouncer'

    def run(self):
        self.socket.bind(('', 0))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        data = [
            settings.LAN_IDENTIFIER, # Magic ID to recognize a Connect Four LAN game announcement
            socket.gethostname() # Name of the game (currently the hostname of this announcer)
        ]

        data = str.encode(''.join(data))

        while True:
            if self.stopped():
                break

            self.socket.sendto(data, ('<broadcast>', settings.LAN_PORT))
            time.sleep(5)


class Discoverer(LanGame):
    def __init__(self, lobby, games_list):
        logging.info('Running Discoverer thread')

        self.lobby = lobby
        self.games_list = games_list

        super(Discoverer, self).__init__()

        self.name = 'LanDiscoverer'

    def run(self):
        self.socket.bind(('', settings.LAN_PORT))

        while True:
            if self.stopped():
                break

            try:
                data, host_ip = self.socket.recvfrom(512)

                data = data.decode()
            except:
                continue

            if data:
                if not data.startswith(settings.LAN_IDENTIFIER):
                    continue

                game_name = data.replace(settings.LAN_IDENTIFIER, '')

                # We don't care if this host already exists in the games list. Erase existing so this will always update
                # old values like the game name which can change.
                self.games_list[host_ip] = {
                    'name': game_name,
                    'last_ping_at': time.time()
                }

                self.lobby.update_games_list_gui()
