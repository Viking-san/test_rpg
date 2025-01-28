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
        self.hit_box = self.rect.inflate(-6, -6)
        self.current_pos = deepcopy(self.hit_box.center)

        self.health = 900
        self.max_health = 900
        self.original_speed = 3
        self.speed = self.original_speed

        self.abilities = abilities
        self.hp_bar = Bars(50, 8, 'green', self.max_health)

        self.agro_radius = 300
        self.attack_radius = 150

        self.obstacles = obstacles

        self.player = None

    def attack(self):
        self.abilities['create_bullet']['method'](self)

    def make_decision(self, distance, player):
        if distance > self.agro_radius or self.pathfinder_control:
            return

        if not self.is_los(player):
            self.pathfinder.go_find(self, player)
        elif distance <= self.attack_radius:
            self.attack()
        else:
            self.moving()

    def update(self, offset, player, player_bullets):
        if self.is_dead():
            self.kill()
        self.collide_bullets(player_bullets)
        self.my_effects.update(offset)

        self.player = player

        distance = self.get_distance_and_direction(player)
        self.make_decision(distance, player)

        if self.pathfinder_control:
            self.pathfinder.update(self, offset)


class FireElemental(Entity):
    def __init__(self, groups, pos, abilities, obstacles):
        super().__init__(groups)

        self.type = 'fire elemental'
        self.original_surf = pg.image.load('sprite/fireelemental.png')
        self.image = copy(self.original_surf)
        self.rect = self.image.get_rect(topleft=(pos))
        self.hit_box = self.rect.inflate(-6, -6)

        self.health = 1900
        self.max_health = 1900
        self.original_speed = 3
        self.speed = self.original_speed

        self.abilities = abilities
        self.hp_bar = Bars(50, 8, 'green', self.max_health)

        self.agro_radius = 400
        self.attack_radius = 250

        self.obstacles = obstacles

    def attack(self):
        self.abilities['create_fireball']['method'](self)

    def make_decision(self, distance, player):
        if distance > self.agro_radius or self.pathfinder_control:
            return

        if not self.is_los(player):
            self.pathfinder.go_find(self, player)
        elif distance <= self.attack_radius:
            self.attack()
        else:
            self.moving()

    def update(self, offset, player, player_bullets):
        self.is_moving = False
        if self.is_dead():
            self.kill()
        self.collide_bullets(player_bullets)
        self.my_effects.update(offset)

        distance = self.get_distance_and_direction(player)
        self.make_decision(distance, player)

        if self.pathfinder_control:
            self.pathfinder.update(self, offset)
