import timeit
import time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class TowerSolver(QObject):
    output = pyqtSignal(list)

    def __init__(self, parent=None):
        super(TowerSolver, self).__init__(parent)

        self.board = [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]]

        self.counter = 0
        self.start = 0
        self.visualization = False

    # if checked, show solution step by step
    def visualize(self, b):
        self.visualization = b.isChecked()

    # start backtracking recursion
    @pyqtSlot()
    def initialize(self):
        self.start = timeit.default_timer()
        if self.solve():
            print("Completed in ", timeit.default_timer() - self.start, "seconds and", self.counter, "guesses")
        else:
            print("Could not find a solution")
        self.output.emit(self.board)
        self.thread().finished.emit()

    def change_board_value(self, pos, value):
        self.board[pos[0]][pos[1]] = value

    def reset_board(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]]
        self.counter = 0

    def get_board(self):
        return self.board

    # get an empty slot from the board
    def get_empty(self):
        for row in range(1, 6):
            for col in range(1, 6):
                if self.board[row][col] == 0:
                    return row, col
        return None

    # check position validity for given tower
    def valid(self, tower, pos):
        # check col and row for another tower with same height
        for row in range(1, 6):
            if self.board[row][pos[1]] == tower:
                return False
        for col in range(1, 6):
            if self.board[pos[0]][col] == tower:
                return False

        # get limits for how many tower you can see from each direction
        left_limit = self.board[pos[0]][0]
        right_limit = self.board[pos[0]][6]
        upper_limit = self.board[0][pos[1]]
        bottom_limit = self.board[6][pos[1]]

        # check left limit
        highest = 0
        left = 0
        for i in range(1, 6):
            if i == pos[1] and tower >= highest:
                highest = tower
                left += 1

            elif self.board[pos[0]][i] > highest:
                highest = self.board[pos[0]][i]
                left += 1

        if left > left_limit:
            return False

        # check right limit if we are at the right edge
        highest = 0
        right = 0
        if pos[1] == 5:
            for i in range(5, 0, -1):

                if i == pos[1] and tower > highest:
                    highest = tower
                    right += 1

                elif self.board[pos[0]][i] > highest:
                    highest = self.board[pos[0]][i]
                    right += 1

            if right != right_limit:
                return False

        # check upper limit
        upper = 0
        highest = 0
        for i in range(1, 6):
            if i == pos[0] and tower > highest:
                highest = tower
                upper += 1

            elif self.board[i][pos[1]] > highest:
                highest = self.board[i][pos[1]]
                upper += 1

        if upper > upper_limit:
            return False

        # check bottom limit if we are at bottom row
        bottom = 0
        highest = 0

        if pos[0] == 5:
            for i in range(5, 0, -1):
                if i == pos[0] and tower > highest:
                    highest = tower
                    bottom += 1

                elif self.board[i][pos[1]] > highest:
                    highest = self.board[i][pos[1]]
                    bottom += 1

            if bottom != bottom_limit:
                return False

        return True

    def solve(self):
        pos = self.get_empty()
        # if all slots are filled, puzzle is completed
        if not pos:
            return True

        else:
            for guess in range(1, 6):
                if self.valid(guess, pos):
                    self.board[pos[0]][pos[1]] = guess
                    self.counter += 1
                    # if visualization is on, update board after every guess
                    if self.visualization:
                        time.sleep(0.15)
                        self.output.emit(self.board)
                    # backtracking algorithm by recursion
                    if self.solve():
                        return True
                    self.board[pos[0]][pos[1]] = 0
            return False


# text based version
# to get results, you must modify self.board to represent an unsolved tower puzzle
def main():
    solver = TowerSolver()
    board = solver.get_board()
    print('Tower puzzle to solve:')

    for line in board:
        print(line, '\n')

    print('------------------------------')
    solver.start = timeit.default_timer()

    solver.solve()

    print('Solved in: ', timeit.default_timer()-solver.start, 'seconds')

    for line in board:
        print(line, '\n')


if __name__ == "__main__":
    main()









