import numpy as np
import random as random

NOTHING = 0
BORDER = 1
SAND = 2
WATER = 3
STONE = 4

MATERIALS = {
    NOTHING: np.asarray([0, 0, 0]),
    BORDER: np.asarray([1, 1, 1]),
    SAND: np.asarray([255, 255, 204]),
    WATER: np.asarray([28, 163, 236]),
    STONE: np.asarray([145, 142, 133])
}

class World():
    def __init__(self, surface, width, height, tick_speed):
        self.surface, self.width, self.height, self.tick_speed = surface, width, height, tick_speed

        self.array = np.zeros((width, height), dtype='u1')
        self.awake = []

        for y in range(height): 
            self.set_cell(0, y, BORDER)
            self.set_cell(width - 1, y, BORDER)
        for x in range(width):
            self.set_cell(x, 0, BORDER)
            self.set_cell(x, height - 1, BORDER)

    def set_cell(self, x, y, cell):
        # assert is_nothing(cell) or is_sand(cell) or is_water(cell) or is_border(cell) or is_stone(cell)
        assert type(x) == int and type(y) == int

        if not self.in_bounds(x, y): return None

        material = self.array[x,y]
        if material == BORDER or (material == STONE and not cell == NOTHING): return None

        self.array[x,y] = cell
        self.set_awake(x, y)

        # if (is_stone(cell)):
        #     width, height = self.surface.get_size()
        #     scale = width // np.shape(self.array)[0] or 1
        #     paint_coords_to_surface(self.awake, self.surface, scale, lambda x, y: self.array[x][y])

    def swap_cell(self, x1, y1, x2, y2):
        cell2 = np.copy(self.array[x2,y2])
        self.set_cell(x2, y2, self.array[x1,y1])
        self.set_cell(x1, y1, cell2)

    def set_cells(self, cur_x, cur_y, del_x, del_y, cell, brush_size):
        def draw_brush(x, y):
            for x_ in range(x - brush_size, x + brush_size):
                for y_ in range(y - brush_size, y + brush_size):
                    self.set_cell(x_, y_, cell)
        line_alg(cur_x, cur_y, del_x, del_y, draw_brush)

    def in_bounds(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def set_awake(self, x, y):
        coords = [x, y]
        if not coords in self.awake and self.in_bounds(x, y): self.awake += [coords]

    def get_surface(self):
        return self.surface

    def get_num_awake(self):
        return len(self.awake)

    def tick(self):
        for i in range(self.tick_speed):
            width, height = self.surface.get_size()

            scale = width // np.shape(self.array)[0] or 1

            # offset = 25

            # def noise(mat):
            #     return [i - offset + int(offset * random.random()) if i > offset else i for i in mat]

            paint_coords_to_surface(self.awake, self.surface, scale, lambda x, y: MATERIALS[self.array[x,y]])

            self.single_tick()


    def single_tick(self):
        cells_to_update = np.copy(self.awake).tolist()

        self.awake = []

        seed = len(cells_to_update)

        cells_to_update.sort(key=lambda v: v[1], reverse=True)

        for cell in cells_to_update:
            x, y = cell
            left = 1 if (x + y + seed) % 2 == 0 else -1

            def check_and_swap(cond, *deltas):
                for delta in deltas:
                    dx, dy = delta
                    dx *= left
                    if cond(self.array[x + dx,y + dy]):
                        self.swap_cell(x, y, x + dx, y + dy)
                        for delta in deltas:
                            dx, dy = delta
                            self.set_awake(x - dx, y - dy)
                        return True

            if self.array[x,y] == SAND:
                check_and_swap(lambda x: x == NOTHING or x == WATER, (0, 1), (1, 1), (-1, 1))                      

            if self.array[x,y] == WATER and y + 2 < self.height:
                check_and_swap(lambda x: x == NOTHING, (0, 1), (1, 1), (-1, 1), (1, 0), (-1, 0))

def paint_coords_to_surface(coords, surface, scale, color):
    for coord in coords:
        x, y = coord
        for dx in range(scale):
            for dy in range(scale):
                surface.set_at((scale * x + dx, scale * y + dy), color(x, y))    
            

def line_alg(cur_x, cur_y, del_x, del_y, f):
        distance = del_x ** 2 + del_y ** 2
        distance = 100 // distance if distance else 1
        step = int(distance or 1)
        for i in range(0, 100, step):
            x = cur_x - (i / 100) * del_x
            y = cur_y - (i / 100) * del_y
            x, y = int(x), int(y)
            f(x, y)

                



    


