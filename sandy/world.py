import numpy as np

check = lambda n: lambda x: list(x) == n

NOTHING = [0, 0, 0]
is_nothing = check(NOTHING)

BORDER = [255, 255, 255]
is_border = check(BORDER)

SAND = [255, 255, 204]
is_sand = check(SAND)

WATER = [28, 163, 236]
is_water = check(WATER)

class World():
    def __init__(self, surface, width, height):
        self.surface, self.width, self.height = surface, width, height

        world = np.zeros((width, height, 3))
        for y in range(height): 
            world[0][y] = BORDER
            world[width - 1][y] = BORDER
        for x in range(width):
            world[x][0] = BORDER
            world[x][height - 1] = BORDER

        self.array = world
        self.awake = []

    def set_cell(self, x, y, cell):
        assert is_nothing(cell) or is_sand(cell) or is_water(cell)
        assert type(x) == int and type(y) == int
        if is_border(self.array[x][y]) or not self.in_bounds(x, y): return None

        self.array[x][y] = cell
        self.set_awake(x, y)

    def swap_cell(self, x1, y1, x2, y2):
        cell2 = self.array[x2][y2].copy()
        self.set_cell(x2, y2, self.array[x1][y1])
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

    def get_rgbs(self):
        return self.array

    def get_num_awake(self):
        return len(self.awake)

    def tick(self):
        self.single_tick()
    
        for coord in self.awake:
            self.surface.set_at(coord, self.array[coord[0]][coord[1]])

    def single_tick(self):
        old_awake = self.awake
        self.awake = []

        for cell in old_awake:
            x, y = cell
            moved = False
            # left = 1 if x % 2 == 0 else -1

            def check_and_swap(dx, dy, f):
                # dx *= left
                #if self.in_bounds(x + dx, y + dy) and f(self.array[x + dx][y + dy]):
                if f(self.array[x + dx][y + dy]):
                    self.swap_cell(x, y, x + dx, y + dy)
                    return True
                return False

            if is_sand(self.array[x][y]):
                if y + 1 < self.height:
                    if check_and_swap(0, 1, lambda x: is_nothing(x) or is_water(x)): moved = True
                    elif check_and_swap(1, 1, lambda x: is_nothing(x) or is_water(x)): moved = True
                    elif check_and_swap(-1, 1, lambda x: is_nothing(x) or is_water(x)): moved = True

                    self.set_awake(x, y - 1)

            if is_water(self.array[x][y]):
                if y + 1 < self.height:
                    if check_and_swap(0, 1, lambda x: is_nothing(x)): moved = True
                    elif check_and_swap(1, 1, lambda x: is_nothing(x)): moved = True
                    elif check_and_swap(-1, 1, lambda x: is_nothing(x)): moved = True
                   # elif check_and_swap(2, 1, lambda x: is_nothing(x)): moved = True
                   # elif check_and_swap(2, 1, lambda x: is_nothing(x)): moved = True
                   # elif check_and_swap(3, 1, lambda x: is_nothing(x)): moved = True
                    #elif check_and_swap(-3, 1, lambda x: is_nothing(x)): moved = True
                if not moved:
                    if check_and_swap(1, 0, lambda x: is_nothing(x)): moved = True
                    elif check_and_swap(-1, 0, lambda x: is_nothing(x)): moved = True
                    #elif check_and_swap(2, 0, lambda x: is_nothing(x)): moved = True
                    #elif check_and_swap(-2, 0, lambda x: is_nothing(x)): moved = True
                if moved: 
                    self.set_awake(x, y - 1)
                    self.set_awake(x - 1, y)
                    self.set_awake(x + 1, y)

def line_alg(cur_x, cur_y, del_x, del_y, f):
        distance = del_x ** 2 + del_y ** 2
        for i in range(0, 100, 1 if not distance else (100 // distance or 1)):
            x = cur_x - (i / 100) * del_x
            y = cur_y - (i / 100) * del_y
            x, y = int(x), int(y)
            f(x, y)

                



    


