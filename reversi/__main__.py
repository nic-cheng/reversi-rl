from .board import CellState, Board
from .player import Player

if __name__ == "__main__":
    # Example usage
    board = Board()
    player_b = Player(CellState.BLACK)
    player_w = Player(CellState.WHITE)
    
    while (player_b.get_valid_moves(board) or player_w.get_valid_moves(board)):
        print("Current board:")
        board.print_board()
        
        if player_b.get_valid_moves(board):
            move_b = player_b.get_valid_moves(board)[0]
            print(f"Black plays: {move_b}")
            board = player_b.make_move(board, move_b)
        else:
            print("Black has no valid moves and must pass.")

        if player_w.get_valid_moves(board):
            move_w = player_w.get_valid_moves(board)[0]
            print(f"White plays: {move_w}")
            board = player_w.make_move(board, move_w)
        else:
            print("White has no valid moves and must pass.")
    
    board.print_board()
    print("Game over!")
    
    
