from .board import Board, Colour
import pytest

MOVE_DIRECTIONS = [(d_row, d_col) for d_row in [-1, 0, 1]
                   for d_col in [-1, 0, 1] if not (d_row, d_col) == (0, 0)]


def is_move_direction_valid(board: Board, position: tuple[int, int], direction: tuple[int, int]) -> bool:
    """Check if a move is valid from a given direction

    Args:
        board (Board): The board state and current player
        position (tuple[int, int]): The square to place the piece on
        direction (tuple[int, int]): (dx, dy) step vector

    Returns:
        bool: True if the move is valid in the given direction, False otherwise
    """
    ##
    # A move is valid in a direction if there is a line of opponent pieces and then a friendly piece
    # The line can be of length 1
    # Empty squares or the edge of the board break the line
    ##

    row, col = position

    # Guard against out of bounds
    if not Board.valid_square((row, col)):
        raise IndexError(f"Position {position} out of bounds")

    # Guard against no direction
    if direction == (0, 0):
        raise ValueError("Direction cannot be (0, 0)")

    # Guard against occupied square
    if board[(row, col)] != Colour.EMPTY:
        return False

    d_row, d_col = direction
    row += d_row
    col += d_col
    enemy_piece_encountered = False

    # First step must be an opponent piece
    if not Board.valid_square((row, col)) or board[(row, col)] != board.player_to_move.opponent():
        return False

    # Continue until line of opponents ends
    while Board.valid_square((row, col)) and board[(row, col)] == board.player_to_move.opponent():
        row += d_row
        col += d_col
        enemy_piece_encountered = True

    # Lazy evaluation means the value is only read if the ending square is in bounds
    # The line is valid only if it ends with a friendly piece and there was an enemy piece in between
    return Board.valid_square((row, col)) and board[(row, col)] == board.player_to_move and enemy_piece_encountered


def is_move_valid(board: Board, position: tuple[int, int]) -> bool:
    """Check if a move is valid (in any direction)

    Args:
        board (Board): The board state and current player
        position (tuple[int, int]): The square to place the piece on
    Returns:
        bool: True if the move is valid, False otherwise
    """
    for d_row, d_col in MOVE_DIRECTIONS:
        if is_move_direction_valid(board, position, (d_row, d_col)):
            return True
    return False


def get_valid_moves(board: Board) -> list[tuple[int, int]]:
    """Get a list of valid moves for the current player

    Args:
        board (Board): The board state and current player

    Returns:
        list[tuple[int, int]]: A list of valid move positions
    """
    valid_moves = []
    for row in range(Board.SIZE):
        for col in range(Board.SIZE):
            if is_move_valid(board, (row, col)):
                valid_moves.append((row, col))
    return valid_moves


def make_move(board: Board, position: tuple[int, int]) -> Board:
    """Make a move on the board and return the new board state

    Args:
        board (Board): The current board state and player
        position (tuple[int, int]): The square to place the piece on

    Returns:
        Board: The new board state after making the move
    """
    if not is_move_valid(board, position):
        raise ValueError(
            f"Move {position} is not valid for player {board.player_to_move}")

    new_board = board.copy()
    new_board[position] = board.player_to_move

    # Flip enemy pieces until a friendly piece is encountered in all valid directions
    for d_row, d_col in MOVE_DIRECTIONS:
        if is_move_direction_valid(board, position, (d_row, d_col)):
            row, col = position
            row += d_row
            col += d_col
            while Board.valid_square((row, col)) and new_board[(row, col)] != board.player_to_move:
                new_board[(row, col)] = board.player_to_move
                row += d_row
                col += d_col

    new_board.player_to_move = board.player_to_move.opponent()
    return new_board

def pass_turn(board: Board) -> Board:
    """Pass the turn to the opponent without making a move

    Args:
        board (Board): The current board state and player

    Returns:
        Board: A new board state with the same grid but opponent to move
    """
    new_board = board.copy()
    new_board.player_to_move = board.player_to_move.opponent()
    return new_board

class TestMoves:
    def test_is_move_direction_valid(self):
        board = Board.from_fen()
        with pytest.raises(IndexError):
            is_move_direction_valid(board, (8, 0), (1, 0))
        with pytest.raises(ValueError):
            is_move_direction_valid(board, (2, 3), (0, 0))
        assert is_move_direction_valid(board, (2, 3), (1, 0)) == True
        assert is_move_direction_valid(board, (2, 3), (1, 1)) == False
        assert is_move_direction_valid(board, (2, 3), (0, 1)) == False
        assert is_move_direction_valid(board, (2, 3), (-1, 0)) == False
        assert is_move_direction_valid(board, (2, 3), (-1, -1)) == False
        assert is_move_direction_valid(board, (2, 3), (0, -1)) == False

    def test_is_move_valid(self):
        board = Board.from_fen()
        with pytest.raises(IndexError):
            is_move_valid(board, (0, -1))
        with pytest.raises(IndexError):
            is_move_valid(board, (0, 8))
        
        assert is_move_valid(board, (2, 3)) == True
        assert is_move_valid(board, (2, 4)) == False
        assert is_move_valid(board, (3, 2)) == True
        assert is_move_valid(board, (7, 0)) == False

    def test_get_valid_moves(self):
        board = Board.from_fen()
        valid_moves = get_valid_moves(board)
        expected_moves = [(2, 3), (3, 2), (4, 5), (5, 4)]
        assert set(valid_moves) == set(expected_moves)

    def test_make_move(self):
        board = Board.from_fen()
        new_board = make_move(board, (2, 3))
        expected_fen = "8/8/3B4/3BB3/3BW3/8/8/8 W"
        assert new_board.to_fen() == expected_fen
    
    def test_pass_turn(self):
        board = Board.from_fen()
        new_board = pass_turn(board)
        expected_fen = "8/8/8/3WB3/3BW3/8/8/8 W"
        assert new_board.to_fen() == expected_fen
        board = make_move(board, (2, 3))
        assert board.to_fen() == "8/8/3B4/3BB3/3BW3/8/8/8 W"
        assert new_board.to_fen() == "8/8/8/3WB3/3BW3/8/8/8 W"


if __name__ == "__main__":
    # board = Board.from_fen()
    # board.display()
    # print(get_valid_moves(board))
    # new_board = make_move(board, (2, 3))
    # new_board.display()
    # print(str(new_board))
    board = Board.from_fen("1BBBBBBW/WWWWBBWW/WWWWWWBW/WWWWWWWW/WWBBWWWW/WWBBBWWW/WWBBWWWW/WWWWWWWW W")
    print(get_valid_moves(board))
    board = make_move(board, (0, 0))
    board.display()
