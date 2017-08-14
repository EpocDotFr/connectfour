from enum import Enum
import pygame
import sys
import os
import gui
import utils

VERSION = '1.2'
FPS = 30
IMAGES_SIDE_SIZE = 80
COLS = 7
ROWS = 6
COLUMN_CHOOSING_MARGIN_TOP = 50
BOARD_MARGIN_TOP = IMAGES_SIDE_SIZE + COLUMN_CHOOSING_MARGIN_TOP
WINDOW_SIZE = (IMAGES_SIDE_SIZE * COLS, (IMAGES_SIDE_SIZE * ROWS) + BOARD_MARGIN_TOP)
LAN_IDENTIFIER = '51af46a9396f46cdae0eedc4efa9d7a1'
LAN_PORT = 2560
LAN_TIMEOUT = 5

# When frozen by PyInstaller, the path to the resources is different
RESOURCES_ROOT = os.path.join(sys._MEIPASS, 'resources') if getattr(sys, 'frozen', False) else 'resources'

CONFIG_FILE = 'connectfour.ini'
DEFAULT_CONFIG = {
    'master_server_endpoint': 'https://cfms.epoc.fr/api/',
    'sounds_volume': 0.1,
    'music_volume': 0.2,
    'game_name': ''
}


class GuiTheme(gui.DefaultTheme):
    def __init__(self, sounds_volume=0.5):
        gui.DefaultTheme.__init__(self)

        # self.hover_sound = utils.load_sound('hover.wav', volume=sounds_volume)
        self.click_sound = utils.load_sound('click.wav', volume=sounds_volume)


class COLORS(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 174, 0),
    BLUE = (0, 42, 224)


class GAME_STATES(Enum):
    PLAYING = 2
    WON = 4
    NO_ONE_WIN = 6


class EVENTS(Enum):
    WINNER_CHIPS_EVENT = pygame.USEREVENT + 1
    GET_ONLINE_GAMES = pygame.USEREVENT + 2
    CLEAN_LAN_GAMES = pygame.USEREVENT + 3


class LOBBY_STATES(Enum):
    HOST_ONLINE_GAME = 2
    HOST_LAN_GAME = 4
    JOIN_ONLINE_GAME = 6
    JOIN_LAN_GAME = 8


class NETWORK_ENGINE_MODE(Enum):
    HOST = 2
    JOIN = 4
