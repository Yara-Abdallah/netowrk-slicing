from abc import ABC, abstractmethod
from typing import Tuple
from collections import deque

from RL.RLBuilder import RLBuilder
from RL.RLEnvironment.Action.ActionResponse import ActionResponse
from RL.RLEnvironment.State.DecentralizedState import DeCentralizedState
from RL.RLEnvironment.Reward.DecentralizedReward import DeCentralizedReward


class Outlet(ABC):
    """
    Definition of coverage towers
    """

    __id = -1

    def __init__(
        self,
        position: Tuple[float],
        radius: float,
        power: [float],
        requests_allocated_power: [float],
    ):
        """
        Parameters
        ----------
        position : Tuple[float]
            The coordinates of the outlet.
        radius : float
            The radius of the coverage area.
        power : [float]
            The power or the outlet.

            """
        self.__class__.__id += 1
        self.dqn = RLBuilder().agent.build_agent(ActionResponse()).environment.build_env(DeCentralizedReward(),
                                                                                         DeCentralizedState()).model_.build_model(
            "decentralized", 7, 1).build()
        self._distinct = self.__class__.__id
        self.position = position
        self._radius = radius
        self._power = power  # bit rate
        self.requests_allocated_power = requests_allocated_power
        self._power_distinct = []
        self.request_buffer = []

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def power(self):
        return self._power

    @power.setter
    def power(self, value):
        self._power = value

    @property
    def distinct(self):
        return self._distinct

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

    @property
    def power_distinct(self):
        return [self._power, self._distinct]
