from abc import ABC, abstractmethod
from typing import Optional


class IHandler(ABC):
    def __init__(self, action, successor: Optional["IHandler"] = None):
        self.successor = successor
        self.action = action

    def handle(self, test, epsilon):
        self.action = self.check_epsilon(test, epsilon)
        if not hasattr(self.action, 'all'):
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
            return self.action.explore()


class Exploit(IHandler):
    "A Concrete Handler"

    def __init__(self, action, model, state, successor):
        super().__init__(action, successor)
        self.model = model
        self.state = state

    def check_epsilon(self, test, epsilon):
        if 1 > epsilon >= test > 0:
            # action = Action.exploit()
            print(f'handled in {self.__class__.__name__} because epsilon is {epsilon} and random is {test}')
            return self.action.exploit(self.model, self.state)


class FallbackHandler(IHandler):
    def check_epsilon(self, test, epsilon):
        print(f'handled in {self.__class__.__name__}')
        raise ValueError("epsilon must be in range 0 to 1 :", epsilon)
