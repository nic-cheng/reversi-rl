from typing import Optional
import numpy as np
import gymnasium as gym
from gymnasium.utils.env_checker import check_env

import reversi


class ReversiEnv(gym.Env):
    def __init__(self, board: Optional[reversi.Board] = None):
        self.board = board if board is not None else reversi.Board.from_fen()

        # # Observation as an 8x8 grid with values -1 (opponent), 0 (empty), 1 (current player)
        # self.observation_space = gym.spaces.Box(low=-1, high=1, shape=(8, 8), dtype=np.int8)

        # Flattened 8x8 grid to 1x64 to input into neural network
        self.observation_space = gym.spaces.Box(
            low=-1, high=1, shape=(1, 64), dtype=np.int8)

        self.action_space = gym.spaces.Discrete(64)  # Squares encoded by index
        self._action_to_move = lambda action: (
            action // 8, action % 8)  # Convert index to (row, col)

    @classmethod
    def board_from_obs(cls, obs: np.ndarray, player_to_move: reversi.Colour = reversi.Colour.BLACK) -> reversi.Board:
        """Convert an observation back to a Board object.

        Args:
            obs: 1x64 grid with values -1 (opponent), 0 (empty), 1 (current player)
            player_to_move: The colour of the current player

        Returns:
            Board: The corresponding Board object
        """
        grid = []
        for i in range(0, 64, 8):
            row = []
            for cell in obs[0][i:i+8]:
                if cell == 1:
                    row.append(player_to_move)
                elif cell == -1:
                    row.append(player_to_move.opponent())
                else:
                    row.append(reversi.Colour.EMPTY)
            grid.append(row)
        return reversi.Board(grid=grid, player_to_move=player_to_move)

    def _get_obs(self):
        """Convert internal state to observation format.

        Returns:
            # NDArray: 8x8 grid with values -1 (opponent), 0 (empty), 1 (current player)
            NDArray: Flattened 1x64 grid with values -1 (opponent), 0 (empty), 1 (current player)
        """
        def cell_state_to_value(piece: reversi.Colour, player: reversi.Colour) -> int:
            if piece == reversi.Colour.EMPTY:
                return 0
            elif piece == player:
                return 1
            else:
                return -1

        return np.array([
            cell_state_to_value(self.board[(row, col)], self.board.player_to_move) for col in range(8) for row in range(8)
        ], dtype=np.int8)

    def _get_info(self):
        """Compute auxiliary information for debugging.

        Returns:
            dict: Contains current player, board FEN, valid moves, and piece counts
        """
        return {
            "current_player": self.board.player_to_move,
            "board_fen": self.board.to_fen(),
            "valid_moves": reversi.get_valid_moves(self.board),
            "friendly_count": reversi.piece_count(self.board, self.board.player_to_move),
            "opponent_count": reversi.piece_count(self.board, self.board.player_to_move.opponent())
        }

    def reset(self, *, seed: Optional[int] = None, options: Optional[dict] = None):
        """Start a new episode.

        Args:
            seed: Random seed for reproducible episodes
            options: Additional configuration (unused in this example)

        Returns:
            tuple: (observation, info) for the initial state
        """
        # IMPORTANT: Must call this first to seed the random number generator
        super().reset(seed=seed)

        # Start from the standard initial board state
        self.board = reversi.random_board(seed=seed, approx_moves_to_end=None)

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        """Apply an action and return the new state.

        Args:
            action: An integer in [0, 63] representing the square to place a piece
        Returns:
            tuple: (observation, reward, terminated, truncated, info)
        """
        move = self._action_to_move(action)

        # Validate the move
        is_valid = reversi.is_move_valid(self.board, move)
        if is_valid:
            self.board = reversi.make_move(self.board, move)

        # Apply the move and update the board state

        # Check if the game is over
        terminated = reversi.is_game_over(self.board) or not is_valid

        # We don't use truncation in this simple environment
        # (could add a step limit here if desired)
        truncated = False

        # Reward is +1 for winning, -1 for losing, 0 otherwise
        piece_diff = reversi.piece_count(self.board, self.board.player_to_move) - \
            reversi.piece_count(
                self.board, self.board.player_to_move.opponent())
        if terminated:
            friendly_count = reversi.piece_count(
                self.board, self.board.player_to_move)
            opponent_count = reversi.piece_count(
                self.board, self.board.player_to_move.opponent())
            if not is_valid:
                # Invalid move penalty (should be filtered by masking)
                reward = -1
                print(f"Invalid move attempted: {move}")
            elif friendly_count > opponent_count:
                reward = 1
            elif friendly_count < opponent_count:
                reward = -1
            else:
                reward = 0
        else:
            # Normalize reward by total number of squares, with a small step penalty to encourage faster wins
            reward = piece_diff / 6400 - 0.01

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, truncated, info


# Register the environment so we can create it with gym.make()
gym.register(
    id="gymnasium_env/Reversi-v0",
    entry_point="agent.training_env:ReversiEnv",
    max_episode_steps=32,  # Prevent infinite episodes
)

if __name__ == "__main__":
    # Check that the environment adheres to the Gymnasium API
    env = gym.make("gymnasium_env/Reversi-v0")
    check_env(env)
