from .board import CellState, Board
import pytest


class Player:
    def __init__(self, color: CellState):
        self.color = color

    def is_direction_valid(self, board: Board, position: tuple[int, int], direction: tuple[int, int]) -> bool:
        """Checks if a move in a specific direction is valid for the player

        Args:
            board (Board): The current game board
            position (tuple[int, int]): The (row, column) position to check
            direction (tuple[int, int]): The (dy, dx) direction to check
        Returns:
            bool: True if the move in the specified direction is valid, False otherwise
        """
        dy, dx = direction
        y, x = position
        y += dy
        x += dx
        has_opponent_piece = False

        while board.is_valid_cell((y, x)):
            if board[y, x] == CellState.EMPTY:
                return False  # Empty cell, no flips possible
            if board[y, x] != self.color:
                has_opponent_piece = True
            elif board[y, x] == self.color:
                return has_opponent_piece  # Valid if opponent piece to flip exists

            y += dy
            x += dx

        return False  # Reached border without confirming valid move

    def is_valid_move(self, board: Board, position: tuple[int, int]) -> bool:
        """Checks if a move is valid for the player

        Args:
            board (Board): The current game board
            position (tuple[int, int]): The (row, column) position to check

        Raises:
            IndexError: If the position is out of bounds

        Returns:
            bool: True if the move is valid, False otherwise
        """
        # A move is valid if the cell is empty and it would flip at least one opponent piece
        if not board.is_valid_cell(position):
            raise IndexError(f"Position {position} out of bounds")

        if board[position] != CellState.EMPTY:
            return False

        # Check in all 8 directions for valid flips
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        for dy, dx in directions:
            if self.is_direction_valid(board, position, (dy, dx)):
                return True
        return False

    def get_valid_moves(self, board: Board) -> list[tuple[int, int]]:
        """Returns a list of valid moves for the player

        Args:
            board (Board): The current game board
        Returns:
            list[tuple[int, int]]: A list of (row, column) positions that are valid moves for the player
        """
        valid_moves = []
        for y in range(8):
            for x in range(8):
                if self.is_valid_move(board, (y, x)):
                    valid_moves.append((y, x))
        return valid_moves

    def make_move(self, board: Board, position: tuple[int, int]) -> Board:
        """Attempts to make a move for the player at the specified position

        Args:
            board (Board): The current game board
            position (tuple[int, int]): The (row, column) position to place the piece

        Raises:
            ValueError: If the move is invalid for the player

        Returns:
            Board: The updated game board
        """
        if not self.is_valid_move(board, position):
            raise ValueError(
                f"Invalid move at position {position} for player {self.color}")

        # Place the piece
        board[position] = self.color
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if (dy, dx) != (0, 0) and self.is_direction_valid(board, position, (dy, dx)):
                    # Flip pieces in this direction
                    y, x = position
                    y += dy
                    x += dx
                    # Direction already validated, flip until friendly piece
                    while board[y, x] != self.color:
                        board[y, x] = self.color
                        y += dy
                        x += dx
        return board


# Unit tests
class TestPlayer:
    def test_valid_move(self):
        board = Board()
        player_b = Player(CellState.BLACK)
        player_w = Player(CellState.WHITE)

        # Valid move for white
        assert player_w.is_valid_move(board, (2, 3))

        # Invalid move for white (cell not empty)
        assert not player_w.is_valid_move(board, (3, 3))

        # Invalid move for white (no flips)
        assert not player_w.is_valid_move(board, (0, 0))

        # Invalid move for black (out of bounds)
        with pytest.raises(IndexError):
            player_b.is_valid_move(board, (8, 0))

    def test_make_move(self):
        board = Board()
        player_b = Player(CellState.BLACK)
        player_w = Player(CellState.WHITE)

        # Make a valid move
        updated_board = player_w.make_move(board, (2, 3))
        assert updated_board[2, 3] == CellState.WHITE

        # Attempt to make an invalid move
        with pytest.raises(ValueError):
            player_b.make_move(board, (0, 0))

        # Attempt to make a move on a non-empty cell
        with pytest.raises(ValueError):
            player_b.make_move(board, (3, 3))

        # Attempt to make a move out of bounds
        with pytest.raises(IndexError):
            player_w.make_move(board, (8, 0))
    
    def test_get_valid_moves(self):
        board = Board()
        player_b = Player(CellState.BLACK)
        player_w = Player(CellState.WHITE)

        # Initial valid moves for white
        valid_moves_w = player_w.get_valid_moves(board)
        assert (2, 3) in valid_moves_w
        assert (3, 2) in valid_moves_w
        assert (4, 5) in valid_moves_w
        assert (5, 4) in valid_moves_w
        assert len(valid_moves_w) == 4

        # Initial valid moves for black
        valid_moves_b = player_b.get_valid_moves(board)
        assert (2, 4) in valid_moves_b
        assert (3, 5) in valid_moves_b
        assert (4, 2) in valid_moves_b
        assert (5, 3) in valid_moves_b
        assert len(valid_moves_b) == 4


if __name__ == "__main__":
    # Example usage
    board = Board()
    player_b = Player(CellState.BLACK)
    player_w = Player(CellState.WHITE)

    board.print_board()

    # Check some moves for player 1
    print(player_w.is_valid_move(board, (2, 3)))  # Should be True
    print(player_b.is_valid_move(board, (0, 0)))  # Should be False
    print(player_b.get_valid_moves(board))
