from screens import game
import pygame
import logging
import constants
import gui
import utils
import sys


class Menu:
    def __init__(self, app):
        logging.info('Initializing menu')

        self.app = app

        logging.info('Loading fonts')

        self.title_font = utils.load_font('monofur.ttf', 62)
        self.normal_font = utils.load_font('monofur.ttf', 18)

        logging.info('Loading GUI')

        self.load_gui()

        utils.load_music('menu.wav')

    def create_menu_button(self, y, text, on_click):
        btn_rect = pygame.Rect(0, y, 200, 40)
        btn_rect.centerx = self.app.window.get_rect().centerx

        return gui.ButtonWidget(
            rect=btn_rect,
            font=self.normal_font,
            text=text,
            text_color=constants.COLORS.WHITE.value,
            background_color=constants.COLORS.BLUE.value,
            border_color=constants.COLORS.RED.value,
            on_click=on_click
        )

    def btn_offline_game_click(self):
        self.app.set_current_screen(game.Game)

    def btn_host_online_game_click(self):
        logging.info('Host an online game button clicked')

    def btn_join_online_game_click(self):
        logging.info('Join an online game button clicked')

    def btn_host_lan_game_click(self):
        logging.info('Host a LAN game button clicked')

    def btn_join_lan_game_click(self):
        logging.info('Join a LAN game button clicked')

    def btn_quit_click(self):
        pygame.quit()
        sys.exit()

    def load_gui(self):
        self.menu_gui = pygame.sprite.Group()

        # Offline game button
        self.menu_gui.add(self.create_menu_button(
            y=200,
            text='Offline game',
            on_click=self.btn_offline_game_click
        ))

        # Host an online game button
        self.menu_gui.add(self.create_menu_button(
            y=300,
            text='Host an online game',
            on_click=self.btn_host_online_game_click
        ))

        # Join an online game button
        self.menu_gui.add(self.create_menu_button(
            y=350,
            text='Join an online game',
            on_click=self.btn_join_online_game_click
        ))

        # Host a LAN game button
        self.menu_gui.add(self.create_menu_button(
            y=450,
            text='Host a LAN game',
            on_click=self.btn_host_lan_game_click
        ))

        # Join a LAN game button
        self.menu_gui.add(self.create_menu_button(
            y=500,
            text='Join a LAN game',
            on_click=self.btn_join_lan_game_click
        ))

        # Quit button
        self.menu_gui.add(self.create_menu_button(
            y=600,
            text='Quit',
            on_click=self.btn_quit_click
        ))

    def draw_title(self):
        title = self.title_font.render('Connect Four ', True, constants.COLORS.WHITE.value)
        title_rect = title.get_rect()
        title_rect.centerx = self.app.window.get_rect().centerx
        title_rect.top = 25

        self.app.window.blit(title, title_rect)

        version = self.normal_font.render('v' + constants.VERSION, True, constants.COLORS.WHITE.value)
        version_rect = version.get_rect()
        version_rect.topright = title_rect.bottomright

        self.app.window.blit(version, version_rect)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            gui.event_handler(self.menu_gui, event)

        self.app.window.fill(constants.COLORS.BLACK.value)

        self.draw_title()

        self.menu_gui.draw(self.app.window)
