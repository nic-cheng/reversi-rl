from enum import Enum
import numpy as np
import pytest

light_mode = False


class CellState(Enum):
    """Enum class for cell states
        - EMPTY: Empty cell
        - BLACK: Black piece
        - WHITE: White piece
    """
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __str__(self) -> str:
        """Displays a cell state properly \n
        Flips black and white pieces based on light_mode setting for accurate colouring

        Returns:
            str: String representation of cell state
        """
        if self == CellState.EMPTY:
            return ' '
        elif self == CellState.BLACK:
            return '●' if light_mode else '○'
        elif self == CellState.WHITE:
            return '○' if light_mode else '●'
        else:
            return '?'


class Board:
    def __init__(self, initial_state: np.ndarray | None = None):
        if initial_state is None:
            self.board = np.full((8, 8), CellState.EMPTY)
            self.board[3, 3] = CellState.BLACK
            self.board[3, 4] = CellState.WHITE
            self.board[4, 3] = CellState.WHITE
            self.board[4, 4] = CellState.BLACK
        else:
            self.board = initial_state

    def print_board(self):
        """Displays the current board state with row and column indices for reference
        """
        for i, row in enumerate(self.board):
            print(f"{i} |{' '.join(str(cell) for cell in row)}")
        print("   " + "-" * 15)
        print("   " + " ".join(str(i) for i in range(8)))

    def is_valid_cell(self, position: tuple[int, int]) -> bool:
        """Check if the given position is within the board boundaries

        Args:
            position (tuple[int, int]): The (row, column) position to check

        Returns:
            bool: True if the position is within the board boundaries, False otherwise
        """
        y, x = position
        return 0 <= y < 8 and 0 <= x < 8

    def count_pieces(self) -> tuple[int, int]:
        """Counts the number of black and white pieces on the board

        Returns:
            tuple[int, int]: A tuple (black_count, white_count)
        """
        black_count = 0
        white_count = 0
        for row in self.board:
            for cell in row:
                if cell == CellState.BLACK:
                    black_count += 1
                elif cell == CellState.WHITE:
                    white_count += 1
        return black_count, white_count

    def __getitem__(self, position: tuple[int, int]) -> CellState:
        """Reads the cell state at a given board position

        Args:
            position (tuple[int, int]): (row, col) position to read

        Raises:
            IndexError: If the position is out of bounds

        Returns:
            CellState: The state of the cell at the given position
        """
        if not self.is_valid_cell(position):
            raise IndexError(f"Position {position} out of bounds")
        return self.board[position]

    def __setitem__(self, position: tuple[int, int], value: CellState) -> None:
        """Sets the cell state at a given board position

        Args:
            position (tuple[int, int]): (row, col) position to set
            value (CellState): The new value to set the cell to

        Raises:
            IndexError: If the position is out of bounds
        """
        if not self.is_valid_cell(position):
            raise IndexError(f"Position {position} out of bounds")
        self.board[position] = value


# Unit tests
class TestBoard:
    def test_initial_setup(self):
        board = Board()
        assert board[0, 0] == CellState.EMPTY
        assert board[3, 3] == CellState.BLACK
        assert board[3, 4] == CellState.WHITE
        assert board[4, 3] == CellState.WHITE
        assert board[4, 4] == CellState.BLACK
        
        set_board = np.full((8, 8), CellState.BLACK)
        custom_board = Board(initial_state=set_board)
        assert custom_board[0, 0] == CellState.BLACK
        assert custom_board[4, 3] == CellState.BLACK
        

    def test_set_and_get_cell(self):
        board = Board()
        board[0, 0] = CellState.BLACK
        assert board[0, 0] == CellState.BLACK
        board[5, 6] = CellState.WHITE
        assert board[5, 6] == CellState.WHITE
        board[5, 6] = CellState.EMPTY
        assert board[5, 6] == CellState.EMPTY
        assert board[7, 7] == CellState.EMPTY

    def test_out_of_bounds_access(self):
        board = Board()
        with pytest.raises(IndexError):
            _ = board[8, 0]
        with pytest.raises(IndexError):
            _ = board[0, 8]
        with pytest.raises(IndexError):
            _ = board[-1, 0]
        with pytest.raises(IndexError):
            _ = board[0, -1]
        with pytest.raises(IndexError):
            board[8, 0] = CellState.BLACK
        with pytest.raises(IndexError):
            board[0, 8] = CellState.WHITE
        with pytest.raises(IndexError):
            board[-1, 0] = CellState.BLACK
        with pytest.raises(IndexError):
            board[0, -1] = CellState.WHITE

    def test_count_pieces(self):
        board = Board()
        board[0, 0] = CellState.BLACK
        black_count, white_count = board.count_pieces()
        assert black_count == 3
        assert white_count == 2
        board[1, 1] = CellState.WHITE
        black_count, white_count = board.count_pieces()
        assert black_count == 3
        assert white_count == 3


if __name__ == "__main__":
    board = Board()
    board.print_board()
