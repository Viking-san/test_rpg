import pygame as pg
from entity import Entity


class Peasant(Entity):
    def __init__(self, groups, pos, player):
        super().__init__(groups)
        self.image = pg.image.load('sprite/peasant.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.player = player
        self.offset = player.offset

    def interact(self):
        mouse_pos = pg.mouse.get_pos() + self.offset
        mouse_lcm = pg.mouse.get_pressed()[0]
        if self.rect.collidepoint(mouse_pos) and mouse_lcm:
            print('Hello, adventurer!')

    def update(self, offset):
        self.offset = offset
        self.interact()