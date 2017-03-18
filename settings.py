from enum import Enum
import pygame
import sys
import os
import gui
import utils

VERSION = '1.0'
FPS = 30
IMAGES_SIDE_SIZE = 60
COLS = 7
ROWS = 6
COLUMN_CHOOSING_MARGIN_TOP = 50
BOARD_MARGIN_TOP = IMAGES_SIDE_SIZE + COLUMN_CHOOSING_MARGIN_TOP
WINDOW_SIZE = (IMAGES_SIDE_SIZE * COLS, (IMAGES_SIDE_SIZE * ROWS) + BOARD_MARGIN_TOP)
SOUNDS_VOLUME = 0.1
MUSIC_VOLUME = 0.2
LAN_IDENTIFIER = '51af46a9396f46cdae0eedc4efa9d7a1'
LAN_PORT = 2560

# When frozen by PyInstaller, the path to the resources is different
RESOURCES_ROOT = os.path.join(sys._MEIPASS, 'resources') if getattr(sys, 'frozen', False) else 'resources'

CONFIG_FILE = 'connectfour.ini'
DEFAULT_CONFIG = {
    'master_server_endpoint': 'https://cfg.epoc.fr/api/'
}


class GuiTheme(gui.DefaultTheme):
    def __init__(self):
        gui.DefaultTheme.__init__(self)

        self.hover_sound = utils.load_sound('hover.wav')
        self.click_sound = utils.load_sound('click.wav')


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
    WINNER_CHIPS_EVENT = pygame.USEREVENT + 2


class LOBBY_STATES(Enum):
    HOST_ONLINE_GAME = 2
    HOST_LAN_GAME = 4
    JOIN_ONLINE_GAME = 6
    JOIN_LAN_GAME = 8