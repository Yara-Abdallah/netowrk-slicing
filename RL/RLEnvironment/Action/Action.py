from RL.RLEnvironment.Action.ActionAssignment import ActionAssignment
from RL.RLEnvironment.Action.ActionResponse import ActionResponse
from RL.RLEnvironment.State.State import State

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np


class Action:

    def __init__(self, command: ActionResponse | ActionAssignment):
        self._command = command
        self.grid_cell = 2
        self.num_services = 3

    def execute(self, state, action_decision):
        next_state = self._command.excute(state, action_decision)
        return next_state

    def explore(self):
        # random
        return np.random.randint(2, size=(self.num_services, self.grid_cell))

    def exploit(self, model, state):
        print("1 ",state)
        #return np.random.randint(2, size=(self.num_services, self.grid_cell))
        state = np.array(state).reshape([1, np.array(state).shape[0]])
        print("2 ", state)
        return np.array(model.predict(state)).reshape(3,2)

