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


class GraveyardGraphics0(pg.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        print('here')
        surf = load_graveyard_tile_map()
        self.image = surf.subsurface((0, 0, 32, 32))
        self.rect = self.image.get_rect(topleft=pos)


class GraveyardGraphics1(pg.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        surf = load_graveyard_tile_map()
        self.image = surf.subsurface((32, 0, 32, 32))
        self.rect = self.image.get_rect(topleft=pos)


class GraveyardGraphics2(pg.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        surf = load_graveyard_tile_map()
        self.image = surf.subsurface((64, 0, 32, 32))
        self.rect = self.image.get_rect(topleft=pos)


class GraveyardGraphics3(pg.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        surf = load_graveyard_tile_map()
        self.image = surf.subsurface((96, 0, 32, 32))
        self.rect = self.image.get_rect(topleft=pos)


class GraveyardGraphics4(pg.sprite.Sprite):
    def __init__(self, groups, pos):
        super().__init__(groups)
        surf = load_graveyard_tile_map()
        self.image = surf.subsurface((128, 0, 32, 32))
        self.rect = self.image.get_rect(topleft=pos)