import pygame as pg


class AnimatePlayer:
    def __init__(self, player):
        self.player = player

        self.sprites = {
            'idle': {
                'up': [], 'down': [], 'left': [], 'right': []
            },
            'move': {
                'up': [], 'down': [], 'left': [], 'right': []
            }
        }
        self.load_images()

        self.sprite_index = 0
        self.animation_speed = .15
        self.animation_index = 0

    def load_images(self):
        idle_up = pg.image.load('./sprite/player/idle/up/up.png').convert_alpha()
        idle_down = pg.image.load('./sprite/player/idle/down/down.png').convert_alpha()
        idle_left = pg.image.load('./sprite/player/idle/left/left.png').convert_alpha()
        idle_right = pg.image.load('./sprite/player/idle/right/right.png').convert_alpha()

        move_up_0 = pg.image.load('./sprite/player/move/up/up_0.png').convert_alpha()
        move_up_1 = pg.image.load('./sprite/player/move/up/up_1.png').convert_alpha()
        move_down_0 = pg.image.load('./sprite/player/move/down/down_0.png').convert_alpha()
        move_down_1 = pg.image.load('./sprite/player/move/down/down_1.png').convert_alpha()
        move_left_0 = pg.image.load('./sprite/player/move/left/left_0.png').convert_alpha()
        move_left_1 = pg.image.load('./sprite/player/move/left/left_1.png').convert_alpha()
        move_right_0 = pg.image.load('./sprite/player/move/right/right_0.png').convert_alpha()
        move_right_1 = pg.image.load('./sprite/player/move/right/right_1.png').convert_alpha()

        self.sprites['idle']['up'] = [idle_up]
        self.sprites['idle']['down'] = [idle_down]
        self.sprites['idle']['left'] = [idle_left]
        self.sprites['idle']['right'] = [idle_right]

        self.sprites['move']['up'] = [move_up_0, move_up_1]
        self.sprites['move']['down'] = [move_down_0, move_down_1]
        self.sprites['move']['left'] = [move_left_0, move_left_1]
        self.sprites['move']['right'] = [move_right_0, move_right_1]

    def processing(self):
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.sprites[self.player.status][self.player.direction]):
            self.animation_index = 0

        self.sprite_index = int(self.animation_index)

    def update(self):
        self.processing()
        self.player.image = self.sprites[self.player.status][self.player.direction][self.sprite_index]
