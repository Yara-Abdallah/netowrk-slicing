from abc import abstractmethod, ABC
from collections import deque
from typing import runtime_checkable, Protocol

from Communications.BridgeCommunications.ComsThreeG import ComsThreeG
from Outlet.Cellular.ThreeG import ThreeG
from RL.RLEnvironment.Action.ActionAssignment import ActionAssignment
from RL.RLEnvironment.Action.ActionChain import Exploit, Explore, FallbackHandler
from RL.RLEnvironment.Action.ActionResponse import ActionResponse

from RL.RLEnvironment.Action.Action import Action
from RL.RLEnvironment.State.CentralizedState import CentralizedState
from RL.RLEnvironment.State.State import State
import numpy as np


@runtime_checkable
class AgentProtocol(Protocol):
    action: Action

    def q(self):
        pass


class Agent():
    def __init__(self, action_type, epsilon=0.95, gamma=0.95, epsilon_decay=0.09, min_epsilon=0.01,
                 episodes=7,
                 cumulative_reward=0,
                 step=60 * 60 * 24):
        self.action_type = Action(action_type)
        self.epsilon = epsilon
        self.gamma = gamma
        self.buffer = deque()
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.episodes = episodes
        self.cumulative_reward = cumulative_reward
        self.step = step
        # model state action reward

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, a):
        self._action = a

    def replaybuffer(self):
        pass

    def train(self, model, stop_at_convergence=False, **kwargs):
        """ Train model. """
        pass

    def q(self, state):
        """ Return q values for state. """
        pass

    def chain(self, model,state, epsilon):
        "A chain with a default first successor"
        test = np.random.rand()
        "Setting the first successor that will modify the payload"
        action = self.action_type
        handler = Exploit(action, model,state, Explore(action, FallbackHandler(action)))
        return action,handler.handle(test, epsilon)

# comm = ComsThreeG(0, 0, 0, 0, 0)
# outlet = ThreeG(0, comm, [1, 1, 1], 1, 1, [10, 15, 22])
# outlet2 = ThreeG(0, comm, [0, 0, 1], 1, 1, [10, 15, 28])
#
# c = CentralizedState()
# # print(c.calculate_state(4, 3))
# c.allocated_power = outlet.power_distinct
# c.supported_services = outlet.supported_services_distinct
# c.allocated_power = outlet2.power_distinct
# c.supported_services = outlet2.supported_services_distinct
# c.filtered_powers = c.allocated_power
# # state=c.calculate_state(c.supported_services)
#
# #print(c.calculate_state(c.supported_services))
#
# state=c.calculate_state(c.supported_services)
# print(state)
# action = Chain().start(0.1)
