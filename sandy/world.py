import numpy as np

NOTHING = (0, 0, 0)
is_nothing = lambda x: x == NOTHING

SAND = (255, 255, 255)
is_sand = lambda x: x == SAND

class World():
    def __init__(self, width, height):
        self.array = np.zeros((width, height, 3))
        self.awake = []

    def set_cell(self, x, y, cell):
        assert is_nothing(cell) or is_sand(cell)
        assert type(x) == int and type(y) == int

        self.array[x][y] = cell
        self.awake += [[x, y]]

    def set_cells(self, cur_x, cur_y, del_x, del_y, cell):
        distance = del_x ** 2 + del_y ** 2
        for i in range(0, 100, 1 if not distance else (100 // distance or 1)):
            x = cur_x - (i / 100) * del_x
            y = cur_y - (i / 100) * del_y
            x, y = int(x), int(y)
            self.set_cell(x, y, cell)

    def get_rgbs(self):
        return self.array

    def tick(self):
        pass