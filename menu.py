import pygame as pg
from interface import Button
from config import *


class Pause:
    def __init__(self, display):
        self.display = display
        self.font = pg.font.Font('joystix.ttf', 32)
        self.text = self.font.render('Pause', 0, 'white')
        self.rect = self.text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.surf = pg.Surface(self.rect.size)

        self.restart_button = Button(self.rect.width, 50, 'restart', self.rect.bottomleft)

        self.pause_button = Button(self.rect.width, 50, 'exit', self.restart_button.rect.bottomleft)

    def draw(self):
        self.display.blit(self.surf, self.rect)
        self.display.blit(self.text, self.rect)

    def update(self):
        self.draw()
        if self.pause_button.is_used():
            return 1
        if self.restart_button.is_used():
            return 2
        return 0
