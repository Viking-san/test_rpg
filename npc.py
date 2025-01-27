import pygame as pg
from entity import Entity
from dialog import Dialog


class Peasant(Entity):
    def __init__(self, groups, pos, player):
        super().__init__(groups)
        self.image = pg.image.load('sprite/peasant.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.player = player
        self.offset = self.player.offset

        self.dialog = Dialog('Hello, adventurer!')
        self.start_dialog = False
        self.close_dialog = False

    def interact(self):
        mouse_pos = pg.mouse.get_pos() + self.offset
        mouse_lcm = pg.mouse.get_pressed()[0]

        if self.rect.collidepoint(mouse_pos) and mouse_lcm:
            self.start_dialog = True

    def update(self, offset):
        self.offset = offset
        self.interact()

        distance = self.get_distance_and_direction(self.player)
        if self.start_dialog and distance < 100 and not self.close_dialog:
            if self.dialog.draw():
                self.close_dialog = True
                print('bye-bye')

        else:
            self.start_dialog = False
