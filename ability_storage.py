from spells import *


class AllAbilities:
    def __init__(self, sprite_groups):
        self.sprite_groups = sprite_groups
        self.obstacles = self.sprite_groups['obstacle_sprites']
        self.visible = self.sprite_groups['visible_sprites']

        self.abilities = {
                'bullet': {
                        'method': self.create_bullet,
                        'key': 101,
                        'sprite': 'sprite/bullet.png',},
                'fireball': {
                        'method': self.create_fireball,
                        'key': pg.K_f,
                        'sprite': 'sprite/fireball.png',},
                'frostbolt': {
                        'method': self.create_frostbolt,
                        'key': pg.K_r,
                        'sprite': 'sprite/frostbolt.png',},
                'flame_strike': {
                        'method': self.flame_strike,
                        'key': pg.K_q,
                        'sprite': 'sprite/flame_strike_attack.png',},
                'blizzard': {
                        'method': self.blizzard,
                        'key': pg.K_t,
                        'sprite': 'sprite/blizzard_attack.png',},
                'blink': {
                        'method': self.blink,
                        'key': pg.K_b,
                        'sprite': 'sprite/blink.png',},
              }

    def get_abilities(self, abilities):
        result = {}
        for ability in self.abilities:
            if ability in abilities:
                result[ability] = self.abilities[ability]
        return result

    def bullet_group(self, attacker):
        if attacker.type == 'player':
            bullet_group = self.sprite_groups['bullets']
        else:
            bullet_group = self.sprite_groups['enemy_bullet']
        return bullet_group

    def create_bullet(self, attacker):
        Bullet((self.visible, self.bullet_group(attacker)), attacker, self.obstacles)

    def create_fireball(self, attacker):
        Fireball((self.visible, self.bullet_group(attacker)), attacker, self.obstacles)

    def create_frostbolt(self, attacker):
        Frostblot((self.visible, self.bullet_group(attacker)), attacker, self.obstacles)

    def flame_strike(self, attacker):
        FlameStrike((self.visible, self.bullet_group(attacker)), attacker)

    def blizzard(self, attacker):
        Blizzard((self.visible, self.bullet_group(attacker)), attacker)

    def blink(self, attacker):
        Blink(attacker)


class Cooldown:
    def __init__(self, abilities):
        self.abilities = abilities
        self.cant_use = dict()

    def add_ability(self, ability, global_ticks, cooldown):
        self.cant_use[ability] = {'cast_time': global_ticks, 'time_remain': cooldown, 'cooldown': cooldown}

    def clear_ability(self):
        abilities_for_remove = []
        for ability in self.cant_use:
            if self.cant_use[ability]['time_remain'] == 0:
                abilities_for_remove.append(ability)

        for ability in abilities_for_remove:
            del self.cant_use[ability]

    def timers(self, global_ticks):
        current_time = global_ticks
        for ability in self.cant_use:
            remain = max(self.cant_use[ability]['cooldown'] + self.cant_use[ability]['cast_time'] - current_time, 0)
            self.cant_use[ability]['time_remain'] = remain

    def update(self, global_ticks):
        self.timers(global_ticks)
        self.clear_ability()
