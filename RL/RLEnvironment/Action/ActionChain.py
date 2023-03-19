import numpy as np
from abc import ABC
from typing import Optional
from RL.RLEnvironment.Action.Action import *


class IHandler(ABC):
    def init(self, successor: Optional["Handler"] = None):
        self.successor = successor

    def handle(self, request: int) -> None:
        pass


class Explor(IHandler):
    "A Concrete Handler"

    @staticmethod
    def handle(self, test, epsilon):
        if test <= epsilon and test > 0:
            action = Action.explor()
            self.successor = Exploit()
        return action


class Exploit(IHandler):
    "A Concrete Handler"

    @staticmethod
    def handle(self, test, epsilon):
        if test > epsilon and test < 1:
            action = Action.exploit()
            self.successor = FallbackHandler()
        return action


class FallbackHandler(IHandler):
    @staticmethod
    def handle(self, test, epsilon):
        raise ValueError("epsilon must be in range 0 to 1 :", epsilon)


class Chain():
    "A chain with a default first successor"
    test = np.random.rand()
    epsilon = 0.8

    @staticmethod
    def start(test, epsilon):
        "Setting the first successor that will modify the payload"
        return Explor().handle(test, epsilon)
