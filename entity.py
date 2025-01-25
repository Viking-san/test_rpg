import pygame as pg
from config import *
from interface import *
# from spells import *
from effects import MyEffects
from copy import copy
from pathfinder import Pathfinder


class Entity(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.type = 'base_entity'
        self.display = pg.display.get_surface()
        self.angle = 0

        self.health = 100
        self.max_health = 100
        self.speed = 1
        self.vector = pg.math.Vector2()
        self.offset = pg.math.Vector2()
        # self.position = None

        self.is_casting = False
        self.is_moving = False
        self.is_attacked = False

        self.my_effects = MyEffects(self)

        self.pathfinder = Pathfinder()
        self.pathfinder_control = False

        # # collide_entities
        # self.group = groups[0]

    def moving(self):
        self.is_moving = False
        self.current_pos = deepcopy(self.hit_box.center)

        self.hit_box.x += self.vector.x * self.speed
        self.collide_obstacles('h')
        self.hit_box.y += self.vector.y * self.speed
        self.collide_obstacles('v')

        if self.hit_box.center != self.current_pos:
            self.is_moving = True
            self.is_casting = False

        self.vector.x = 0
        self.vector.y = 0

        # # collide_entities
        # self.collide_entities()

    # # collide_entities
    # def collide_entities(self):
    #     for sprite in self.group:
    #         if sprite.hit_box == self.hit_box:
    #             continue
    #         if sprite.hit_box.colliderect(self.hit_box):
    #             self.hit_box.center = deepcopy(self.current_pos)

    def is_los(self, player):
        tl_start = self.hit_box.topleft + pg.math.Vector2(3, 3)
        tl_end = player.hit_box.topleft + pg.math.Vector2(3, 3)
        tr_start = self.hit_box.topright + pg.math.Vector2(-3, 3)
        tr_end = player.hit_box.topright + pg.math.Vector2(-3, 3)
        bl_start = self.hit_box.bottomleft + pg.math.Vector2(3, -3)
        bl_end = player.hit_box.bottomleft + pg.math.Vector2(3, -3)
        br_start = self.hit_box.bottomright + pg.math.Vector2(-3, -3)
        br_end = player.hit_box.bottomright + pg.math.Vector2(-3, -3)

        for obstacle in self.obstacles:
            check = any([obstacle.rect.clipline(tl_start, tl_end),
                         obstacle.rect.clipline(tr_start, tr_end),
                         obstacle.rect.clipline(br_start, br_end),
                         obstacle.rect.clipline(bl_start, bl_end)])
            if check:
                return False
        return True

    def is_dead(self):
        is_dead = self.health <= 0
        if is_dead:
            print(f'{self.type} is dead')
        return is_dead

    def get_distance_and_direction(self, player):
        polar_vector = pg.math.Vector2(0, -1)
        enemy_vector = pg.math.Vector2(self.rect.center)
        player_vector = pg.math.Vector2(player.rect.center)

        direction = (player_vector - enemy_vector)
        distance = direction.magnitude()

        if direction:
            direction.normalize_ip()
            if not self.pathfinder_control:
                self.vector = deepcopy(direction)
            self.angle = polar_vector.angle_to(direction)

        return distance

    def collide_bullets(self, bullets):
        self.is_attacked = False

        for sprite in bullets:
            if self.rect.colliderect(sprite):
                if sprite.is_casting:
                    continue
                self.health -= sprite.damage
                print(int(self.health))
                self.my_effects.add_effect(sprite.effects)

                if sprite.type not in ['flame_strike']:
                    sprite.kill()

    def collide_obstacles(self, direction):
        if direction == 'h':
            for sprite in self.obstacles:
                if self.hit_box.colliderect(sprite):
                    if self.vector.x > 0:
                        self.hit_box.right = sprite.rect.left
                    if self.vector.x < 0:
                        self.hit_box.left = sprite.rect.right

        if direction == 'v':
            for sprite in self.obstacles:
                if self.hit_box.colliderect(sprite):
                    if self.vector.y > 0:
                        self.hit_box.bottom = sprite.rect.top
                    if self.vector.y < 0:
                        self.hit_box.top = sprite.rect.bottom

        self.rect.center = deepcopy(self.hit_box.center)
