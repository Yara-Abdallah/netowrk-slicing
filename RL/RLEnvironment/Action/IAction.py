from abc import ABC, abstractmethod


class Action(ABC):
    def __init__(self):
        self.grid_cell = 2
        self.num_services = 3
        self.num_communication_requirenment = 3
        self.num_statistical_information = 5

    @abstractmethod
    def execute(self, state, action, **kwargs):
        pass

    @abstractmethod
    def explore(self):
        pass

    @abstractmethod
    def exploit(self, model, state):
        pass
