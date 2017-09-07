from app import App
import pygame
import logging
import sys
import os
import click


@click.command()
@click.option('--dev', is_flag=True, default=False, help='Dev mode')
def run(dev):
    if 'SDL_VIDEO_WINDOW_POS' not in os.environ:
        os.environ['SDL_VIDEO_CENTERED'] = '1' # This makes the window centered on the screen

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        stream=sys.stdout
    )

    logging.getLogger().setLevel(logging.DEBUG if dev else logging.WARNING)

    logging.info('Initializing PyGame/{} (with SDL/{})'.format(
        pygame.version.ver,
        '.'.join(str(v) for v in pygame.get_sdl_version())
    ))

    pygame.init()

    if dev:
        logging.info('Dev mode enabled')

    app = App(dev_mode=dev)

    logging.info('Running game')

    while True:
        app.update()

if __name__ == '__main__':
    run()
