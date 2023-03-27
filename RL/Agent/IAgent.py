from abc import abstractmethod
from collections import deque
from typing import runtime_checkable, Protocol

from RL.RLEnvironment.Action.Action import Action


@runtime_checkable
class AgentProtocol(Protocol):
    action: Action

    def q(self):
        pass


class AbstractAgent():
    def __init__(self, action_type, epsilon=0.95, gamma=0.95, epsilon_decay=0.09, min_epsilon=0.01,
                 episodes=7,
                 cumulative_reward=0,
                 step=60 * 60 * 24):
        self._action = None
        self.action_type = Action(action_type)
        self.epsilon = epsilon
        self.gamma = gamma
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon
        self.episodes = episodes
        self.cumulative_reward = cumulative_reward
        self.step = step
        # model state action reward

    @property
    @abstractmethod
    def action(self):
        pass

    @action.setter
    @abstractmethod
    def action(self, a):
        pass

    def replay_buffer(self):
        pass

    def train(self, model, stop_at_convergence=False, **kwargs):
        """ Train model. """
        pass

    def q(self, state):
        """ Return q values for state. """
        pass

    @abstractmethod
    def chain(self, model, state, epsilon):
        pass

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
