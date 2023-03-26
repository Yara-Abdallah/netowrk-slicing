import copy

import numpy as np
import rx
import rx.operators as ops

from Communications.BridgeCommunications.ComsThreeG import ComsThreeG
from Outlet.Cellular.ThreeG import ThreeG
from RL.RLEnvironment.State.State import State

from collections import deque


class DeCentralizedState(State):
    allocated_power: [float]
    supported_services: [bool]
    power_factor: [float]
    indices = []
    accumulated_powers = []
    filtered_powers = []

    def __init__(self):
        super().__init__()
        self.buffer_state = deque()
        self.num_statistical_information = 5
        self.num_state = 2
        self.state_shape = DeCentralizedState.state_shape(self.num_state, self.num_statistical_information)
        self._allocated_power = np.zeros(self.state_shape)
        self._power_factor = copy.deepcopy(self.power_factor)

    @staticmethod
    def state_shape(num_state, num_statistical_information):
        return [num_state, num_statistical_information]

    @property
    def allocated_power(self):
        return self._allocated_power

    @property
    def power_factor(self):
        return self._power_factor

    @allocated_power.setter
    def allocated_power(self, power_array):
        self._allocated_power[:, power_array[1]] = power_array[0]

    @power_factor.setter
    def power_factor(self, power_factor):
        self._power_factor[:, power_factor[1]] = power_factor[0]



    def update_state(self):
        self.buffer_state.append([self.power_factor, self.allocated_power])





