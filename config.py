import pygame as pg


WIDTH = 640
HEIGHT = 480
TILE_SIZE = 32

FPS = 60

DEFAULT_IMAGE = pg.image.load('sprite/default.png')

MAP = [
    'wwwwwwwwwwwwwwwwwwwwwwwwwww',
    'wx x x x x x x x xwx x x ww',
    '  x x x    x x x wwwwww x w',
    'wwww  wwwwwwx x x x x x xww',
    'wx x x x x x x ww  x e x ww',
    'w x x x x x x x x x x e www',
    'wx x x x xww x x x x x x ww',
    'w x x xfx x xwwwwwwww  xwww',
    'wx x x x x x wwwwww  x x ww',
    'w x x  k x x x x x x x x xw',
    'wx x x   x x x x x xwwwwx w',
    'w x x       x x x   x xwwww',
    'wx x x x x xwww x x   wwwww',
    'w x x x x x x x x x  x x xww',
    'wx x x    x x x x x x x www',
    'w x x x x x x x x ww x xwww',
    'wx x   x x x x x x x x x ww',
    'w x x x xwww x x x x x x xw',
    'wx x x x x x x x xwwww x ww',
    'w x x x x x x x x x x x xww',
    'wwwwwwwwwwwwwwwwwwwwwwwwwww',
]


def debug(display, text):
    f = pg.font.Font(None, 20)
    y = 100
    for t in text:
        text_surf = f.render(t, 1, 'black', 'white')
        text_rect = text_surf.get_rect(topleft=(10, y))
        y = text_rect.bottom
        display.blit(text_surf, text_rect)
