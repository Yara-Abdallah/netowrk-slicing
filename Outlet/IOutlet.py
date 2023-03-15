from abc import ABC, abstractmethod
from typing import Tuple

class Outlet(ABC):
    def __init__(self, _id:int, position: Tuple[float], radius:float, power:float)  :
        self._id = _id
        self.position = position
        self.radius = radius
        self.power = power

    @abstractmethod
    def calculate_coverage_area(self):
        pass

    @abstractmethod
    def calculate_downlink(self):
        pass
