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
        self.hit_box = deepcopy(self.rect)

        self.health = 1050
        self.max_health = 1500
        self.original_speed = 5.5
        self.speed = self.original_speed

        self.abilities = abilities
        self.hp_bar = Bars(50, 8, 'green', self.max_health)

        self.obstacles = obstacles

    def input(self):
        keys = pg.key.get_pressed()

        # old_pos = deepcopy(self.hit_box)
        # self.is_moving = False

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

        # if self.hit_box != old_pos:
        #     self.is_moving = True

        if keys[self.abilities['create_fireball']['key']]:
            self.abilities['create_fireball']['method'](self)

        if keys[self.abilities['create_frostbolt']['key']]:
            self.abilities['create_frostbolt']['method'](self)

        if keys[self.abilities['create_bullet']['key']]:
            self.abilities['create_bullet']['method'](self)

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


    # def collide_obstacles(self, direction):
    #     if direction == 'h':
    #         for sprite in self.obstacles:
    #             if self.rect.colliderect(sprite):
    #                 if self.vector.x > 0:
    #                     self.rect.right = sprite.rect.left
    #                 if self.vector.x < 0:
    #                     self.rect.left = sprite.rect.right
    #
    #     if direction == 'v':
    #         for sprite in self.obstacles:
    #             if self.rect.colliderect(sprite):
    #                 if self.vector.y > 0:
    #                     self.rect.bottom = sprite.rect.top
    #                 if self.vector.y < 0:
    #                     self.rect.top = sprite.rect.bottom
