from enum import Enum
import numpy as np

light_mode = False


class CellState(Enum):
    """
    @brief Represents the state of a cell on the Reversi board.
    Possible values: EMPTY, BLACK, WHITE
    """
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __str__(self) -> str:
        if self == CellState.EMPTY:
            return ' '
        elif self == CellState.BLACK:
            return '●' if light_mode else '○'
        elif self == CellState.WHITE:
            return '○' if light_mode else '●'
        else:
            return '?'


class Board:
    def __init__(self):
        self.board = np.full((8, 8), CellState.EMPTY)
        self.board[3, 3] = CellState.BLACK
        self.board[3, 4] = CellState.WHITE
        self.board[4, 3] = CellState.WHITE
        self.board[4, 4] = CellState.BLACK

    def print_board(self):
        for i, row in enumerate(self.board):
            print(f"{i} |{' '.join(str(cell) for cell in row)}")
        print("   " + "-" * 15)
        print("   " + " ".join(str(i) for i in range(8)))

    def is_valid_cell(self, position: tuple[int, int]) -> bool:
        y, x = position
        return 0 <= y < 8 and 0 <= x < 8

    def __getitem__(self, position: tuple[int, int]) -> CellState:
        return self.board[position]

    def __setitem__(self, position: tuple[int, int], value: CellState):
        if not self.is_valid_cell(position):
            raise IndexError("Position out of bounds")
        self.board[position] = value


if __name__ == "__main__":
    board = Board()
    board.print_board()
