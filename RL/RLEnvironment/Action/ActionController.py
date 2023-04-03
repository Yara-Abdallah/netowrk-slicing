from RL.RLEnvironment.Action.Action import Action


class ActionController:
    _command: Action = None

    # print("comm ",self._command)

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, comm):
        self._command = comm

    def execute(self, state, action_decision, request_buffer):
        next_state = self._command.execute(state, action_decision, request_buffer)
        return next_state

    def explore(self):
        print("command  : ", self._command)
        return self._command.explore()

    def exploit(self, model, state):
        return self._command.exploit(model, state)
