from .board import Board, Colour
from .moves import get_valid_moves, is_move_valid, make_move


def has_valid_moves(board: Board) -> bool:
    """Check if the current player has any valid moves

    Args:
        board (Board): The current board state and player

    Returns:
        bool: True if the current player has at least 1 valid move, false otherwise
    """
    return len(get_valid_moves(board)) > 0


def is_game_over(board: Board) -> bool:
    """Check if the game is over

    Args:
        board (Board): The current board state and player

    Returns:
        bool: True if the game is over (neither player has valid moves), false otherwise
    """
    return not has_valid_moves(board) and not has_valid_moves(Board(board.grid, board.player_to_move.opponent()))


def piece_count(board: Board, colour: Colour) -> int:
    """Count the number of pieces of a given colour on the board

    Args:
        board (Board): The current board state
        colour (Colour): The colour to count

    Returns:
        int: The number of pieces of the given colour on the board
    """
    return sum(row.count(colour) for row in board.grid)
