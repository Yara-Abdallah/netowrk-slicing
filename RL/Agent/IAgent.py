from abc import ABC, abstractmethod
from RL.IRL import RL


# noinspection PyAbstractClass
class Agent(RL):
    def __init__(self, *args):
        super().__init__(*args)

    pass
