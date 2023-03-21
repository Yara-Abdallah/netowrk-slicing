from abc import abstractmethod, ABC
from collections import deque

from RL.RLEnvironment.Action.Action import Action
from RL.RLEnvironment.State.State import State


class Agent():
    def __init__(self, epsilon=0.95, gamma=0.95, epsilon_decay=0.09, min_epsilon=0.01, episodes=7, cumulative_reward=0,
                 step=60 * 60 * 24):
        self.epsilon = epsilon
        self.gamma = gamma
        self.buffer = deque()
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.episodes = episodes
        self.cumulative_reward = cumulative_reward
        self.step = step
        # model state action reward

    @abstractmethod
    def replaybuffer(self, state: State, action: Action):
        pass

    def train(self, model, stop_at_convergence=False, **kwargs):
        """ Train model. """
        pass

    @abstractmethod
    def q(self, state):
        """ Return q values for state. """
        pass
