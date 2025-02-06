import pygame as pg
from copy import deepcopy


class Bars:
    def __init__(self, width, height, color, max_value):
        self.width = width
        self.height = height
        self.max = max_value
        self.color = color

    def draw(self, display, current, pos):
        ratio = current / self.max
        current_width = self.width * ratio

        pg.draw.rect(display, 'black', (pos[0], pos[1], self.width, self.height))
        pg.draw.rect(display, self.color, (pos[0], pos[1], current_width, self.height))

    def set_max_value(self, value):
        self.max = value


class HotKeys:
    def __init__(self, abilities):
        self.abilities = abilities

        self.pos = [40, 10]
        self.side_size = 32
        self.font = pg.font.Font('joystix.ttf', 10)
        self.rects = []
        self.images = []
        self.key_names = []
        self.load_images()

        self.lock_image = pg.image.load('sprite/lock.png').convert_alpha()
        self.unlock_image = pg.image.load('sprite/unlock.png').convert_alpha()
        self.rect = self.lock_image.get_rect(topleft=(5, 10))
        self.lock = True

        self.change_locker_state_timer_start = None
        self.can_change_locker_state = True
        self.change_locker_state_time = 200

        self.base_busy_keys = [119, 115, 97, 100, 27]
        busy_keys = [self.abilities[i]['key'] for i in self.abilities]
        self.busy_keys = self.base_busy_keys + busy_keys

        """
        Важно. 
        Вероятно нужно будет при добавлении/изменении/удалении спела на панели абилок 
        каждый раз обновлять все ректы/картинки через self.load_images()
        А также отдать self.player новые ректы через self.get_rects()
        """

    def draw_locker(self, display):
        pg.draw.rect(display, (100, 100, 100), self.rect)
        image = self.lock_image if self.lock else self.unlock_image
        display.blit(image, self.rect)

    def change_locker_state(self):
        if self.lock:
            self.lock = False
        else:
            self.lock = True

    def load_images(self):
        pos = deepcopy(self.pos)

        for ability in self.abilities:
            rect = pg.Rect((pos[0], pos[1], self.side_size, self.side_size))
            self.rects.append(rect)

            image = pg.image.load(self.abilities[ability]['sprite']).convert_alpha()
            image = pg.transform.scale(image, (32, 32))
            self.images.append(image)

            key_name = pg.key.name(self.abilities[ability]['key'])
            key_name = key_name.replace('eft', '').replace('ight', '')[:3]
            text = self.font.render(key_name, 0, 'white')
            self.key_names.append(text)

            pos[0] += 35

    def load_key_names(self, abilities):
        self.key_names = []
        for ability in abilities:
            key_name = pg.key.name(abilities[ability]['key'])
            key_name = key_name.lower().replace('eft', '').replace('ight', '')[:3]
            text = self.font.render(key_name, 0, 'white')
            self.key_names.append(text)

    def set_pressed_key(self, rect_id, key_id):
        ability_names = list(self.abilities.keys())
        self.abilities[ability_names[rect_id]]['key'] = key_id

        self.load_key_names(self.abilities)

        busy_keys = [self.abilities[i]['key'] for i in self.abilities]
        self.busy_keys = self.base_busy_keys + busy_keys

    def check_hotkeys_bar_collide_mouse(self):
        mouse_pos = pg.mouse.get_pos()

        if pg.mouse.get_pressed()[0]:
            if self.can_change_locker_state and self.rect.collidepoint(mouse_pos):
                self.change_locker_state()
                self.change_locker_state_timer_start = pg.time.get_ticks()
                self.can_change_locker_state = False

        for i, rect in enumerate(self.rects):
            if rect.collidepoint(mouse_pos):
                return i
        return -1

    def timers(self):
        current_time = pg.time.get_ticks()

        if not self.can_change_locker_state:
            if current_time > self.change_locker_state_time + self.change_locker_state_timer_start:
                self.can_change_locker_state = True

    def display_cooldown(self, pos, cooldown, display):
        if cooldown >= 1000:
            cooldown = str(cooldown // 1000)
        else:
            cooldown = str((cooldown // 100) / 10)[1:]
        text = self.font.render(cooldown, 0, 'white', 'black')
        rect = text.get_rect(midbottom=pos)
        display.blit(text, rect)

    def update(self, display, cooldown):
        self.check_hotkeys_bar_collide_mouse()
        self.draw_locker(display)
        self.timers()

        for index, ability in enumerate(self.abilities):
            rect = self.rects[index]
            pg.draw.rect(display, (100, 100, 100), rect)
            display.blit(self.images[index], rect)
            display.blit(self.key_names[index], rect)
            time_remain = cooldown.get(ability, {"time_remain": 0})["time_remain"]
            if time_remain:
                self.display_cooldown(rect.midbottom, time_remain, display)


class Button:
    def __init__(self, width, height, text, pos):
        self.display = pg.display.get_surface()

        self.width = width
        self.height = height
        self.text = text
        self.pos = pos

        self.font = pg.font.Font('joystix.ttf', 12)
        self.rect = pg.Rect(*pos, self.width, self.height)
        self.color = (50, 50, 50)

        self.button_pressed = False

    def draw(self):
        text = self.font.render(self.text, 0, 'white')
        rect = text.get_rect(center=self.rect.center)

        pg.draw.rect(self.display, self.color, self.rect)
        self.display.blit(text, rect)

    def check_mouse_collision(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True
        return False

    def button_pressed_and_released(self):
        if self.check_mouse_collision() and pg.mouse.get_pressed()[0]:
            self.button_pressed = True

        if self.button_pressed and not pg.mouse.get_pressed()[0]:
            self.button_pressed = False
            return True
        return False

    def update(self):
        self.draw()
        return self.button_pressed_and_released()



