from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from config import *
import pygame as pg


class Pathfinder:
    def __init__(self):
        self.display = pg.display.get_surface()

        self.matrix = []
        self.make_matrix()
        # self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.finder = AStarFinder()
        self.grid = Grid(matrix=self.matrix)

        self.start = None
        self.end = None
        self.path = []
        self.path_rects = []

    def set_points(self, seeker, goal):
        start = seeker.rect.center
        self.start = self.grid.node(start[0] // TILE_SIZE, start[1] // TILE_SIZE)

        end = goal.rect.center
        self.end = self.grid.node(end[0] // TILE_SIZE, end[1] // TILE_SIZE)

    def get_path_rects(self):
        self.path, _ = self.finder.find_path(self.start, self.end, self.grid)

        self.path_rects = []
        for i, point in enumerate(self.path):
            if i > 1:
                break
            x = point.x * 32 + 13
            y = point.y * 32 + 13
            rect = pg.Rect((x, y, 6, 6))
            self.path_rects.append(rect)

    def make_matrix(self):
        for i, row in enumerate(MAP):
            self.matrix.append([])
            for col in row:
                if col == 'w':
                    self.matrix[i].append(0)
                else:
                    self.matrix[i].append(1)

    def draw_path(self, offset):
        for rect in self.path_rects:
            pos = rect.center - offset
            pg.draw.rect(self.display, 'black', (pos, rect.size))

    def go_find(self, seeker, goal):
        if not seeker.pathfinder_control:
            self.set_points(seeker, goal)
            self.get_path_rects()
            seeker.pathfinder_control = True

    def collision_check(self, seeker):
        point = self.path_rects[0]
        if point.collidepoint(seeker.rect.center):
            self.path_rects.pop(0)

    def dot_chaser(self, seeker):
        point = self.path_rects[0]
        start = pg.math.Vector2(seeker.rect.center)
        end = pg.math.Vector2(point.center)

        vector = end - start
        if vector:
            seeker.vector = vector.normalize()

        seeker.moving()
        self.collision_check(seeker)

    def update(self, seeker, offset):
        # self.draw_path(offset)
        if self.path_rects:
            self.dot_chaser(seeker)
        else:
            seeker.pathfinder_control = False




