from RL.RLEnvironment.Action.ActionAsignment import ActionAssignment
from RL.RLEnvironment.Action.ActionResponse import ActionResponse
from RL.RLEnvironment.State.State import State


class Action:
    def __init__(self, command: ActionResponse | ActionAssignment):
        self._command = command
        pass

    def execute(self, state: State) -> None:
        self._command.excute(state)
        raise NotImplementedError

    def explore(self):
        return 1

    def exploit(self):
        return 2
