import pygame as pg
import csv


<<<<<<< HEAD
with open('graveyard.csv', newline='') as f:
    reader = csv.reader(f)
    GRAVEYARD_TILE_MAP = list(reader)


=======
>>>>>>> e9b968bcb3cf904ba91f3af4d3129c6d46e13ab2
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 32

FPS = 60

DEFAULT_IMAGE = pg.image.load('sprite/default.png')


MAP = [
    'wwwwwwwwwwwwwwwwwwwwwwwwwww',
<<<<<<< HEAD
    'w                 w      ww',
    'w                wwwwww   w',
    'wwww  wwwwww             ww',
    'w               ww       ww',
    'w                       www',
    'w          ww            ww',
    'w             wwwwwwww  www',
    'w             wwwwww     ww',
    'w                         w',
    'w                   wwww  w',
    'w                      wwww',
    'w           www       wwwww',
    'w                        ww',
    'w                       www',
    'w                ww     www',
    'w                        ww',
    'w       www               w',
    'w                 wwwwf  ww',
    'w                        ww',
=======
    'wx x x x x x x x xwx x x ww',
    '  x x x    x x x wwwwww x w',
    'wwww  wwwwwwx x x x x x xww',
    'wx x x x x x  x ww  x  x ww',
    'w x x x x x x  x x x x  www',
    'wx x x x xww x x x x x x ww',
    'w x x x x x xwwwwwwww  xwww',
    'wx x x x x x wwwwww  x x ww',
    'w x x  k x x x x x x x   xw',
    'wx x x   x x x x x xwwwwx w',
    'w x x       x x x   x xwwww',
    'wx x x x x xwww x x   wwwww',
    'w x x x x x x x x x x x xww',
    'wx x x    x x x x x x x www',
    'w x x x x x x x x ww x xwww',
    'wx x   x x x x x x x x x ww',
    'w x x x xwww x x x x x x xw',
    'wx x x x x x x x xwwwwfx ww',
    'w x x x x x     x x x x xww',
>>>>>>> e9b968bcb3cf904ba91f3af4d3129c6d46e13ab2
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
