import pygame as pg
from config import *


class Tile(pg.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pg.image.load('sprite/sand.png')
        self.rect = self.image.get_rect(topleft=pos)


class ObstacleTile(pg.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        self.image = pg.image.load('sprite/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)


class GraveyardGraphics(pg.sprite.Sprite):
    def __init__(self, groups, pos, tile_map, index):
        super().__init__(groups)
        self.image = tile_map.subsurface((int(index) * 32, 0, 32, 32))
        self.rect = self.image.get_rect(topleft=pos)
