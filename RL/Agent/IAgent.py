from abc import ABC, abstractmethod
from RL.IRL import RL


# noinspection PyAbstractClass
class Agent(RL):
    def __init__(self, episode, epsilon, gamma, alpha, batch_size, time_step):
        super().__init__(episode, epsilon, gamma, alpha, batch_size, time_step)

    pass
