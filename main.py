# import pygame as pg
# from config import *
# from spells import *
from player import Player
from enemy import *
from tiles import *
from interface import *
from ability_storage import AllAbilities
from npc import Peasant
from menu import *
import csv


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Test RPG')

        self.display = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.pause = False

        self.visible_sprites = pg.sprite.Group()
        self.obstacle_sprite = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemy_bullet = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.npc = pg.sprite.Group()

        sprite_groups_for_abilities = {
            'visible_sprites': self.visible_sprites,
            'bullets': self.bullets,
            'enemy_bullet': self.enemy_bullet,
            'obstacle_sprites': self.obstacle_sprite,
        }
        self.all_abilities = AllAbilities(sprite_groups_for_abilities)

        abilities_for_player = ['bullet', 'fireball', 'frostbolt', 'flame_strike', 'blizzard', 'blink']
        self.abilities_for_player = self.all_abilities.get_abilities(abilities_for_player)
        self.player = Player((), (50, 50), self.abilities_for_player, self.obstacle_sprite)
        # FireElemental((self.enemies,),
        #               (100, 50),
        #               self.all_abilities.get_abilities(['fireball', 'bullet', 'frostbolt']),
        #               self.obstacle_sprite)
        self.hotkeys = HotKeys(self.abilities_for_player)

        self.global_ticks = 0
        self.delta_ticks = 0
        self.offset = pg.math.Vector2()

        self.create_graveyard()
        self.restart()

        self.pause_menu = Pause(self.display)

    def create_graveyard(self):
        tile_map = pg.image.load('sprite/tilemap_graveyard.png').convert_alpha()

        for y, map_string in enumerate(GRAVEYARD_TILE_MAP):
            for x, tile in enumerate(map_string):
                pos = (x * TILE_SIZE, y * TILE_SIZE)
                if tile == '0':
                    GraveyardGraphics((self.visible_sprites, ), pos, tile_map, tile)
                else:
                    GraveyardGraphics((self.visible_sprites, self.obstacle_sprite), pos, tile_map, tile)

    def camera(self):
        previous_ticks = self.global_ticks
        self.global_ticks = pg.time.get_ticks()
        if self.pause:
            self.delta_ticks += self.global_ticks - previous_ticks

        self.display.fill('white')

        self.offset.x = self.player.rect.centerx - WIDTH // 2
        self.offset.y = self.player.rect.centery - HEIGHT // 2

        for sprite in self.visible_sprites:
            offset = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset)

        for sprite in self.enemies:
            offset = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset)
            sprite.hp_bar.draw(self.display, sprite.health, sprite.rect.midbottom - self.offset + (-25, 5))

        for sprite in self.npc:
            offset = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset)

        offset = self.player.rect.topleft - self.offset
        self.display.blit(self.player.image, offset)
        self.player.hp_bar.draw(self.display, self.player.health, self.player.rect.center - self.offset + (-25, 25))

        if not self.pause:
            self.player.update(self.offset, self.enemies, self.enemy_bullet, self.global_ticks - self.delta_ticks)
            self.enemies.update(self.offset, self.player, self.bullets, self.global_ticks - self.delta_ticks)
            self.npc.update(self.offset)
            self.bullets.update(self.offset)
            self.enemy_bullet.update(self.offset)

    @staticmethod
    def clear_sprites(groups):
        for group in groups:
            for sprite in group:
                sprite.kill()

    def restart(self):
        self.clear_sprites((self.enemies, self.bullets, self.enemy_bullet, self.npc))

        self.player = Player((), (50, 50), self.abilities_for_player, self.obstacle_sprite)

        Sceleton((self.enemies,),
                 (500, 50),
                             self.all_abilities.get_abilities(['bullet']),
                             self.obstacle_sprite)
        FireElemental((self.enemies,),
                      (500, 420),
                                  self.all_abilities.get_abilities(['fireball', 'bullet', 'frostbolt']),
                                  self.obstacle_sprite)
        Peasant((self.npc,), (100, 100), self.player)

    def draw(self):
        self.camera()
        self.hotkeys.update(self.display, self.player.cooldown.cant_use)

        if self.pause:
            instruction = self.pause_menu.update()
            if instruction == 1:
                self.running = False
            elif instruction == 2:
                self.restart()
                self.pause = False

        if self.player.is_dead():
            self.pause = True

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
                            self.player.convert_abilities()
                    if event.key == pg.K_ESCAPE:
                        self.pause = not self.pause


game = Game()
game.run()
