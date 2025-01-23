import pygame as pg
from config import *
from interface import *
# from spells import *
from effects import MyEffects
from copy import copy


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

        self.is_casting = False
        self.is_moving = False
        self.is_attacked = False

        self.my_effects = MyEffects(self)

    def moving(self):
        self.is_moving = False
        current_pos = deepcopy(self.hit_box.center)

        self.hit_box.x += self.vector.x * self.speed
        self.collide_obstacles('h')
        self.hit_box.y += self.vector.y * self.speed
        self.collide_obstacles('v')

        if self.hit_box.center != current_pos:
            self.is_moving = True

        self.vector.x = 0
        self.vector.y = 0

    def is_los(self, player, offset):
        line_start = self.rect.center
        line_end = player.rect.center
        for obstacle in self.obstacles:
            if obstacle.rect.clipline(line_start, line_end):
                # pg.draw.line(self.display, 'black', line_start - offset, line_end - offset, 2)
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