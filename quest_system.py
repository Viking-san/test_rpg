import pygame as pg
from config import *
from interface import Button


class Dialog:
    def __init__(self, text):
        self.display = pg.display.get_surface()
        self.text = text
        self.splited_text = []
        self.font = pg.font.Font('joystix.ttf', 12)
        self.button_exit = Button(95, 20, 'exit', (165, 350))
        self.button_accept = Button(95, 20, 'accept', (10, 350))

        self.bg_rect = pg.Rect(10, 50, 250, 300)

    def split_text(self):
        max_length = 25
        current_length = 0
        string = ''
        for word in self.text.split():
            current_length += len(word)
            if current_length > max_length:
                self.splited_text.append(string)
                string = word
                current_length = len(word)
            else:
                string += ' ' + word
                current_length += 1 + len(word)

        if string:
            self.splited_text.append(string)

    def create_text(self):
        if not self.splited_text:
            self.split_text()
        y = 50

        for string in self.splited_text:
            text = self.font.render(string, 0, 'white')
            rect = text.get_rect(topleft=(10, y))

            self.display.blit(text, rect)
            y += 20

    def draw(self):
        pg.draw.rect(self.display, (50, 50, 50), self.bg_rect)
        self.create_text()

        if self.button_accept.is_used():
            print('accept')
            return 1
        if self.button_exit.is_used():
            print('exit')
            return -1
        return 0

    def change_text(self, text):
        self.text = text
        self.splited_text = []
        self.split_text()


class Quest:
    def __init__(self, player):
        self.player = player
        self.type = 'sceleton'
        self.require = 1

    def check(self):
        if self.player.statistics['killed'].get(self.type, 0) == self.require:
            return True
        else:
            return False

