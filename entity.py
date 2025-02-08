import pygame as pg
from config import *
from interface import *
from effects import MyEffects
from copy import copy
from pathfinder import Pathfinder
from ability_storage import Cooldown


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
        self.cooldown = None
        self.pathfinder = Pathfinder()
        self.pathfinder_control = False
        self.player = None
        self.global_ticks = None
        self.statistics = {'killed': {}, 'collected': {}}

    def activate_cooldown(self):
        self.cooldown = Cooldown(self.abilities)

    def moving(self):
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

    def is_los(self, rect):
        tl_start = self.hit_box.topleft + pg.math.Vector2(1, 1)
        tl_end = rect.topleft + pg.math.Vector2(1, 1)
        tr_start = self.hit_box.topright + pg.math.Vector2(-1, 1)
        tr_end = rect.topright + pg.math.Vector2(-1, 1)
        bl_start = self.hit_box.bottomleft + pg.math.Vector2(1, -1)
        bl_end = rect.bottomleft + pg.math.Vector2(1, -1)
        br_start = self.hit_box.bottomright + pg.math.Vector2(-1, -1)
        br_end = rect.bottomright + pg.math.Vector2(-1, -1)

        for obstacle in self.obstacles:
            check = any([obstacle.rect.clipline(tl_start, tl_end),
                         obstacle.rect.clipline(tr_start, tr_end),
                         obstacle.rect.clipline(br_start, br_end),
                         obstacle.rect.clipline(bl_start, bl_end)])
            if check:
                return False
        return True

    def add_statistics(self, action, type):
        if action == 'killed':
            if type in self.statistics['killed']:
                self.statistics['killed'][type] += 1
            else:
                self.statistics['killed'][type] = 1

    def is_dead(self):
        is_dead = self.health <= 0
        if is_dead:
            if self.type != 'player':
                self.player.add_statistics('killed', self.type)
            print(f'{self.type} is dead')
            self.kill()
        return is_dead

    def get_distance_and_direction(self, pos):
        polar_vector = pg.math.Vector2(0, -1)
        enemy_vector = pg.math.Vector2(self.rect.center)
        player_vector = pg.math.Vector2(pos)

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
                self.my_effects.add_effect(sprite.effects)

                if sprite.die_by_collide_enemy:
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

    def ability_is_ready(self, ability):
        return self.cooldown.cant_use.get(ability, {'time_remain': 0})['time_remain'] <= 0

    def attack(self, ability):
        if self.ability_is_ready(ability):
            self.abilities[ability]['method'](self)

    def all_entities_updater(self, offset, bullets, global_ticks):
        self.is_moving = False
        self.global_ticks = global_ticks
        self.cooldown.update(global_ticks)
        self.my_effects.update(offset)
        self.collide_bullets(bullets)
        self.offset = offset

    def identical_enemies_updater(self, offset, player, player_bullets, global_ticks):
        self.all_entities_updater(offset, player_bullets, global_ticks)

        if self.is_dead():
            self.kill()

        self.player = player
        distance = self.get_distance_and_direction(player.rect.center)
        self.make_decision(distance, player)

        if self.pathfinder_control:
            self.pathfinder.update(self, offset)
