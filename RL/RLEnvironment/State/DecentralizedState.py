import copy

import numpy as np
import rx
import rx.operators as ops

from Communications.BridgeCommunications.ComsThreeG import ComsThreeG
from Outlet.Cellular.ThreeG import ThreeG
from RL.RLEnvironment.State.State import State
from Utils.Statistics import Statistics
from collections import deque
import itertools


class DeCentralizedState(State):
    allocated_power: [float]
    supported_services: [bool]
    power_factor: [float]
    indices = []
    accumulated_powers = []
    filtered_powers = []
    request_buffer = []

    def __init__(self):
        super().__init__()
        self.num_statistical_information = 4
        self.num_state = 2
        self.state_shape = DeCentralizedState.state_shape(self.num_state, self.num_statistical_information)
        self._allocated_power = []
        self._power_factor = []

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
        self._allocated_power = power_array

    @power_factor.setter
    def power_factor(self, power_factor):
        self._power_factor = power_factor

    def update_state(self, buffer_state, binary):
        if binary == 1:
            buffer_state.extend(np.stack((
                np.array(self.power_factor), np.array(self.allocated_power)), axis=1)
            )
            return True
        else:
            return False

    def calculate_state(self, buffer_state):
        return [Statistics.mean(buffer_state), Statistics.std(buffer_state), Statistics.max(buffer_state),
                Statistics.min(buffer_state)]
