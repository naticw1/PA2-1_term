from typing import Any, Optional
from board import Board
import pickle

class Node:
    def __init__(self, queens: Optional[int] = None, other=None) -> None:
        self.depth: int
        self.board: Board
        self.children: list[Any]

        if other and isinstance(other, Node):
            self.depth = other.depth + 1
            self.board = Board(other=other.board)
            self.children = [None] * (self.board.size * (self.board.size - 1))

        elif other and isinstance(other, Board):
            self.depth = 1
            self.board = pickle.loads(pickle.dumps(other, -1))
            self.children = [None] * (self.board.size * (self.board.size - 1))

        elif not other:
            self.depth = 1
            self.board = Board(queens=queens)  # create empty board
            self.board.generate_board()
            self.children = [None] * (self.board.size * (self.board.size - 1))

    # cost for A star
    @property
    def cost(self):
        _g = self.depth
        _h = self.board.conflict_number()
        return _g + _h

    # Comparator for priority queue
    def __lt__(self, node):
        return self.cost < node.cost

    # look at if it is solved
    def is_solved(self):
        return self.board.conflict_number() == 0

    # make move
    def expand(self):
        row = 0
        shift = 1

        for i in range(len(self.children)):
            if shift == self.board.size:
                row += 1
                shift = 1

            cp = pickle.loads(pickle.dumps(self, -1))

            self.children[i] = Node(other=cp)
            self.children[i].board.move_figure(row, shift)

            shift += 1