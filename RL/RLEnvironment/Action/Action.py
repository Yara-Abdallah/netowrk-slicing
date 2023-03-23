from RL.RLEnvironment.Action.ActionAsignment import ActionAssignment
from RL.RLEnvironment.Action.ActionResponse import ActionResponse
from RL.RLEnvironment.State.State import State

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np


class Action:
    def __init__(self, command: ActionResponse | ActionAssignment):
        self._command = command

    def execute(self, state):
        return self._command.excute(state)

    def explore(self):
        return 1

    def exploit(self):
        return 2
