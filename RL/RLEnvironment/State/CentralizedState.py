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

    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = CentralizedState.state_shape(self.num_services, self.grid_cell)
        self._allocated_power = np.zeros(self.state_shape)
        self._supported_services = copy.deepcopy(self.allocated_power)

    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]

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

    def calculate_state(self, binary):
        temp = list(numpy.concatenate(binary).flat)
        countzero = np.all(temp)
        # print("temp : >>>>>>>>>>>>>>>>>>>>>>>>",temp)
        # print("bool : >>>>>>>>>>>>>>>>>>>>>>>>",countzero)
        # print("binary : >>>>>>>>>>>>>>>>>>>>>>",binary)
        if countzero == False:
            self.accumulated_powers = []
            xs = rx.from_(binary)
            disposable = xs.pipe(
                ops.map_indexed(
                    lambda x, i: (i, np.where(np.array(x) == 1.0))),
                ops.map(lambda x: [x[0], x[1][0]]),
                ops.map(self.filter_power))
            disposable.subscribe(self.observer_sum)
            # print("self.accumulated_powers : >>>>>>>>>>>> ",self.accumulated_powers)
            return self.accumulated_powers
        else:
            return [0.0, 0.0, 0.0]
