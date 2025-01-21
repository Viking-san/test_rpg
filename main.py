import pygame as pg
from config import *
from player import Player
from enemy import *
from tiles import *
from interface import *
from spells import *


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Test RPG')

        self.display = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.visible_sprites = pg.sprite.Group()
        self.obstacle_sprite = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemy_bullet = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

        self.abilities = {'create_bullet': {'method': self.create_bullet, 'key': 101, 'sprite': 'sprite/bullet.png'},
                          'create_fireball': {'method': self.create_fireball, 'key': pg.K_f, 'sprite': 'sprite/fireball.png'},
                          'create_frostbolt': {'method': self.create_frostbolt, 'key': pg.K_r, 'sprite': 'sprite/frostbolt.png'},
                          }

        self.player = Player([], (0, 0), self.abilities, self.obstacle_sprite)



        self.hotkeys = HotKeys(self.abilities)

        self.offset = pg.math.Vector2()

        self.create_map()

        self.running = True

    def create_map(self):
        for y, map_string in enumerate(MAP):
            for x, tile in enumerate(map_string):
                pos = (x * TILE_SIZE, y * TILE_SIZE)
                if tile == 'x':
                    Tile([self.visible_sprites], pos)
                elif tile == 'e':
                    Sceleton([self.enemies], pos, self.abilities, self.obstacle_sprite)
                elif tile == 'f':
                    FireElemental([self.enemies], pos, self.abilities, self.obstacle_sprite)
                elif tile == 'w':
                    ObstacleTile([self.visible_sprites, self.obstacle_sprite], pos)

    def camera(self):
        self.offset.x = self.player.rect.centerx - WIDTH // 2
        self.offset.y = self.player.rect.centery - HEIGHT // 2

        for sprite in self.visible_sprites:
            offset = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset)

        for sprite in self.enemies:
            offset = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset)
            sprite.hp_bar.draw(self.display, sprite.health, sprite.rect.midbottom - self.offset + (-25, 5))

        self.enemies.update(self.offset, self.player, self.bullets)

        offset = self.player.rect.topleft - self.offset
        self.display.blit(self.player.image, offset)
        self.player.hp_bar.draw(self.display, self.player.health, self.player.rect.center - self.offset + (-25, 25))
        self.player.update(self.offset, self.enemies, self.enemy_bullet)

        self.bullets.update(self.offset)
        self.enemy_bullet.update(self.offset)

    def draw(self):
        self.display.fill('white')

        self.camera()
        self.hotkeys.update(self.display)

        if self.player.is_dead():
            self.running = False

        pg.display.update()

    def run(self):
        while self.running:
            self.draw()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if not self.hotkeys.lock:
                        rect_id = self.hotkeys.check_hotkeys_bar_collide_mouse()
                        k = event.key
                        if rect_id != -1 and k not in self.hotkeys.busy_keys:
                            self.hotkeys.set_pressed_key(rect_id, k)
                    if event.key == pg.K_ESCAPE:
                        self.running = False

    def bullet_group(self, attacker):
        bullet_group = self.bullets if attacker.type == 'player' else self.enemy_bullet
        return bullet_group

    def create_bullet(self, attacker):
        Bullet([self.visible_sprites, self.bullet_group(attacker)], attacker, self.obstacle_sprite)

    def create_fireball(self, attacker):
        Fireball([self.visible_sprites, self.bullet_group(attacker)], attacker, self.obstacle_sprite)

    def create_frostbolt(self, attacker):
        Frostblot([self.visible_sprites, self.bullet_group(attacker)], attacker, self.obstacle_sprite)


game = Game()
game.run()
