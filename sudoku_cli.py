from .board import Board


class SudokuCLI:
    def __init__(self, mode='computer'):
        self.board = Board()

    def mainloop(self):
        while True:
            print(self.board_to_str())

            cmd = input(': ').lower()

            if cmd == '/help':
                print('help')
            elif cmd.startswith('/save'):
                self.board.save(cmd.split(' ')[1])
            elif cmd.startswith('/load'):
                self.board.load(cmd.split(' ')[1])
            elif cmd == '/tip':
                print('TODO: tip')
            elif cmd == '/check':
                if self.board.check():
                    self._game_over()
                else:
                    print('Nope')
            elif len(cmd) == 4 and cmd[0] in 'abcdefgkl' and cmd[1] in '123456789' and cmd[3] in '123456789':
                row = int(cmd[1]) - 1
                column = 'abcdefgkl'.index(cmd[0])
                digit = int(cmd[3])
                self.board.move(row, column, digit)
            else:
                print('bad input')

    def print_board(self):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print('- - - - - - - - - - - - - ')

            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print(' | ', end='')

                if j == 8:
                    print(self.board[i, j])
                else:
                    print(self.board[i, j], end=' ')



