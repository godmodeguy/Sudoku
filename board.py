from random import choice, randint
import numpy as np
import pickle


class Board:
    def __init__(self, n_drop=30, one_solution=False):
        self.grid = None
        self.n_drop = n_drop
        self.one_solution = one_solution

        self._create_grid()
        self.filled_grid = self.grid.copy()
        self._create_sudoku()

    def _create_grid(self):
        self.grid = np.array([
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [2, 3, 4, 5, 6, 7, 8, 9, 1],
            [5, 6, 7, 8, 9, 1, 2, 3, 4],
            [8, 9, 1, 2, 3, 4, 5, 6, 7],
            [3, 4, 5, 6, 7, 8, 9, 1, 2],
            [6, 7, 8, 9, 1, 2, 3, 4, 5],
            [9, 1, 2, 3, 4, 5, 6, 7, 8],
        ])
        ops = [
            self._transpose_grid,
            self._row_swap,
            self._triple_row_swap,
            # self._column_swap,
            # self._area_column_swap
        ]
        for _ in range(10000):
            choice(ops)()

    def _transpose_grid(self):
        self.grid = self.grid.T

    def _row_swap(self):
        area = choice((0, 1, 2))
        row1 = choice((0, 1, 2)) + area * 3
        row2 = choice((0, 1, 2)) + area * 3

        self.grid[[row1, row2]] = self.grid[[row2, row1]]

    def _triple_row_swap(self):
        area1 = choice(([0, 1, 2], [3, 4, 5], [6, 7, 8]))
        area2 = choice(([0, 1, 2], [3, 4, 5], [6, 7, 8]))
        self.grid[area1], self.grid[area2] = self.grid[area2], self.grid[area1]

    # def _column_swap(self):
    #     area = choice((0, 1, 2))
    #     column1 = choice((0, 1, 2)) + area * 3
    #     column2 = choice((0, 1, 2)) + area * 3
    #
    #     self.grid[:, [column1, column2]] = self.grid[:, [column2, column1]]
    #
    # def _area_row_swap(self):
    #     area1 = choice(([0, 1, 2], [3, 4, 5], [6, 7, 8]))
    #     area2 = choice(([0, 1, 2], [3, 4, 5], [6, 7, 8]))
    #     self.grid[area1], self.grid[area2] = self.grid[area2], self.grid[area1]
    #
    # def _area_column_swap(self):
    #     area1 = choice(([0, 1, 2], [3, 4, 5], [6, 7, 8]))
    #     area2 = choice(([0, 1, 2], [3, 4, 5], [6, 7, 8]))
    #     self.grid[:, area1], self.grid[:, area2] = self.grid[:, area2], self.grid[:, area1]

    def _create_sudoku(self):
        while True:
            grid = self.grid.copy()
            n = self.n_drop
            while n:
                i, j = randint(0, 8), randint(0, 8)
                if grid[i, j]:
                    grid[i, j] = 0
                    n -= 1
            if self.one_solution:
                pass
                # solutions = Solver.solve()
                #       if len(solutions) != 1:
                #             continue
            self.grid = grid
            break

    @staticmethod
    def check_grid(grid):
        for i in range(9):
            if len(set(grid[i, :])) != 9 or len(set(grid[:, i])) != 9:
                return False

        # for bi in (0, 1, 2):
        #     box = {}
        #     for by in (0, 1, 2):
        #         box += grid[]
        #         grid[t1, [t2, t2 + 1, t2 + 2]],
        #         tb[t1 + 1, [t2, t2 + 1, t2 + 2]],
        #         tb[t1 + 2, [t2, t2 + 1, t2 + 2]]
        return True


    def check(self):
        return self.check_grid(self.grid)

    def save(self, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump((self.grid, self.filled_grid), f)
            return 1
        except:
            return -1

    def load(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.grid, self.filled_grid = pickle.load(f)
            return True
        except:
            return -1

    def __repr__(self):
        return str(self.grid)
