import random
import math
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F

import reversi

from .environment import ReversiEnv

class DQN(nn.Module):
    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)

class Parameters:
    def __init__(self):
        self.env: ReversiEnv = ReversiEnv()
        self.device = torch.device("mps" if torch.mps.is_available() else "cpu")
        self.BATCH_SIZE = 128
        self.GAMMA = 0.999
        self.EPS_START = 0.9
        self.EPS_END = 0.05
        self.EPS_DECAY = 200
        self.TARGET_UPDATE = 10

def select_action(state: np.ndarray, policy: nn.Module, steps_done: int, params: Parameters) -> torch.Tensor:
    """Selects an action using epsilon-greedy strategy, with invalid moves filtered

    Args:
        state (np.ndarray): The current state representation as a numpy array.
        policy (nn.Module): The neural network policy model.
        steps_done (int): The number of steps completed so far (for epsilon decay).
        params (Parameters): The parameters object containing environment and training settings.

    Returns:
        torch.Tensor: The selected action as a tensor.
    """
    sample = random.random()
    eps_threshold = params.EPS_END + (params.EPS_START - params.EPS_END) * \
        math.exp(-1. * steps_done / params.EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            # t.max(1) will return the largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            nn_output = policy(state)
            # filter invalid moves
            board = ReversiEnv.board_from_obs(state, reversi.Colour.BLACK)  # Actual colours don't matter for move validity
            for i in range(64):
                if not reversi.is_move_valid(board, params.env._action_to_move(i)):
                    nn_output[0][i] = -float('inf')
            return nn_output.max(1).indices.view(1, 1)
    else:
        action = torch.tensor([[params.env.action_space.sample()]], device=params.device, dtype=torch.long)
        return action

