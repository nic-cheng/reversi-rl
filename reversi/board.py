from enum import Enum

import pytest


class Colour(Enum):
    BLACK = 1
    EMPTY = 0
    WHITE = -1

    @classmethod
    def from_char(cls, char: str) -> "Colour":
        if char == "B":
            return cls.BLACK
        elif char == "W":
            return cls.WHITE
        elif char == ".":
            return cls.EMPTY
        else:
            raise ValueError(f"Invalid character for Colour: {char}")

    def opponent(self) -> "Colour":
        """Get the opposite colour

        Returns:
            Colour: BLACK <-> WHITE, EMPTY -> EMPTY
        """
        return Colour(-self.value)

    def render(self):
        if self == self.BLACK:
            return "◯"
        elif self == self.WHITE:
            return "●"
        else:
            return "⠶"

    def __str__(self):
        if self == self.BLACK:
            return "B"
        elif self == self.WHITE:
            return "W"
        else:
            return "."


class Board():
    SIZE = 8

    def __init__(self, grid: list[list[Colour]], player_to_move: Colour):
        self.grid: list[list[Colour]] = grid
        self.player_to_move: Colour = player_to_move
        
    def copy(self) -> "Board":
        """Create a deep copy of the board

        Returns:
            Board: A new Board instance with the same grid and player to move
        """
        new_grid = [row.copy() for row in self.grid]
        return Board(new_grid, self.player_to_move)

    @classmethod
    def valid_square(cls, position: tuple[int, int]) -> bool:
        """Check if a position is within the bounds of the board

        Args:
            position (tuple[int, int]): The position to check
        Returns:
            bool: True if the position is valid, False otherwise
        """
        row, col = position
        return 0 <= row < Board.SIZE and 0 <= col < Board.SIZE

    @classmethod
    def from_fen(cls, fen: str = "8/8/8/3WB3/3BW3/8/8/8 B") -> "Board":
        """Initialize a board from FEN notation

        Args:
            fen (str): FEN string representing the board state and player to move, e.g. "8/8/8/3WB3/3BW3/8/8/8 B"

        Returns:
            Board: The initialized board
        """
        grid = []
        board_state, player_to_move = fen.split()

        for row in board_state.split("/"):
            board_row = []
            for char in row:
                if char.isdigit():
                    board_row.extend([Colour.EMPTY] * int(char))
                elif char == "B":
                    board_row.append(Colour.BLACK)
                elif char == "W":
                    board_row.append(Colour.WHITE)
            grid.append(board_row)

        return cls(grid, Colour.from_char(player_to_move))

    def to_fen(self) -> str:
        """Output the board state in an adapted form of FEN notation for reversi

        Returns:
            str: Board state in reversi FEN
        """
        fen = ""
        for row in self.grid:
            fen_row = ""
            empty_count = 0
            for piece in row:
                if piece == Colour.EMPTY:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += str(piece)
            if empty_count > 0:
                fen_row += str(empty_count)
            fen += fen_row + "/"
        return fen[:-1] + " " + str(self.player_to_move)

    def display(self) -> None:
        """Display the board in a human-readable format, with row and column numbers"""
        for i, row in enumerate(self.grid):
            print(f"{i}| {' '.join(piece.render() for piece in row)}")
        print("  " + "-" * (Board.SIZE * 2))
        print("   " + " ".join(str(i) for i in range(Board.SIZE)))

    def __getitem__(self, position: tuple[int, int]) -> Colour:
        if not (0 <= position[0] < Board.SIZE and 0 <= position[1] < Board.SIZE):
            raise IndexError(f"Position {position} out of bounds")
        row, col = position
        return self.grid[row][col]
    
    def __setitem__(self, position: tuple[int, int], value: Colour) -> None:
        if not (0 <= position[0] < Board.SIZE and 0 <= position[1] < Board.SIZE):
            raise IndexError(f"Position {position} out of bounds")
        row, col = position
        self.grid[row][col] = value


class TestBoard():
    def test_fen_conversion(self):
        fen = "8/8/8/3WB3/3BW3/8/8/8 B"
        board = Board.from_fen(fen)
        assert board.grid == [
            [Colour.EMPTY] * 8,
            [Colour.EMPTY] * 8,
            [Colour.EMPTY] * 8,
            [Colour.EMPTY, Colour.EMPTY, Colour.EMPTY, Colour.WHITE,
                Colour.BLACK, Colour.EMPTY, Colour.EMPTY, Colour.EMPTY],
            [Colour.EMPTY, Colour.EMPTY, Colour.EMPTY, Colour.BLACK,
                Colour.WHITE, Colour.EMPTY, Colour.EMPTY, Colour.EMPTY],
            [Colour.EMPTY] * 8,
            [Colour.EMPTY] * 8,
            [Colour.EMPTY] * 8
        ]
        assert board.player_to_move == Colour.BLACK
        assert board.to_fen() == fen
        
        fen = "BB5W/8/8/8/8/8/8/8 W"
        board = Board.from_fen(fen)
        assert board.grid == [
            [Colour.BLACK, Colour.BLACK, Colour.EMPTY, Colour.EMPTY, Colour.EMPTY, Colour.EMPTY, Colour.EMPTY, Colour.WHITE],
            [Colour.EMPTY] * 8,
            [Colour.EMPTY] * 8,
            [Colour.EMPTY] * 8,
            [Colour.EMPTY] * 8,
            [Colour.EMPTY] * 8,
            [Colour.EMPTY] * 8,
            [Colour.EMPTY] * 8
        ]
        assert board.player_to_move == Colour.WHITE
        assert board.to_fen() == fen

    def test_get_set_item(self):
        board = Board.from_fen()
        assert board[(3, 3)] == Colour.WHITE
        assert board[(3, 4)] == Colour.BLACK
        assert board[(0, 0)] == Colour.EMPTY

        board[(0, 0)] = Colour.BLACK
        assert board[(0, 0)] == Colour.BLACK

        with pytest.raises(IndexError):
            board[(-1, 0)]
        
        with pytest.raises(IndexError):
            board[(8, 0)] = Colour.WHITE


if __name__ == "__main__":
    board = Board.from_fen()
    board.display()
    print(board.to_fen())
