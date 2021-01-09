from selenium import webdriver
from pyautogui import press
import numpy as np

from solver import Solver


class WebSolver:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.grid = self.cells = None

    def start(self, difficult=None):
        if difficult not in ['easy', 'medium', 'hard', 'expert']:
            difficult = 'hard'
        self.driver.get(f'https://sudoku.com/{difficult}/')
        self.driver.implicitly_wait(20)

        self.init_grid()
        solved, self.grid = Solver(self.grid).solve()
        print(solved)
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
        for i in range(9):
            for j in range(9):
                self.cells[i*9 + j].click()
                press(str(self.grid[i, j]))


if __name__ == '__main__':
    WebSolver().start()
