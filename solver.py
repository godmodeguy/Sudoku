import numpy as np
from board import Board


class Solver:
    def __init__(self, grid, algorithm=None, find_all_solutions=False):
        self.grid = np.array(grid)
        self.find_all_solutions = find_all_solutions
        self.solve_fn = {
            'backtracking': self.backtracking,
        }.get(algorithm, self.backtracking)

    def solve(self):
        solved = self.solve_fn()
        return Board.check_grid(self.grid), self.grid

    def backtracking(self):
        find = self._find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self._valid(i, (row, col)):
                self.grid[row][col] = i

                if self.backtracking():
                    return True

                self.grid[row][col] = 0

        return False

    def _valid(self, num, pos):
        bo = self.grid

        # Check row
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(bo)):
            if bo[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if bo[i][j] == num and (i, j) != pos:
                    return False

        return True

    def _find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] == 0:
                    return [i, j]


def test():
    from board import Board

    for _ in range(1):
        b = Board(70)
        s = Solver(b.grid).solve()
        print(b.grid)
        print(s[1])

if __name__ == '__main__':
    test()
