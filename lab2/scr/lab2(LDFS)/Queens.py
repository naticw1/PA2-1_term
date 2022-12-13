from node import Node
from board import Board, Optional
from Logger import NQLogger
import pickle


class Nqueens:
    def __init__(self, queens: int, board: Optional[Board] = None) -> None:

        # for report info
        self.mem_states: int = 1
        self.total_st: int = 1
        self.iteration: int = 0
        self.dead_ends = 0

        self.size = queens
        self.last_node: Node

        self.root = Node(queens=queens, other=board)

    def solve(self, limit):
        NQLogger.info("** LDFS Algorithm **")

        if self.LDFS(self.root, limit):
            print("There are solution: ")
        else:
            print("No solution with this limit")

        self.info()
        return True

    def LDFS(self, node: Node, limit):

        self.iteration += 1

        # pickle for copy
        self.last_node = pickle.loads(pickle.dumps(node, -1))

        if (node.is_solved()):
            NQLogger.info("** IDS Solved **")

            print("Solved board:")
            node.board.print()

            print("limits:")
            print(f"  ---: depth: {node.depth}")
            print(f"  ---: limit: {limit}\n")

            return True

        if node.depth < limit:

            NQLogger.info(f"#{self.iteration}: Expand with {len(node.children)} child nodes")

            node.expand()
            self.total_st += len(node.children)

            for i in range(len(node.children)):
                if self.LDFS(node.children[i], limit):
                    self.mem_states += len(node.children)
                    return True
                else:
                    self.dead_ends += 1

        return False

    def info(self):
        print("In total: ")
        print(f"  ---: iterations: {self.iteration}")
        print(f"  ---: states: {self.total_st}")
        print(f"  ---: memory states: {self.mem_states}")
        print(f"  ---: dead ends {self.dead_ends}")

        print()
