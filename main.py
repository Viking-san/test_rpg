import pygame as pg
from config import *
from player import Player
from enemy import *
from tiles import *
from interface import *
# from spells import *
from ability_storage import AllAbilities
from npc import Peasant


class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Test RPG')

        self.display = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True

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

        abilities_for_player = ['create_bullet', 'create_fireball', 'create_frostbolt', 'flame_strike', 'blizzard']
        abilities_for_player = self.all_abilities.get_abilities(abilities_for_player)
        self.player = Player([], (50, 50), abilities_for_player, self.obstacle_sprite)
        self.hotkeys = HotKeys(abilities_for_player)

        self.offset = pg.math.Vector2()
        self.create_map()

    def create_map(self):
        for y, map_string in enumerate(MAP):
            for x, tile in enumerate(map_string):
                pos = (x * TILE_SIZE, y * TILE_SIZE)
                if tile == 'x':
                    Tile([self.visible_sprites], pos)
                elif tile == 'e':
                    Sceleton([ self.enemies], pos, self.all_abilities.get_abilities(['create_bullet']), self.obstacle_sprite)
                elif tile == 'f':
                    FireElemental([self.enemies], pos, self.all_abilities.get_abilities(['create_fireball']), self.obstacle_sprite)
                elif tile == 'w':
                    ObstacleTile([self.visible_sprites, self.obstacle_sprite], pos)
                elif tile == 'k':
                    Peasant([self.npc], pos, self.player)

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

        for sprite in self.npc:
            offset = sprite.rect.topleft - self.offset
            self.display.blit(sprite.image, offset)

        self.enemies.update(self.offset, self.player, self.bullets)

        offset = self.player.rect.topleft - self.offset
        self.display.blit(self.player.image, offset)
        self.player.hp_bar.draw(self.display, self.player.health, self.player.rect.center - self.offset + (-25, 25))
        self.player.update(self.offset, self.enemies, self.enemy_bullet)

        self.bullets.update(self.offset)
        self.enemy_bullet.update(self.offset)

        self.npc.update(self.offset)

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
                            self.player.convert_abilities()
                    if event.key == pg.K_ESCAPE:
                        self.running = False


game = Game()
game.run()
