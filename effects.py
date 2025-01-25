import pygame as pg
from copy import copy


class Freeze:
    def __init__(self, entity, data):
        print('freeze')
        self.type = 'freeze'
        self.entity = entity

        self.icon = pg.image.load('sprite/frenzied.png').convert_alpha()

        self.works_time = 1000
        self.expire = False

        self.begin_at = pg.time.get_ticks()

        self.change_entity()

    def restore_entity(self):
        self.entity.speed = copy(self.entity.original_speed)
        self.entity.image = copy(self.entity.original_surf)

        self.expire = True

    def change_entity(self):
        self.surf = copy(self.entity.image)
        blue_mask = pg.Surface(self.entity.rect.size)
        blue_mask.fill((0, 255, 255))
        self.surf.blit(blue_mask, (0, 0), special_flags=pg.BLEND_RGB_MULT)

        ice_image = copy(self.icon)
        ice_image = pg.transform.scale(ice_image, self.entity.rect.size)
        self.surf.blit(ice_image, (0, 0))

        self.entity.image = self.surf
        self.entity.speed = 0

    def timer(self):
        current_time = pg.time.get_ticks()

        if current_time >= self.works_time + self.begin_at:
            print('unfreeze')
            self.restore_entity()

    def update(self):
        self.change_entity()
        self.timer()
        return self.expire


class Burning:
    def __init__(self, entity, data):
        print('burning')
        _, tick_time, damage = data.split('|')
        self.type = 'burning'
        self.entity = entity
        self.icon = pg.image.load('sprite/burns.png').convert_alpha()

        self.tick_time = 1000
        if int(tick_time) < 1000:
            self.tick_time = int(tick_time)

        self.ticks = 3
        self.tick_damage = int(damage) / self.ticks
        self.ticks_count = 1

        self.begin_at = pg.time.get_ticks()
        self.expire = False

        self.change_entity()

    def change_entity(self):
        self.surf = copy(self.entity.image)
        red_mask = pg.Surface(self.entity.rect.size)
        red_mask.fill((255, 215, 0))
        self.surf.blit(red_mask, (0, 0), special_flags=pg.BLEND_RGB_MULT)

        burn_image = self.icon
        burn_image = pg.transform.scale(burn_image, self.entity.rect.size)
        self.surf.blit(burn_image, (0, 0))

        self.entity.image = self.surf

    def restore_entity(self):
        self.entity.image = copy(self.entity.original_surf)

        self.expire = True
        print('unburn')

    def timer(self):
        current_time = pg.time.get_ticks()

        if current_time > self.begin_at + self.tick_time * self.ticks_count:
            self.ticks_count += 1
            if self.ticks_count > self.ticks:
                self.restore_entity()
            self.entity.health -= self.tick_damage

            print(int(self.entity.health))

    def update(self):
        self.change_entity()
        self.timer()
        return self.expire


class Slow:
    def __init__(self, entity, data):
        self.type = 'slow'
        self.entity = entity
        self.icon = pg.image.load('sprite/burns.png').convert_alpha()

        self.works_time = 1500

        self.begin_at = pg.time.get_ticks()
        self.expire = False

        self.change_entity()

    def restore_entity(self):
        self.entity.speed = self.entity.original_speed
        self.expire = True

    def change_entity(self):
        if self.entity.speed >= 1:
            self.entity.speed = 1

    def timer(self):
        current_time = pg.time.get_ticks()

        if current_time >= self.works_time + self.begin_at:
            print('unslow')
            self.restore_entity()

    def update(self):
        self.change_entity()
        self.timer()
        return self.expire


class MyEffects:
    def __init__(self, entity):
        self.my_effects = []
        self.entity = entity

        self.all_effects = {
            'freeze': Freeze,
            'burning': Burning,
            'slow': Slow,
        }

    def add_effect(self, effects):
        if not effects:
            return

        for effect in effects:
            effect0 = effect.split('|')[0]
            for my_effect in self.my_effects:
                if effect0 == my_effect.type:
                    self.my_effects.remove(my_effect)
            self.my_effects.append(self.all_effects[effect0](self.entity, effect))

    def update(self, offset):
        for effect in self.my_effects:
            if effect.update():
                self.my_effects.remove(effect)
