from spells import *


class AllAbilities:
    def __init__(self, sprite_groups):
        self.sprite_groups = sprite_groups
        self.obstacles = self.sprite_groups['obstacle_sprites']
        self.visible = self.sprite_groups['visible_sprites']

        self.abilities = {'bullet': {'method': self.create_bullet, 'key': 101, 'sprite': 'sprite/bullet.png', 'cd': 0},
                          'fireball': {'method': self.create_fireball, 'key': pg.K_f, 'sprite': 'sprite/fireball.png', 'cd': 2000},
                          'frostbolt': {'method': self.create_frostbolt, 'key': pg.K_r, 'sprite': 'sprite/frostbolt.png', 'cd': 1000},
                          'flame_strike': {'method': self.flame_strike, 'key': pg.K_q, 'sprite': 'sprite/flame_strike_attack.png', 'cd': 3000},
                          'blizzard': {'method': self.blizzard, 'key': pg.K_t, 'sprite': 'sprite/blizzard_attack.png', 'cd': 5000},
                          }

    def get_abilities(self, abilities):
        result = {}
        for ability in self.abilities:
            if ability in abilities:
                result[ability] = self.abilities[ability]
        return result

    def bullet_group(self, attacker):
        bullet_group = self.sprite_groups['bullets'] if attacker.type == 'player' else self.sprite_groups['enemy_bullet']
        return bullet_group

    def create_bullet(self, attacker):
        Bullet([self.visible, self.bullet_group(attacker)], attacker, self.obstacles)

    def create_fireball(self, attacker):
        Fireball([self.visible, self.bullet_group(attacker)], attacker, self.obstacles)

    def create_frostbolt(self, attacker):
        Frostblot([self.visible, self.bullet_group(attacker)], attacker, self.obstacles)

    def flame_strike(self, attacker):
        FlameStrike([self.visible, self.bullet_group(attacker)], attacker)

    def blizzard(self, attacker):
        Blizzard([self.visible, self.bullet_group(attacker)], attacker)


class Cooldown:
    def __init__(self, abilities):
        self.abilities = abilities
        self.cant_use = dict()

    def add_ability(self, ability):
        self.cant_use[ability] = {'cast_time': pg.time.get_ticks(), 'time_remain': self.abilities[ability]['cd']}

    def clear_ability(self):
        abilities_for_remove = []
        for ability in self.cant_use:
            if self.cant_use[ability]['time_remain'] == 0:
                abilities_for_remove.append(ability)

        for ability in abilities_for_remove:
            del self.cant_use[ability]

    def timers(self):
        current_time = pg.time.get_ticks()
        for ability in self.cant_use:
            self.cant_use[ability]['time_remain'] = max(self.abilities[ability]['cd'] + self.cant_use[ability]['cast_time'] - current_time, 0)

    def update(self):
        self.timers()
        self.clear_ability()
