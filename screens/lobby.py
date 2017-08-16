from screens import menu
import networking.lan
import networking.engine
import pygame
import logging
import settings
import utils
import sys
import socket
import gui
import time


class Lobby:
    def __init__(self, app, lobby_type):
        logging.info('Initializing lobby')

        self.app = app
        self.lobby_type = lobby_type
        self.games_list = {}

        logging.info('Type: {}'.format(self.lobby_type))

        logging.info('Loading fonts')

        self.title_font = utils.load_font('monofur.ttf', 24)
        self.normal_font = utils.load_font('monofur.ttf', 18)

        gui.init()

        self.gui_container = pygame.sprite.Group()

        if self.lobby_type == settings.LOBBY_STATES.HOST_ONLINE_GAME:
            self.create_online_game()
        elif self.lobby_type == settings.LOBBY_STATES.JOIN_ONLINE_GAME:
            self.get_online_games()
            pygame.time.set_timer(settings.EVENTS.GET_ONLINE_GAMES.value, 5000)
        elif self.lobby_type == settings.LOBBY_STATES.HOST_LAN_GAME:
            self.lan_announcer = networking.lan.Announcer(game_name=self.app.config.get('connectfour', 'game_name'))
            self.lan_announcer.start()

            networking.engine.Engine(settings.NETWORK_ENGINE_MODE.HOST, '')
        elif self.lobby_type == settings.LOBBY_STATES.JOIN_LAN_GAME:
            self.lan_discoverer = networking.lan.Discoverer(self, self.games_list)
            self.lan_discoverer.start()

            pygame.time.set_timer(settings.EVENTS.CLEAN_LAN_GAMES.value, 3000)

    def on_server_click(self, widget):
        self.lan_discoverer.stop()
        del self.lan_discoverer

        networking.engine.Engine(settings.NETWORK_ENGINE_MODE.JOIN, widget.data['ip'])

    def update_games_list_gui(self):
        self.gui_container.empty()

        y = 50

        for ip, infos in self.games_list.items():
            game_name_label = gui.Label(
                font=self.normal_font,
                text=infos['name'],
                on_click=self.on_server_click,
                data={'ip': ip, **infos}
            )

            game_name_label.rect.left = 10
            game_name_label.rect.top = y

            self.gui_container.add(game_name_label)

            game_ip_label = gui.Label(
                font=self.normal_font,
                text='{}{}'.format(ip, ' (' + infos['country'] + ')' if 'country' in infos and infos['country'] else ''),
                on_click=self.on_server_click,
                data={'ip': ip, **infos}
            )

            game_ip_label.rect.right = settings.WINDOW_SIZE[0] - 10
            game_ip_label.rect.top = y

            self.gui_container.add(game_ip_label)

            y += 50

    def get_online_games(self):
        logging.info('Getting online games list')

        try:
            games = self.app.master_server_client.get_games(settings.VERSION)

            for game in games:
                if game['ip'] not in self.games_list:
                    self.games_list[game['ip']] = {
                        'name': game['name'],
                        'country': game['country']
                    }

            games_ip = [game['ip'] for game in games]

            for ip, infos in self.games_list.items():
                if ip not in games_ip:
                    del self.games_list[ip]

            self.update_games_list_gui()
        except Exception as e:
            logging.error(e)

    def create_online_game(self):
        if not hasattr(self.app, 'current_online_game'):
            logging.info('Creating a new online game')

            try:
                self.app.current_online_game = self.app.master_server_client.create_game(socket.gethostname(), settings.VERSION)

                # TODO Start a looping thread that POST to /games/{id} every 3 minutes without any parameter (to update the last_ping_at attribute)
            except Exception as e:
                logging.error(e)

    def delete_online_game(self):
        if hasattr(self.app, 'current_online_game') and self.app.current_online_game:
            logging.info('Deleting the current online game #{}'.format(self.app.current_online_game['id']))

            try:
                self.app.master_server_client.delete_game(self.app.current_online_game['id'], self.app.current_online_game['token'])

                del self.app.current_online_game

                # TODO Kill the looping thread that POST to /games/{id} every 3 minutes
            except Exception as e:
                logging.error(e)
        else:
            logging.info('No current online game to delete')

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                if self.lobby_type == settings.LOBBY_STATES.HOST_ONLINE_GAME:
                    self.delete_online_game()
                elif self.lobby_type == settings.LOBBY_STATES.HOST_LAN_GAME and self.lan_announcer:
                    self.lan_announcer.stop()
                    del self.lan_announcer
                elif self.lobby_type == settings.LOBBY_STATES.JOIN_LAN_GAME and self.lan_discoverer:
                    self.lan_discoverer.stop()
                    del self.lan_discoverer

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # The user want to go back to the game menu
                    self.app.set_current_screen(menu.Menu)

            if event.type == settings.EVENTS.GET_ONLINE_GAMES.value:
                self.get_online_games()
                pygame.time.set_timer(settings.EVENTS.GET_ONLINE_GAMES.value, 5000)
            if event.type == settings.EVENTS.CLEAN_LAN_GAMES.value:
                for ip, infos in self.games_list.copy().items():
                    if infos['last_ping_at'] <= time.time() - settings.LAN_TIMEOUT:
                        del self.games_list[ip]

                self.update_games_list_gui()

                pygame.time.set_timer(settings.EVENTS.CLEAN_LAN_GAMES.value, 3000)

            gui.event_handler(self.gui_container, event)

        self.app.window.fill(settings.COLORS.WHITE.value)

        if self.lobby_type == settings.LOBBY_STATES.HOST_ONLINE_GAME:
            self.draw_title('Host an online game')
        elif self.lobby_type == settings.LOBBY_STATES.HOST_LAN_GAME:
            self.draw_title('Host a LAN game')
        elif self.lobby_type == settings.LOBBY_STATES.JOIN_LAN_GAME:
            self.draw_title('Join a LAN game')
        elif self.lobby_type == settings.LOBBY_STATES.JOIN_ONLINE_GAME:
            self.draw_title('Join an online game')

        self.gui_container.update()
        self.gui_container.draw(self.app.window)

    def draw_title(self, text):
        title = self.title_font.render(text, True, settings.COLORS.BLACK.value)
        title_rect = title.get_rect()
        title_rect.left = 10
        title_rect.top = 10

        self.app.window.blit(title, title_rect)
