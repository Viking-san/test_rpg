from spells import *


class AllAbilities:
    def __init__(self, sprite_groups):
        self.sprite_groups = sprite_groups
        self.obstacles = self.sprite_groups['obstacle_sprites']
        self.visible = self.sprite_groups['visible_sprites']

        self.abilities = {'create_bullet': {'method': self.create_bullet, 'key': 101, 'sprite': 'sprite/bullet.png'},
                          'create_fireball': {'method': self.create_fireball, 'key': pg.K_f, 'sprite': 'sprite/fireball.png'},
                          'create_frostbolt': {'method': self.create_frostbolt, 'key': pg.K_r, 'sprite': 'sprite/frostbolt.png'},
                          'flame_strike': {'method': self.flame_strike, 'key': pg.K_q, 'sprite': 'sprite/flame_strike_attack.png'},
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
