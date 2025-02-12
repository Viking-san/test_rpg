import pygame as pg
import csv


with open('graveyard.csv', newline='') as f:
    reader = csv.reader(f)
    GRAVEYARD_TILE_MAP = list(reader)


WIDTH = 800
HEIGHT = 600
TILE_SIZE = 32

FPS = 60

DEFAULT_IMAGE = pg.image.load('sprite/default.png')


MAP = [
    'wwwwwwwwwwwwwwwwwwwwwwwwwww',
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
