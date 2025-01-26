from entity import Entity
import pygame as pg
from copy import copy, deepcopy
from interface import Bars


class Player(Entity):
    def __init__(self, groups, pos, abilities, obstacles):
        super().__init__(groups)

        self.type = 'player'
        self.original_surf = pg.image.load('sprite/ship.png').convert_alpha()
        self.image = copy(self.original_surf)
        self.rect = self.image.get_rect(topleft=pos)
        self.hit_box = self.rect.inflate(-6, -6)

        self.health = 1050
        self.max_health = 1500
        self.original_speed = 5.5
        self.speed = self.original_speed

        self.abilities = abilities
        self.ability_key_method = None
        self.convert_abilities()
        self.hp_bar = Bars(50, 8, 'green', self.max_health)

        self.obstacles = obstacles

    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.vector.y = -1
        if keys[pg.K_s]:
            self.vector.y = 1
        if keys[pg.K_a]:
            self.vector.x = -1
        if keys[pg.K_d]:
            self.vector.x = 1

        if self.vector:
            self.vector.normalize_ip()

        self.moving()

        for key in self.ability_key_method:
            if keys[key]:
                self.ability_key_method[key](self)

    def convert_abilities(self):
        result = {}
        abilities_list = list(self.abilities.keys())
        for ability in abilities_list:
            result[self.abilities[ability]['key']] = self.abilities[ability]['method']
        self.ability_key_method = result

    def follow_mouse(self):
        polar_vector = pg.math.Vector2(0, -1)
        mouse_pos = pg.math.Vector2(pg.mouse.get_pos()) + self.offset
        rect_pos = pg.math.Vector2(self.rect.centerx, self.rect.centery)
        direction = mouse_pos - rect_pos

        self.angle = polar_vector.angle_to(direction)
        self.image = pg.transform.rotate(self.original_surf, -self.angle)
        self.rect = self.image.get_rect(center=self.hit_box.center)

    def update(self, offset, enemies, enemy_bullets):
        self.offset = offset
        self.input()
        self.follow_mouse()
        self.collide_bullets(enemy_bullets)
        self.my_effects.update(offset)
