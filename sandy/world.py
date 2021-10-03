import numpy as np

NOTHING = [0, 0, 0]
is_nothing = lambda x: list(x) == NOTHING

SAND = [255, 255, 204]
is_sand = lambda x: list(x) == SAND

class World():
    def __init__(self, width, height, gravity):
        self.width, self.height, self.gravity = width, height, gravity
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

    def get_num_awake(self):
        return len(self.awake)

    def find_nearest_vertical_empty_cell(self, x, y, range):
        for i in range:
            if y + i < self.height and is_nothing(self.array[x][y + i]):
                return x, y + i
        return x, y

    def tick(self):
        for i in range(self.gravity):
            self.single_tick()

    def single_tick(self):
        old_awake = self.awake
        self.awake = []

        for cell in old_awake:
            x, y = cell
            if is_sand(self.array[x][y]):
                if y + 1 < self.height:
                    if y - 1 > 0: self.awake += [[x, y - 1]]
                    
                    if is_nothing(self.array[x][y + 1]): 
                        self.set_cell(x, y + 1, SAND)
                        self.set_cell(x, y, NOTHING)
                    elif x + 1 < self.width and is_nothing(self.array[x + 1][y + 1]): 
                        self.set_cell(x + 1, y + 1, SAND)
                        self.set_cell(x, y, NOTHING)
                    elif x - 1 >= 0 and is_nothing(self.array[x - 1][y + 1]): 
                        self.set_cell(x - 1, y + 1, SAND)
                        self.set_cell(x, y, NOTHING)
                # new_x, new_y = self.find_nearest_vertical_empty_cell(x, y, range(self.gravity, 0, -1))
                # if not new_y == y:
                #     self.set_cell(new_x, new_y, SAND)
                #     self.set_cell(x, y, NOTHING)

                #     if y - 1 > 0: self.awake += [[x, y - 1]]

    


