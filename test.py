import pygame as pg
from copy import copy

pg.init()

display = pg.display.set_mode((500, 500))
clock = pg.time.Clock()

surf = pg.image.load('sprite/enemy.png').convert_alpha()
frenzied = pg.image.load('sprite/frenzied.png').convert_alpha()
frenzied.set_alpha(150)
image = copy(surf)
rect = image.get_rect(center=(250, 250))
mask = pg.Surface((32, 32))
color = (0, 255, 255)
mask.fill(color)
image.blit(mask, (0, 0), special_flags=pg.BLEND_MULT)



running = True
while running:
    display.fill('white')

    display.blit(image, rect)
    display.blit(mask, (0, 0))
    rect.x += 1
    pg.display.update()
    clock.tick(20)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_e:
                image = copy(surf)
            if event.key == pg.K_r:
                image.blit(frenzied, (0, 0))

