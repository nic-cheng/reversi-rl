from .board import Board, Colour
from .moves import get_valid_moves, is_move_valid, make_move, pass_turn

import random
from typing import Optional


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


def random_board(seed: Optional[int] = None, approx_moves_to_end: Optional[int] = None) -> Board:
    """Generate a random board state by applying a random sequence of valid moves from the initial position.

    Args:
        seed: Optional random seed for reproducibility
        approx_moves_to_end: Optional approximate number of moves to end the game (default is random)
    Returns:
        Board: A random board state
    """
    if seed is None:
        seed = random.randint(0, pow(10, 28))

    random.seed(seed)

    board = Board.from_fen()  # Start from the initial position
    move_list = []

    # Randomly apply valid moves until the game is over
    while not is_game_over(board):
        valid_moves = get_valid_moves(board)
        if valid_moves:
            move = random.choice(valid_moves)
            board = make_move(board, move)
            move_list.append(move)
        else:
            # If no valid moves, pass the turn to the opponent
            board = pass_turn(board)
            move_list.append(None)  # Use None to represent a pass

    # Randomly choose how many moves to game end if not specified
    if approx_moves_to_end is None:
        # Randomly choose how many moves to end the game
        approx_moves_to_end = random.randint(2, len(move_list))
        # print(f"Randomly chosen approx_moves_to_end: {approx_moves_to_end}")

    # Slice the move list to get approximately the desired number of pieces placed to end the game
    if len(move_list) > approx_moves_to_end:
        move_count = 0
        while move_count < approx_moves_to_end:
            curr_move = move_list.pop()
            move_count += 1 if curr_move is not None else 0
        
    else:  # If not enough moves, return the initial position
        return Board.from_fen()

    new_board = Board.from_fen()  # Reset to initial position
    for move in move_list:
        if move is not None:
            new_board = make_move(new_board, move)
        else:
            new_board = pass_turn(new_board)

    return new_board


if __name__ == "__main__":
    # Example usage: Generate a random board state and print it
    print()
    random_board_state = random_board(seed=None, approx_moves_to_end=None)
    
    random_board_state.display()
    print(random_board_state.to_fen())
