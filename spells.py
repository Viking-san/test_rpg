import pygame as pg
from interface import Bars
from config import *
from copy import copy


class ProjectileSpell(pg.sprite.Sprite):
    def __init__(self, groups, player, obstacles):
        super().__init__(groups)

        self.is_casting = True
        self.player = player
        if self.player.is_casting:
            self.kill()
        self.player.is_casting = True
        self.display = pg.display.get_surface()
        self.rotatable = True

        self.cast_time = 1000
        self.cast_time_start = pg.time.get_ticks()
        self.angle = 0
        self.vector = pg.math.Vector2(0, -1)
        self.damage = 0
        self.attack = 1
        self.ttl = 1
        self.speed = 1
        self.type = 'bullet'
        self.effects = []
        self.current_cast_time = 0

        self.obstacles = obstacles

    def collide_obstacles(self):
        for sprite in self.obstacles:
            if self.rect.colliderect(sprite):
                self.kill()

    def rotate(self):
        self.angle = self.player.angle
        self.vector = pg.math.Vector2(0, -1)
        self.vector.rotate_ip(self.angle)
        if self.rotatable:
            self.image = pg.transform.rotate(self.surf, -self.angle)

    def timer(self, offset):
        current_time = pg.time.get_ticks()
        cast_is_over_time = self.cast_time + self.cast_time_start
        self.current_cast_time = current_time - self.cast_time_start

        if current_time >= cast_is_over_time:
            if self.is_casting:
                self.rotate()
                self.is_casting = False
                self.player.is_casting = False
                self.damage = self.attack

        if current_time >= cast_is_over_time + self.ttl:
            self.kill()

        if self.is_casting:
            pos = self.player.hit_box.center - offset + (-25, -25)
            self.cast_bar.draw(self.display, current_time - self.cast_time_start, pos)

    def update(self, offset):
        self.collide_obstacles()
        # self.player.is_casting = self.is_casting
        self.timer(offset)
        if self.is_casting:
            if self.player.is_moving or self.player.is_attacked or self.player.is_dead():
                self.is_casting = False
                self.player.is_casting = False
                self.kill()
            return

        self.rect.x += self.vector.x * self.speed
        self.rect.y += self.vector.y * self.speed


class Bullet(ProjectileSpell):
    def __init__(self, groups, player, obstacles):
        super().__init__(groups, player, obstacles)

        self.surf = pg.image.load('sprite/bullet.png').convert_alpha()
        self.surf = pg.transform.scale(self.surf, (10, 10))
        self.image = self.surf
        self.rect = self.image.get_rect(center=self.player.rect.center)

        self.type = 'bullet'
        self.attack = 1
        self.speed = 9

        self.ttl = 1000
        self.cast_time = 0

        if self.cast_time:
            self.cast_bar = Bars(50, 5, 'blue', self.cast_time)

        self.rotatable = False


class Frostblot(ProjectileSpell):
    def __init__(self, groups, player, obstacles):
        super().__init__(groups, player, obstacles)

        self.surf = pg.image.load('sprite/frostbolt.png').convert_alpha()
        self.surf = pg.transform.scale(self.surf, (20, 20))
        self.image = pg.transform.rotate(self.surf, -self.angle)
        self.rect = self.image.get_rect(center=self.player.rect.center)

        self.type = 'frostbolt'
        self.attack = 20
        self.speed = 8

        self.ttl = 1000
        self.cast_time = 300

        self.cast_bar = Bars(50, 8, 'red', self.cast_time)

        self.effects = [f'freeze|{str(self.cast_time)}|{str(self.attack)}']


class Fireball(ProjectileSpell):
    def __init__(self, groups, player, obstacles):
        super().__init__(groups, player, obstacles)

        self.surf = pg.image.load('sprite/fireball.png').convert_alpha()
        self.surf = pg.transform.scale(self.surf, (20, 20))
        self.image = pg.transform.rotate(self.surf, -self.angle)
        self.rect = self.image.get_rect(center=self.player.rect.center)

        self.type = 'fireball'
        self.attack = 200
        self.speed = 4

        self.ttl = 1000
        self.cast_time = 800

        self.cast_bar = Bars(50, 8, 'red', self.cast_time)

        self.effects = [f'burning|{str(self.cast_time)}|{str(self.attack)}']


