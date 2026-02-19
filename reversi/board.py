from enum import Enum
from typing import NamedTuple

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


if __name__ == "__main__":
    board = Board.from_fen()
    board.display()
    print(board.to_fen())
