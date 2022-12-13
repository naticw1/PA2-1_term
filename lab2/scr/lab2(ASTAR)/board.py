from typing import Literal, Optional
from Logger import NQLogger
from random import randint
import pickle


class Board:
    def __init__(self, queens: Optional[int] = None, other=None) -> None:
        self.size: int
        self.matrix: list[list[Literal[0, 1]]]

        if other:

            # debug board that was generated
            if isinstance(other, Board):
                self.size = other.size
                self.matrix = pickle.loads(pickle.dumps(other.matrix, -1))

            elif isinstance(other, list):
                self.size = len(other)
                self.matrix = other

        # create empty board

        else:

            # default value is 4( if only necessary to look at if it is working)
            self.size = queens or 4

            # create board in the form of matrix)
            self.matrix = [[0 for i in range(self.size)] for j in range(self.size)]

        self.conf = self.conflict_number()

    # Generate board with random place for Queen in row
    def generate_board(self):
        for i in range(self.size):
            j = randint(0, self.size - 1)
            self.matrix[i][j] = 1

    # Get number of conflict
    def conflict_number(self):
        conflicts = 0

        for i in range(self.size):
            for j in range(self.size):

                if self.matrix[i][j] == 1:
                    conflicts += self.get_conflict(i, j)

        return conflicts

    def correct_index(self, i, j):
        return i >= 0 and i < self.size and j >= 0 and j < self.size

    def get_conflict(self, i, j):
        conf_n = 0

        # Horizontal conflict:
        # 1. Before Q
        for col in range(j):
            count = 0
            if self.matrix[i][col] == 1:
                count += 1

            if count:
                conf_n += count
                break

        # Horizontal conflict:
        # 2. After Q
        for col in range(j + 1, self.size):
            count = 0
            if self.matrix[i][col] == 1:
                count += 1

            if count:
                conf_n += count
                break

        # Vertical conflict:
        # 1.Before Q
        for row in range(i):
            count = 0
            if self.matrix[row][j] == 1:
                count += 1

            if count:
                conf_n += count
                break

        # Vertical conflict:
        # 2. After Q
        for row in range(i + 1, self.size):
            count = 0
            if self.matrix[row][j] == 1:
                count += 1

            if count:
                conf_n += count
                break

        row = i - 1
        col = j - 1

        # Diagonal conflict:
        # 1.Before Q
        while self.correct_index(row, col):
            if self.matrix[row][col] == 1:
                conf_n += 1
                break

            row -= 1
            col -= 1

        row = i + 1
        col = j + 1

        # Diagonal conflict:
        # 2.After diagonal
        while self.correct_index(row, col):
            if self.matrix[row][col] == 1:
                conf_n += 1
                break

            row += 1
            col += 1

        row = i - 1
        col = j + 1

        # Anti-Diagonal conflict:
        # 1.Before Q
        while self.correct_index(row, col):
            if self.matrix[row][col] == 1:
                conf_n += 1
                break

            row -= 1
            col += 1

        row = i + 1
        col = j - 1

        # Anti-Diagonal conflict:
        # 2.After Q
        while self.correct_index(row, col):
            if self.matrix[row][col] == 1:
                conf_n += 1
                break

            row += 1
            col -= 1

        return conf_n

    def move_figure(self, row: int, shift: int):
        # for logging
        new_row = 0
        new_col = 0
        last_j = 0

        for j in range(self.size):
            if self.matrix[row][j] == 1:
                self.matrix[row][j] = 0

                col = j + shift
                if col >= self.size:
                    col -= self.size

                self.matrix[row][col] = 1

                # for logging
                [new_row, new_col, last_j] = [row, col, j]
                break

        self.conf = self.conflict_number()

        # log the move
        NQLogger.info(f"Move Q: ({row},{last_j}) -> ({new_row},{new_col})  ::  {self.conf} conflicts after moving")

    # for board printing
    def print(self, pre: str | None = None, end: str | None = '\n') -> None:
        if pre:
            print(pre)

        def print_black_cell(q: Literal['Q', ' ']) -> None:
            print(f"\033[100m \033[97m{q} \033[0m", end="")

        def print_white_cell(q: Literal['Q', ' ']) -> None:
            print(f'\033[47m \033[30m{q} \033[0m', end="")

        for i in range(len(self.matrix)):
            print("|", end="")

            for j in range(len(self.matrix[i])):
                q = 'Q' if self.matrix[i][j] == 1 else ' '

                if (i % 2 == 0):
                    if (j % 2 == 0):
                        print_white_cell(q)
                    else:
                        print_black_cell(q)

                else:
                    if (j % 2 == 0):
                        print_black_cell(q)
                    else:
                        print_white_cell(q)

            print("|")
        print(end, end='')
