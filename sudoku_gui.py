import sys, os, random
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import askyesnocancel, askyesno, showerror
import pygame

from board import Board
from solver_fail import Solver


class SudokuGUI:
    def __init__(self):
        pygame.init()
        Tk().withdraw()

        self.screen = pygame.display.set_mode((900, 900))

        self.background = pygame.image.load("img/board.png")
        self.background_rect = self.background.get_rect()
        self.font = pygame.font.Font(None, 150)

        self.board = Board()
        self.mouse_pos = [0, 0]
        self.checking = False  # TODO: work for many solutions

    def mainloop(self):
        while True:
            self.checking = pygame.key.get_pressed()[pygame.K_SPACE]
            if self.checking and self.board.check():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit()
                    if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                        self.game_over()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.save_game()
                    elif event.key == pygame.K_l:
                        self.load_game()
                    elif event.key == pygame.K_h:
                        self.hint()

            self.mouse_handle()
            self.draw()

    def mouse_handle(self):
        x, y = pygame.mouse.get_pos()
        self.mouse_pos = int((x-15) / 95), int((y-15) / 95)

        if pygame.mouse.get_pressed()[0]:
            self.input()

    def hint(self):
        free = []
        for i in range(9):
            for j in range(9):
                if self.board.grid[i, j] == 0:
                    free.append([i, j])
        if free:
            i, j = random.choice(free)
            self.board.grid[i, j] = self.board.filled_grid[i, j]

    def input(self):
        x, y = self.mouse_pos

        cell = pygame.Surface((100, 100), pygame.SRCALPHA)
        cell.fill((40, 40, 40, 140))
        self.screen.blit(cell, (x*100, y*100))
        pygame.display.flip()

        mouse_btn_down = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_btn_down = True
                if event.type == pygame.MOUSEBUTTONUP and mouse_btn_down:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.board.grid[x, y] = 0
                    elif event.key in range(49, 58):
                        self.board.grid[x, y] = event.key - 48
                    return

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, self.background_rect)

        x, y = self.mouse_pos

        s_x = pygame.Surface((890, 102), pygame.SRCALPHA)
        s_x.fill((0, 0, 0, 100))
        self.screen.blit(s_x, (6, y*101 - 3*((y+1)//3)))

        s_y = pygame.Surface((102, 890), pygame.SRCALPHA)
        s_y.fill((0, 0, 0, 100))
        self.screen.blit(s_y, (x*101 - 3*((x+1)//3), 6))

        for i in range(9):
            for j in range(9):
                digit = self.board.grid[i, j]
                if digit != 0:
                    if self.checking:
                        color = (20, 200, 20) if digit == self.board.filled_grid[i, j] else (200, 20, 20)
                    else:
                        color = (20, 20, 20)

                    text = self.font.render(str(digit), True, color)
                    self.screen.blit(text, (23 + i*100, 5 + j*100))

        pygame.display.flip()

    def save_game(self):
        filename = asksaveasfilename(defaultextension='.pkl', initialdir=os.getcwd())
        if filename:
            status = self.board.save(filename)
            if status == -1:
                showerror('Error', 'Error to save game')

    def load_game(self):
        filename = askopenfilename(defaultextension='.pkl', initialdir=os.getcwd())
        if filename:
            status = self.board.load(filename)
            if status == -1:
                showerror('Error', 'Error to load game')

    def exit(self):
        ans = askyesnocancel('Exit Application', 'Do you want to save game?', icon='warning')
        if ans is None:
            return
        if ans:
            self.save_game()
        sys.exit()

    def game_over(self):
        ans = askyesno('Game Over', 'Sudoku solved!\nRestart?')
        if ans:
            self.board = Board()
            self.mainloop()
        else:
            sys.exit()


if __name__ == "__main__":
    SudokuGUI().mainloop()
