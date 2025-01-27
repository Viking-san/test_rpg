import pygame as pg
from config import *
from interface import Button


class Dialog:
    def __init__(self, text):
        self.display = pg.display.get_surface()
        self.text = text
        self.font = pg.font.Font('joystix.ttf', 20)
        self.button = Button(50, 20, 'skip', (WIDTH - 140, HEIGHT - 30))

    def draw(self):
        text = self.font.render(self.text, 0, 'white', 'black')
        rect = text.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
        self.display.blit(text, rect)
        if self.button.update():
            print('skip')
            return True
        return False