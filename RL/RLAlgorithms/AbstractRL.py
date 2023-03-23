from abc import abstractmethod

from RL.RLMeta import RLMeta, rlabc


@rlabc
class AbstractRL(metaclass=RLMeta):
    _agents = []
    _env = None

    def __init__(self, agents, env):
        self._agents = agents
        self._env = env

    def len_(self):
        return len(self._agents)

    @property
    @abstractmethod
    def env(self):
        # return self._env
        pass

    @env.setter
    @abstractmethod
    def env(self, env):
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
