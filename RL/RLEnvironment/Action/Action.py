from abc import abstractmethod,ABC

from RL.RLEnvironment.Action.ActionAssignment import ActionAssignment
from RL.RLEnvironment.Action.ActionResponse import ActionResponse
from RL.RLEnvironment.State.State import State

import numpy as np


class Action():

    def __init__(self, command: ActionResponse | ActionAssignment):

        self._command = command
        print("comm ",self._command)


    def execute(self, state, action_decision, request_buffer):
        next_state = self._command.execute(state, action_decision, request_buffer)
        return next_state

    def explore(self):
        print("command  : ",self._command)
        return self._command.explore()

    def exploit(self, model, state):
        return self._command.exploit(model, state)




