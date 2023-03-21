from abc import ABC, abstractmethod
from typing import Optional

import numpy as np


class IHandler(ABC):
    def __init__(self, successor: Optional["IHandler"] = None):
        self.successor = successor

    def handle(self, test, epsilon):
        res = self.check_epsilon(test, epsilon)
        if not res:
            self.successor.handle(test, epsilon)

    @abstractmethod
    def check_epsilon(self, test, epsilon) -> Optional[bool]:
        pass


class Explore(IHandler):
    "A Concrete Handler"

    def check_epsilon(self, test, epsilon):
        if 0 < epsilon < test < 1:
            # action = Action.explore()
            print(f'handled in {self.__class__.__name__} because epsilon is {epsilon} and random is {test}')
            return True


class Exploit(IHandler):
    "A Concrete Handler"

    def check_epsilon(self, test, epsilon):
        if 1 > epsilon >= test > 0:
            # action = Action.exploit()
            print(f'handled in {self.__class__.__name__} because epsilon is {epsilon} and random is {test}')
            return True


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
        handler = Explore(Exploit(FallbackHandler()))
        handler.handle(test, epsilon)


Chain().start(0.4)
