from argparse import ArgumentParser, ArgumentTypeError
from Queens import Nqueens

# for analysis
from timer import Timer
from Logger import log_file


def val_int(val):
    tmp = int(val)
    if tmp < 0:
        raise ArgumentTypeError("must provide non-negative value")
    return tmp


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument('-q', type=val_int, default=8)
    argparser.add_argument('-l', type=str, default='info_about_alg.log')

    # get number of queens from cl args
    queens: int = argparser.parse_args().q
    log_path: str = argparser.parse_args().l

    # Set up the logger
    log_file(log_path)

    # Create root node's board
    NQ_Astar = Nqueens(queens)

    # Print the root node's board
    NQ_Astar.root.board.print(pre=f"Generated {queens}x{queens} board:", end='')
    print(f"  ---: conflicts: {NQ_Astar.root.board.conflict_number()}\n")


    def solve():
        with Timer():
            NQ_Astar.AStar()


    solve()

    print(f"\n** logged to {log_path} **")
