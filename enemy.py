import pygame as pg
from interface import Bars
from copy import copy, deepcopy
from effects import *
from entity import Entity


class Sceleton(Entity):
    def __init__(self, groups, pos, abilities, obstacles):
        super().__init__(groups)

        self.type = 'sceleton'
        self.original_surf = pg.image.load('sprite/enemy.png')
        self.image = copy(self.original_surf)
        self.rect = self.image.get_rect(topleft=(pos))
        self.hit_box = deepcopy(self.rect)

        self.health = 900
        self.max_health = 900
        self.original_speed = 3
        self.speed = self.original_speed

        self.abilities = abilities
        self.hp_bar = Bars(50, 8, 'green', self.max_health)

        self.agro_radius = 300
        self.attack_radius = 150

        self.obstacles = obstacles

    def attack(self):
        self.abilities['create_bullet']['method'](self)

    def make_decision(self, distance):
        if distance <= self.attack_radius:
            self.attack()
        elif distance <= self.agro_radius:
            self.moving()

    def update(self, offset, player, player_bullets):
        if self.is_dead():
            self.kill()
        self.collide_bullets(player_bullets)
        self.my_effects.update(offset)

        distance = self.get_distance_and_direction(player)
        self.make_decision(distance)


class FireElemental(Entity):
    def __init__(self, groups, pos, abilities, obstacles):
        super().__init__(groups)

        self.type = 'fire elemental'
        self.original_surf = pg.image.load('sprite/fireelemental.png')
        self.image = copy(self.original_surf)
        self.rect = self.image.get_rect(topleft=(pos))
        self.hit_box = deepcopy(self.rect)

        self.health = 1900
        self.max_health = 1900
        self.original_speed = 5
        self.speed = self.original_speed

        self.abilities = abilities
        self.hp_bar = Bars(50, 8, 'green', self.max_health)

        self.agro_radius = 400
        self.attack_radius = 250

        self.obstacles = obstacles

    def attack(self):
        self.abilities['create_fireball']['method'](self)

    def make_decision(self, distance):
        if distance <= self.attack_radius:
            self.attack()
        elif distance <= self.agro_radius:
            self.moving()

    def update(self, offset, player, player_bullets):
        self.is_moving = False
        if self.is_dead():
            self.kill()
        self.collide_bullets(player_bullets)
        self.my_effects.update(offset)

        distance = self.get_distance_and_direction(player)
        self.make_decision(distance)
