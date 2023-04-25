import copy

import numpy
import numpy as np
import rx
import rx.operators as ops
from RL.RLEnvironment.State.State import State


class CentralizedState(State):
    allocated_power: [float]
    supported_services: [bool]
    indices = []
    accumulated_powers = []
    filtered_powers = []
    _services_ensured: np.ndarray
    _services_requested: np.ndarray
    _tower_capacity: float

    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = CentralizedState.state_shape(self.num_services, self.grid_cell)
        self._allocated_power = np.zeros(self.state_shape)
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
        self._services_requested = np.array(value)

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
        self._allocated_power[:, power_array[1]] = power_array[0]

    @supported_services.setter
    def supported_services(self, supported_array):
        self._supported_services[:, supported_array[1]] = supported_array[0]

    def observer_sum(self, x):
        self.accumulated_powers.append(sum(x))

    def filter_power(self, x):
        self.indices.append(x)
        x = list(map(self.filtered_powers[x[0]].__getitem__, x[1]))
        return x

    def calculate_utility(self):
        percentage_array = np.zeros(self.num_services)
        for i,j in enumerate(self.services_requested):
            if j == 0 :
                percentage_array[i] = 0
            else:
                percentage_array[i] = self.services_ensured[i] / self.services_requested[i]
        return percentage_array


    def resetsate(self):

        # self._services_ensured = np.zeros(self.num_services)
        # self._services_requested = np.zeros(self.num_services)
        self._allocated_power = np.zeros(self.num_services)

    def calculate_state(self, binary):
        temp = list(numpy.concatenate(binary).flat)
        count_zero = np.all(temp)
        if count_zero == False:
            self.accumulated_powers = []
            final_state = []
            xs = rx.from_(binary)
            disposable = xs.pipe(
                ops.map_indexed(
                    lambda x, i: (i, np.where(np.array(x) == 1.0))),
                ops.map(lambda x: [x[0], x[1][0]]),
                ops.map(self.filter_power))
            disposable.subscribe(self.observer_sum)
            # final_state.append(self.tower_capacity)
            final_state.extend(self.accumulated_powers)
            final_state.extend(self.calculate_utility())
            return final_state
        else:
            return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
