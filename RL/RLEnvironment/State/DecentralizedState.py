import copy
import rx
import rx.operators as ops
import numpy as np
from RL.RLEnvironment.State.State import State


class DeCentralizedState(State):
    allocated_power: [float]
    _services_ensured: np.ndarray
    _services_requested: np.ndarray
    _tower_capacity: float

    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = DeCentralizedState.state_shape(self.num_services, self.grid_cell)
        self._allocated_power = np.zeros(3)
        self._supported_services = copy.deepcopy(self.allocated_power)
        self._services_ensured = np.zeros(self.num_services)
        self._services_requested = np.zeros(self.num_services)
        self._tower_capacity = 0.0

    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]

    @property
    def tower_capacity(self):
        return self._tower_capacity

    @tower_capacity.setter
    def tower_capacity(self, value):
        self._tower_capacity = value

    @property
    def services_requested(self):
        return self._services_requested

    @services_requested.setter
    def services_requested(self, value):
        self._services_requested = value

    @property
    def services_ensured(self):
        return self._services_ensured

    @services_ensured.setter
    def services_ensured(self, value: np.ndarray):
        self._services_ensured = np.array(value)

    @property
    def allocated_power(self):
        return self._allocated_power

    @property
    def supported_services(self):
        return self._supported_services

    @allocated_power.setter
    def allocated_power(self, power_array):
        self._allocated_power = power_array

    @supported_services.setter
    def supported_services(self, supported_array):
        self._supported_services = supported_array

    def calculate_utility(self):
        percentage_array = np.zeros(self.num_services)
        for i, j in enumerate(self.services_requested):
            if j == 0:
                percentage_array[i] = 0
            else:
                percentage_array[i] = self.services_ensured[i] / self.services_requested[i]
        return percentage_array

    def resetsate(self, tower_capacity):
        # self._services_ensured = np.zeros(self.num_services)
        # self.services_requested = np.zeros(self.num_services)
        self._allocated_power = np.zeros(self.num_services)
        self._tower_capacity = tower_capacity

    def calculate_state(self):
        final_state = []
        final_state.append(self._tower_capacity)
        final_state.extend(self.allocated_power)
        final_state.extend(self.calculate_utility())
        return final_state
