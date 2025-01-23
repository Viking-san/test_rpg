from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from config import *


class Pathfinder:
    def __init__(self, seeker, goal, offset):
        self.offset = offset
        self.matrix = []
        self.make_matrix()
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.grid = Grid(matrix=self.matrix)
        self.path = []

        self.display = pg.display.get_surface()

        self.set_points(seeker, goal)

    def set_points(self, seeker, goal):
        start = seeker.rect.center
        start = self.grid.node(start[0] // TILE_SIZE, start[1] // TILE_SIZE)

        end = goal.rect.center
        end = self.grid.node(end[0] // TILE_SIZE, end[1] // TILE_SIZE)

        self.path, _ = self.finder.find_path(start, end, self.grid)
        # print(self.path)
        lines = []
        for line in self.path:
            coord_x = line.x * 32 + 16 - self.offset.x
            coord_y = line.y * 32 + 16 - self.offset.y
            lines.append((coord_x, coord_y))
        pg.draw.lines(self.display, 'black', False, lines, 2)

    def make_matrix(self):
        for i, row in enumerate(MAP):
            self.matrix.append([])
            for col in row:
                if col == 'w':
                    self.matrix[i].append(0)
                else:
                    self.matrix[i].append(1)
