from abc import abstractmethod

from RL.RLMeta import RLMeta, rlabc


@rlabc
class AbstractRL(metaclass=RLMeta):
    _agents = []
    _environment = None

    def __init__(self,model):
        self._agents = None
        self._environment = None
        self.model = model

    def len_(self):
        return len(self._agents)

    @property
    @abstractmethod
    def environment(self):
        # return self._env
        pass

    @environment.setter
    @abstractmethod
    def environment(self, env):
        # self._env = env
        pass

    @property
    @abstractmethod
    def agents(self):
        # return self.agents
        pass

    @agents.setter
    @abstractmethod
    def agents(self, agent):
        # self.agents.append(agent)
        pass

    @abstractmethod
    def create_model(self):
        pass
