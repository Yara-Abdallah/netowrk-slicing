from typing import Protocol


class Action(Protocol):
    def execute(self, state, action, **kwargs):
        ...

    def explore(self):
        ...

    def exploit(self, model, state):
        ...
