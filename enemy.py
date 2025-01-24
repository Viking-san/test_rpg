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
        # self.hit_box = deepcopy(self.rect)
        self.hit_box = self.rect.inflate(-6, -6)

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

    def make_decision(self, distance, player, offset):
        if distance > self.agro_radius:
            return

        self.lock_on_player = True
        if not self.is_los(player, offset):
            self.lock_on_player = False
            if not self.path:
                self.pathfinder.set_points(self, player)
                self.path = self.pathfinder.get_path_rects()

            point = self.path[0]
            self.go_to_point(point)

            # print path
            # for rect in self.path:
            #     x = rect.x - offset.x
            #     y = rect.y - offset.y
            #     pg.draw.rect(self.display, 'black', (x, y, *rect.size))

        elif distance <= self.attack_radius:
            self.attack()
            self.path = []
        else:
            self.moving()
            self.path = []

    def update(self, offset, player, player_bullets):
        if self.is_dead():
            self.kill()
        self.collide_bullets(player_bullets)
        self.my_effects.update(offset)

        distance = self.get_distance_and_direction(player)
        self.make_decision(distance, player, offset)


class FireElemental(Entity):
    def __init__(self, groups, pos, abilities, obstacles):
        super().__init__(groups)

        self.type = 'fire elemental'
        self.original_surf = pg.image.load('sprite/fireelemental.png')
        self.image = copy(self.original_surf)
        self.rect = self.image.get_rect(topleft=(pos))
        # self.hit_box = deepcopy(self.rect)
        self.hit_box = self.rect.inflate(-6, -6)

        self.health = 1900
        self.max_health = 1900
        self.original_speed = 3
        self.speed = self.original_speed

        self.abilities = abilities
        self.hp_bar = Bars(50, 8, 'green', self.max_health)

        self.agro_radius = 400
        self.attack_radius = 50

        self.obstacles = obstacles

    def attack(self):
        self.abilities['create_fireball']['method'](self)

    def make_decision(self, distance, player, offset):

        if distance > self.agro_radius:
            return

        if self.pathfinder_control:
            return

        if not self.is_los(player):
            self.pathfinder.go_find(self, player, offset)
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
        self.make_decision(distance, player, offset)

        if self.pathfinder_control:
            self.pathfinder.update(self, offset)

        print(self.is_casting)
