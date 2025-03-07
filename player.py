from entity import Entity
import pygame as pg
from copy import copy, deepcopy
from interface import Bars
from quest_system import Quest
from ability_storage import Cooldown
from graphics import *


class Player(Entity):
    def __init__(self, groups, pos, abilities, obstacles):
        super().__init__(groups)

        self.type = 'player'
        self.original_surf = pg.image.load('sprite/player/idle/down/down.png').convert_alpha()
        # self.original_surf = pg.image.load('sprite/player/idle/down/down.png').convert_alpha()
        self.image = copy(self.original_surf)
        self.rect = self.image.get_rect(topleft=pos)
        self.hit_box = self.rect.inflate(-6, -6)
        self.obstacles = obstacles

        self.health = 1050
        self.max_health = 1500
        self.original_speed = 5.5
        self.speed = self.original_speed

        self.abilities = abilities
        self.ability_name_by_key = None
        self.convert_abilities()
        self.hp_bar = Bars(50, 8, 'green', self.max_health)

        self.quests = []

        self.activate_cooldown()
        self.global_ticks = None

        self.animation = AnimatePlayer(self)

    def input(self):
        keys = pg.key.get_pressed()

        self.status = 'idle'
        if keys[pg.K_w]:
            self.vector.y = -1
            self.status = 'move'
            self.direction = 'up'
        if keys[pg.K_s]:
            self.vector.y = 1
            self.status = 'move'
            self.direction = 'down'
        if keys[pg.K_a]:
            self.vector.x = -1
            self.status = 'move'
            self.direction = 'left'
        if keys[pg.K_d]:
            self.vector.x = 1
            self.status = 'move'
            self.direction = 'right'

        if self.vector:
            self.vector.normalize_ip()

        self.moving()

        for key in self.ability_name_by_key:
            if keys[key]:
                self.attack(self.ability_name_by_key[key])

    def convert_abilities(self):
        result = {}
        abilities_list = list(self.abilities.keys())
        for ability in abilities_list:
            result[self.abilities[ability]['key']] = ability
        self.ability_name_by_key = result

    def follow_mouse(self):
        polar_vector = pg.math.Vector2(0, -1)
        mouse_pos = pg.math.Vector2(pg.mouse.get_pos()) + self.offset
        rect_pos = pg.math.Vector2(self.rect.centerx, self.rect.centery)
        direction = mouse_pos - rect_pos

        self.angle = polar_vector.angle_to(direction)
        self.angle = self.angle if self.angle > 0 else 360 + self.angle

        if self.angle < 45:
            self.direction = 'up'
        elif self.angle < 135:
            self.direction = 'right'
        elif self.angle < 225:
            self.direction = 'down'
        elif self.angle < 315:
            self.direction = 'left'
        else:
            self.direction = 'up'

    def check_quests(self):
        for quest in self.quests:
            if quest.check():
                print('finished')

    def update(self, offset, enemies, enemy_bullets, global_ticks):
        self.animation.update()
        self.all_entities_updater(offset, enemy_bullets, global_ticks)
        self.input()
        # self.check_quests()
