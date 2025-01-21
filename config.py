import pygame as pg


WIDTH = 640
HEIGHT = 480
TILE_SIZE = 32

FPS = 60

MAP = [
    'x x x x x x x x x x x x ',
    ' x x x eeex x x wwwwww x ',
    'wwwwwwwwwwwx x x xfx x x',
    'x x x x x x x ww  x x x ',
    ' x x x x x x x x x x eex',
    'x x x x xww x x x x x x ',
    ' x x x x x xwwwwwwww e x',
    'x x x x x x wwwwww  x x ',
    ' x x    x x x x x x x x x',
    'x x x   x x x x x xwwwwx ',
    ' x xx eex x x x  x x x',
    'x x x x x xwww x x ee',
    ' x x x x x x x x x x x x',
    'x x xee  x x x x x x x ',
    ' x x x x x x x x ww x x',
    'x x x x x x x x x x x x ',
    ' x x x xwww x x x x x x x',
    'x x x x x x x x xwwww x ',
    ' x x x x x x x x x x x x',
]


def debug(display, text):
    f = pg.font.Font(None, 20)
    y = 10
    for t in text:
        text_surf = f.render(t, 1, 'black', 'white')
        text_rect = text_surf.get_rect(topleft=(10, y))
        y = text_rect.bottom
        display.blit(text_surf, text_rect)
