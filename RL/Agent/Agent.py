import numpy as np

from RL.Agent.IAgent import AbstractAgent
from RL.RLEnvironment.Action.ActionChain import Exploit, Explore, FallbackHandler


class Agent(AbstractAgent):

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, a):
        self._action = a

    def chain(self, model, state, epsilon):
        "A chain with a default first successor"
        test = np.random.rand()
        "Setting the first successor that will modify the payload"
        action = self.action_type
        print("inside chain ,,, ", action)
        handler = Exploit(action, model, state, Explore(action, FallbackHandler(action)))
        # = np.where(handler.handle(test, epsilon) > 0.5, 1, 0)
        return action, handler.handle(test, epsilon)
