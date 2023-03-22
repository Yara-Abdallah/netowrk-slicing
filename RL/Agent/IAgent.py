from abc import abstractmethod, ABC
from collections import deque
from typing import runtime_checkable, Protocol
from RL.RLEnvironment.Action.ActionAsignment import ActionAssignment
from RL.RLEnvironment.Action.ActionResponse import ActionResponse

from RL.RLEnvironment.Action.Action import Action
from RL.RLEnvironment.State.State import State


@runtime_checkable
class AgentProtocol(Protocol):
    action: Action

    def q(self):
        pass


class Agent():
    def __init__(self, epsilon=0.95, gamma=0.95, epsilon_decay=0.09, min_epsilon=0.01, episodes=7,
                 cumulative_reward=0,
                 step=60 * 60 * 24):
        self._action = 1
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


command1 = ActionAssignment()
action1 = Action(command1)
state= 10
print(action1.execute(state))

command2 = ActionResponse()
action2 = Action(command2)

print(action2.execute(state))
print(isinstance(action1, AgentProtocol))
