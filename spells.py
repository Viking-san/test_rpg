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

        self.global_ticks = None
        self.cast_time_start = None
        self.cast_time = 1000
        self.angle = 0
        self.vector = pg.math.Vector2(0, -1)
        self.damage = 0
        self.attack = 1
        self.ttl = 1
        self.speed = 1
        self.type = 'bullet'
        self.effects = []
        self.current_cast_time = 0
        self.die_by_collide_enemy = True

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
        current_time = self.global_ticks
        cast_is_over_time = self.cast_time + self.cast_time_start
        self.current_cast_time = current_time - self.cast_time_start

        if current_time >= cast_is_over_time:
            if self.is_casting:
                self.rotate()
                self.is_casting = False
                self.player.is_casting = False
                self.damage = self.attack
                self.player.cooldown.add_ability(self.type)

        if current_time >= cast_is_over_time + self.ttl:
            self.kill()

        if self.is_casting:
            pos = self.player.hit_box.center - offset + (-25, -25)
            self.cast_bar.draw(self.display, current_time - self.cast_time_start, pos)

    def update(self, offset, global_ticks):
        self.global_ticks = global_ticks
        if not self.cast_time_start:
            self.cast_time_start = global_ticks

        self.timer(offset)
        self.collide_obstacles()
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

        self.global_ticks = None
        self.cast_time_start = None
        self.cast_time = 1000
        self.current_cast_time = 0
        self.attack = 1
        self.damage = 0
        self.ttl = 1
        self.type = 'default'
        self.effects = []

        self.cast_bar = Bars(50, 8, 'red', self.cast_time)
        self.die_by_collide_enemy = False

    def check_distance(self):
        pos_vector = pg.math.Vector2(self.pos + self.offset)
        player_vector = pg.math.Vector2(self.player.rect.center)
        distance = (player_vector - pos_vector).magnitude()
        if self.distance < distance:
            self.is_casting = False
            self.player.is_casting = False
            self.kill()

    def timer(self, offset):
        current_time = self.global_ticks
        cast_is_over_time = self.cast_time + self.cast_time_start
        self.current_cast_time = current_time - self.cast_time_start

        if current_time >= cast_is_over_time:
            if self.is_casting:
                self.is_casting = False
                self.player.is_casting = False
                self.damage = self.attack
                self.image = copy(self.surf2)
                self.player.cooldown.add_ability(self.type)

        if current_time >= cast_is_over_time + self.ttl:
            self.kill()

        if self.is_casting:
            pos = self.player.hit_box.center - offset + (-25, -25)
            self.cast_bar.draw(self.display, current_time - self.cast_time_start, pos)

    def update(self, offset, global_ticks):
        self.global_ticks = global_ticks
        if not self.cast_time_start:
            self.cast_time_start = global_ticks

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

        self.cast_time = 3000
        self.current_cast_time = 0
        self.attack = 2
        self.damage = 0
        self.ttl = 3000
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
        self.current_cast_time = 0
        self.attack = 2
        self.damage = 0
        self.ttl = 5000
        self.type = 'blizzard'
        self.effects = ['slow']

        self.cast_bar.set_max_value(self.cast_time)


class Blink:
    def __init__(self, player):
        self.player = player

        if self.player.is_casting:
            return

        self.type = 'blink'
        self.pos = pg.mouse.get_pos() + self.player.offset

        distance = self.player.get_distance_and_direction(self.pos)
        self.possible_distances = [distance // 4 * i for i in range(4)]

        self.reposition()

    def check_los(self):
        rect = pg.Rect((self.pos[0] - 13, self.pos[1] - 13, 26, 26))
        return self.player.is_los(rect)

    def find_new_pos(self):
        while not self.check_los() and self.possible_distances:
            new_pos_x = self.player.hit_box.centerx + self.player.vector.x * self.possible_distances[-1]
            new_pos_y = self.player.hit_box.centery + self.player.vector.y * self.possible_distances[-1]
            self.pos = [int(new_pos_x), int(new_pos_y)]
            self.possible_distances.pop()

        if self.check_los():
            self.player.hit_box.center = self.pos
        self.player.vector.x = 0
        self.player.vector.y = 0

    def reposition(self):
        self.find_new_pos()
        self.player.cooldown.add_ability(self.type)


