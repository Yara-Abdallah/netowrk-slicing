from RL.RLEnvironment.State.State import State
from abc import ABC, abstractmethod
from typing import Optional

import numpy as np



class IHandler(ABC):
    def __init__(self,action, successor: Optional["IHandler"] = None):
        self.successor = successor
        self.action = action

    def handle(self, test, epsilon):
        self.action = self.check_epsilon(test, epsilon)
        if not self.action:
            self.action = self.successor.handle(test, epsilon)
        return self.action

    @abstractmethod
    def check_epsilon(self, test, epsilon) -> Optional[bool]:

        pass


class Explore(IHandler):
    "A Concrete Handler"

    def check_epsilon(self, test, epsilon):
        if 0 < epsilon < test < 1:
            # action = Action.explore()
            print(f'handled in {self.__class__.__name__} because epsilon is {epsilon} and random is {test}')

            print("....  ",self.action.explore())
            return self.action.explore()


class Exploit(IHandler):
    "A Concrete Handler"

    def check_epsilon(self, test, epsilon):
        if 1 > epsilon >= test > 0:
            # action = Action.exploit()
            print(f'handled in {self.__class__.__name__} because epsilon is {epsilon} and random is {test}')

            print("....  ",self.action.explore())
            return self.action.explore()


class FallbackHandler(IHandler):

    def check_epsilon(self, test, epsilon):
        print(f'handled in {self.__class__.__name__}')
        raise ValueError("epsilon must be in range 0 to 1 :", epsilon)


class Chain():
    "A chain with a default first successor"

    epsilon = 0.8

    @staticmethod
    def start(epsilon):
        test = np.random.rand()
        "Setting the first successor that will modify the payload"
        a=Action(ActionResponse())
        handler = Exploit(a,Explore(a,FallbackHandler(a)))
        handler.handle(test, epsilon)
        print(handler.action)

Chain().start(-1)