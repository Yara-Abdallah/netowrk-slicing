from abc import ABC, abstractmethod
from typing import Tuple


class Outlet(ABC):
    """
        Definition of coverage towers

        """


    def __init__(self, _id: int, position: Tuple[float], radius: float, power: float):

        """
            Parameters
            ----------
            position : Tuple[float,float,float]
                The coordinates of the outlet.
            radius : float
                The radius of the coverage area.
            power : float
                The power or the outlet.

            """

        self._id = _id
        self.position = position
        self.radius = radius
        self.power = power

    @abstractmethod
    def calculate_coverage_area(self):
        """Returns
            -------
            nothing , it is an abstract method
               The coverage area that the tower will response the requests in it."""
        pass

    @abstractmethod
    def calculate_downlink(self):
        """Returns
            -------
            nothing , it is an abstract method
               The downlink that the tower will use it for responsing the requests ."""
        pass
