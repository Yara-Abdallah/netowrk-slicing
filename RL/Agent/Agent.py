import numpy as np

from RL.Agent.IAgent import AbstractAgent
from RL.RLEnvironment.Action.ActionChain import Exploit, Explore, FallbackHandler


class Agent(AbstractAgent):
    _grid_outlets = []

    @property
    def grid_outlets(self):
        return self._grid_outlets

    @grid_outlets.setter
    def grid_outlets(self, list_):
        self._grid_outlets = list_

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, a):
        self._action = a

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))

    def chain(self, model, state, epsilon):
        "A chain with a default first successor"
        test = np.random.rand()
        "Setting the first successor that will modify the payload"
        action = self.action
        print("inside chain ,,, ", action)
        handler = Exploit(action, model, state, Explore(action, FallbackHandler(action)))
        # = np.where(handler.handle(test, epsilon) > 0.5, 1, 0)
        # handler.handle(test, epsilon)
        return action, np.where(handler.handle(test, epsilon) > 0.5, 1, 0)
