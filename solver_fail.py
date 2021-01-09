import numpy as np
from collections import Counter
from board import Board


class Solver:
    def __init__(self):
        pass

    @staticmethod
    def solve(grid, search_for_all_solutions=False):
        table = np.array([[grid[j, i] or set(range(1, 10))
                           for i in range(9)] for j in range(9)])

        status, table = Solver._minimize_entropy(table)
        if status == -1:
            return -1, None
        elif status == 1:
            return 1, table
        else:
            solutions = Solver._bruteforce_dfs(table, not search_for_all_solutions)
            return len(solutions), solutions
    
    @staticmethod
    def _bruteforce_dfs(table, one_solution):
        solutions = []
        for i in range(9):
            for j in range(9):
                if isinstance(table[i, j], set):
                    candidates = table[i, j]
                    temp_tb = table.copy()
                    while candidates:
                        temp_tb[i, j] = candidates.pop()
                        sol = Solver._bruteforce_dfs(temp_tb, one_solution)
                        if sol:
                            solutions.extend(sol)
                    
        if solutions:
            return solutions
        elif Solver._check(table) == 1:
            return [table]
                    
                    

    @staticmethod
    def _minimize_entropy(table):
        used_digits = Counter(filter(lambda x: isinstance(x, int), table.flatten()))

        without_changes = 0
        while without_changes != 3:
            without_changes += 1

            to_remove = []
            for key, val in used_digits.items():
                if val == 9:
                    to_remove.append(key)
                    for i in range(9):
                        for j in range(9):
                            if isinstance(table[i, j], set):
                                table[i, j] -= {key}
            for k in to_remove:
                del used_digits[k]

            for i in range(9):
                for j in range(9):
                    if isinstance(table[i, j], set):
                        tb = np.array([[0 if isinstance(i, set) else i for i in j] for j in table])
                        unsuitable_digits, t1, t2 = set(), (i // 3) * 3, (j // 3) * 3
                        unsuitable_digits.update(
                            tb[i, :], tb[:, j],
                            tb[t1, [t2, t2 + 1, t2 + 2]],
                            tb[t1 + 1, [t2, t2 + 1, t2 + 2]],
                            tb[t1 + 2, [t2, t2 + 1, t2 + 2]]
                        )
                        table[i, j] -= unsuitable_digits

                        if len(table[i, j]) == 0:
                            return -1, None
                        if len(table[i, j]) == 1:
                            table[i, j] = table[i, j].pop()
                            used_digits[table[i, j]] += 1
                            without_changes = 0
        return Solver._check(table), table

    @staticmethod
    def _check(table):
        for i in range(9):
            for j in range(9):
                if isinstance(table[i, j], set):
                    return 0
        return 1
        for i in range(9):
            if len(set(table[:, i])) != 9:
                return -1
            if len(set(table[i, :])) != 9:
                return -1
            # if area
        return 1


class WebTest:
    def __init__(self):
        from selenium import webdriver

        self.driver = webdriver.Chrome()
        self.grid = self.cells = None

    def start(self, difficulty='easy'):
        if difficulty not in ['easy', 'medium', 'hard', 'expert']:
            difficulty = 'medium'
        self.driver.get(f'https://sudoku.com/{difficulty}/')
        self.driver.implicitly_wait(20)

        self.init_grid()

        # n_sol, solutions = Solver.solve(self.grid)
        # print(solutions.shape)
        # self.grid = solutions[0]

        self.enter()

        input()
        self.driver.quit()

    def init_grid(self):
        nums = {'M6.698 16.': 3, 'M.12 9.57C': 2, 'M15.855 30': 4, 'M10.553 30': 5,
                'M10.964 31': 6, 'M3.017 30L': 7, 'M10.533 31': 8, 'M10.897 31': 9}

        table = np.array([0] * 81)
        self.cells = self.driver.find_elements_by_tag_name('td')
        for i in range(len(self.cells)):
            if self.cells[i].get_attribute('class') == 'game-cell game-value':
                x = self.cells[i].find_element_by_tag_name('div')
                x = x.find_element_by_tag_name('svg')
                x = x.find_element_by_tag_name('path')
                attr = x.get_attribute('d')
                table[i] = nums.get(attr[:10], 0)
        self.grid = table.reshape((9, 9))

    def enter(self):
        from pyautogui import press

        i = 0
        for row in self.grid:
            for n in row:
                self.cells[i].click()
                press(str(n))
                i += 1


class BoardTest:
    def __init__(self):
        pass

    def start(self):
        for i in range(1):
            b = Board(n_drop=50)
            s = Solver.solve(b.grid, Board)
            print(s)


class Test:
    def __init__(self):
        pass


if __name__ == "__main__":
    BoardTest().start()