class AOEOnPoint(pg.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)

        self.display = pg.display.get_surface()
        self.surf1 = copy(DEFAULT_IMAGE)
        self.surf1 = pg.transform.scale(self.surf1, (64, 64))
        self.surf2 = copy(DEFAULT_IMAGE)
        self.surf2 = pg.transform.scale(self.surf2, (64, 64))
        self.image = copy(self.surf1)
        self.offset = player.offset
        self.pos = pg.mouse.get_pos()
        self.rect = self.image.get_rect(center=self.pos + self.offset)
        self.distance = 30

        self.is_casting = True
        self.player = player
        if self.player.is_casting:
            self.kill()
        self.player.is_casting = True
        self.display = pg.display.get_surface()

        self.cast_time = 1000
        self.cast_time_start = pg.time.get_ticks()
        self.current_cast_time = 0
        self.attack = 1
        self.damage = 0
        self.ttl = 1
        self.type = 'default'
        self.effects = []

        self.cast_bar = Bars(50, 8, 'red', self.cast_time)

    def check_distance(self):
        pos_vector = pg.math.Vector2(self.pos + self.offset)
        player_vector = pg.math.Vector2(self.player.rect.center)
        distance = (player_vector - pos_vector).magnitude()
        if self.distance < distance:
            self.is_casting = False
            self.player.is_casting = False
            self.kill()

    def timer(self, offset):
        current_time = pg.time.get_ticks()
        cast_is_over_time = self.cast_time + self.cast_time_start
        self.current_cast_time = current_time - self.cast_time_start

        if current_time >= cast_is_over_time:
            if self.is_casting:
                self.is_casting = False
                self.player.is_casting = False
                self.damage = self.attack
                self.image = copy(self.surf2)

        if current_time >= cast_is_over_time + self.ttl:
            self.kill()

        if self.is_casting:
            pos = self.player.hit_box.center - offset + (-25, -25)
            self.cast_bar.draw(self.display, current_time - self.cast_time_start, pos)

    def update(self, offset):
        self.timer(offset)
        self.offset = offset
        if self.is_casting:
            if self.player.is_moving or self.player.is_attacked or self.player.is_dead():
                self.is_casting = False
                self.player.is_casting = False
                self.kill()


class FlameStrike(AOEOnPoint):
    def __init__(self, groups, player):
        super().__init__(groups, player)

        self.surf1 = pg.image.load('sprite/flame_strike_cast.png').convert_alpha()
        self.surf1 = pg.transform.scale(self.surf1, (64, 64))
        self.surf2 = pg.image.load('sprite/flame_strike_attack.png').convert_alpha()
        self.surf2 = pg.transform.scale(self.surf2, (64, 64))
        self.image = copy(self.surf1)
        self.offset = player.offset
        self.pos = pg.mouse.get_pos()
        self.rect = self.image.get_rect(center=self.pos + self.offset)

        self.distance = 150
        self.check_distance()

        self.cast_time = 400
        self.cast_time_start = pg.time.get_ticks()
        self.current_cast_time = 0
        self.attack = 1
        self.damage = 0
        self.ttl = 2000
        self.type = 'flame_strike'
        self.effects = ['slow']

        self.cast_bar.set_max_value(self.cast_time)
        
    
class Blizzard(AOEOnPoint):
    def __init__(self, groups, player):
        super().__init__(groups, player)
        self.surf1 = pg.image.load('sprite/blizzard_cast.png').convert_alpha()
        self.surf1 = pg.transform.scale(self.surf1, (64, 64))
        self.surf2 = pg.image.load('sprite/blizzard_attack.png').convert_alpha()
        self.surf2 = pg.transform.scale(self.surf2, (64, 64))
        self.image = copy(self.surf1)
        self.offset = player.offset
        self.pos = pg.mouse.get_pos()
        self.rect = self.image.get_rect(center=self.pos + self.offset)

        self.distance = 300
        self.check_distance()

        self.cast_time = 200
        self.cast_time_start = pg.time.get_ticks()
        self.current_cast_time = 0
        self.attack = 2
        self.damage = 0
        self.ttl = 400
        self.type = 'flame_strike'
        self.effects = ['slow']

        self.cast_bar.set_max_value(self.cast_time)
