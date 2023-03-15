from abc import ABC, abstractmethod


class RL(ABC):
    def __init__(self, episode, epsilon, gamma, alpha, batch_size, time_step):
        self.episode = episode
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.batch_size = batch_size
        self.time_step = time_step

    @abstractmethod
    def update_state(self):
        pass

    @abstractmethod
    def action(self):
        pass

    @abstractmethod
    def reward(self):
        pass

    @abstractmethod
    def build_model(self):
        pass
