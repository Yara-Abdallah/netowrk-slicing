from typing import Tuple

from RL.RLEnvironment.Reward.Reward import Reward
from RL.RLEnvironment.State.State import State


class Action :
    def __init__(self) :
        pass

    def execute(self,state: State) -> Tuple[State,Reward]:
        raise NotImplementedError

    def explore(self):
        raise NotImplementedError
    def exploit(self):
        raise NotImplementedError


