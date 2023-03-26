from RL.RLEnvironment.Action.ActionAssignment import ActionAssignment
from RL.RLEnvironment.Action.ActionResponse import ActionResponse
from RL.RLEnvironment.State.State import State


class Action:
    def __init__(self, command: ActionResponse | ActionAssignment):
        self._command = command

    def execute(self, state, action):
        return self._command.excute(state)


    def explore(self):
        return 1

    def exploit(self):
        return 2
