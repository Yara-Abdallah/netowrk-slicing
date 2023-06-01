import copy
from pandas.core.common import flatten
import numpy
import numpy as np
import rx

# import rx
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
    _services_ensured_prev: np.ndarray
    _services_requested_prev: np.ndarray
    _capacity_each_tower = [0.0, 0.0, 0.0]
    _state_value_centralize = [0.0]*21
    _next_state_centralize = [0.0]*21
    _averaging_value_utility_centralize = 0.0

    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = CentralizedState.state_shape(self.num_services, self.grid_cell)
        self._allocated_power = np.zeros(self.state_shape)
        self._supported_services = copy.deepcopy(self.allocated_power)
        self._services_ensured = np.zeros(self.num_services)
        self._services_requested = np.zeros(self.num_services)
        self._services_ensured_prev = np.zeros(self.num_services)
        self._services_requested_prev = np.zeros(self.num_services)
        self._capacity_each_tower = [0.0, 0.0, 0.0]
        self._averaging_value_utility_centralize_prev = 0.0

    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]
    @property
    def averaging_value_utility_centralize_prev (self):
        return self._averaging_value_utility_centralize_prev
    @averaging_value_utility_centralize_prev.setter
    def averaging_value_utility_centralize_prev(self,value):
        self._averaging_value_utility_centralize_prev = value

    @property
    def capacity_each_tower(self):
        return self._capacity_each_tower

    @capacity_each_tower.setter
    def capacity_each_tower(self, value):
        self._capacity_each_tower = value

    @property
    def state_value_centralize(self):
        return self._state_value_centralize

    @state_value_centralize.setter
    def state_value_centralize(self, val):
        self._state_value_centralize = val

    @property
    def next_state_centralize(self):
        return self._next_state_centralize

    @next_state_centralize.setter
    def next_state_centralize(self, val):
        self._next_state_centralize = val

    @property
    def services_requested_prev(self):
        return self._services_requested_prev

    @services_requested_prev.setter
    def services_requested_prev(self, value):
        self._services_requested_prev = np.array(value)

    @property
    def services_ensured_prev(self):
        return self._services_ensured_prev

    @services_ensured_prev.setter
    def services_ensured_prev(self, value: np.ndarray):
        self._services_ensured_prev = np.array(value)

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
        for i in range(3):
            if (self._services_ensured[i] - self._services_ensured_prev[i]) == 0 and (
                    self._services_requested[i] - self._services_requested_prev[i]) == 0:
                percentage_array[i] = 0
            elif (self._services_ensured[i] - self._services_ensured_prev[i]) != 0 and (
                    self._services_requested[i] - self._services_requested_prev[i]) != 0:

                percentage_array[i] = (self._services_ensured[i]- self._services_ensured_prev[i]) / (
                        self._services_requested[i] - self._services_requested_prev[i])
            else:
                percentage_array[i] = 0

        return percentage_array

    def resetsate(self, tower_capacity):
        self._services_requested = np.zeros(self.num_services)
        self._services_ensured = np.zeros(self.num_services)
        self._capacity_each_tower = tower_capacity

    # def calculate_state(self, binary):
    #     temp = list(numpy.concatenate(binary).flat)
    #     count_zero = np.all(temp)
    #     if count_zero == False:
    #         self.accumulated_powers = []
    #         final_state = []
    #         xs = rx.from_(binary)
    #         disposable = xs.pipe(
    #             ops.map_indexed(
    #                 lambda x, i: (i, np.where(np.array(x) == 1.0))),
    #             ops.map(lambda x: [x[0], x[1][0]]),
    #             ops.map(self.filter_power))
    #         disposable.subscribe(self.observer_sum)
    #         # final_state.append(self.tower_capacity)
    #         final_state.extend(self.accumulated_powers)
    #         final_state.extend(self.calculate_utility())
    #         return final_state
    #     else:
    #         return [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    def calculate_state(self):
        final_state = []
        final_state.extend(self.capacity_each_tower)
        print(" (self.supported_services[:0]): ", (self.supported_services[:0]))
        print(" list(self.supported_services[:0]) ",list(self.supported_services[:0]))
        final_state.extend(list(flatten(self.supported_services[:0])))
        final_state.extend(list(flatten(self.supported_services[:1])))
        final_state.extend(list(flatten(self.supported_services[:2])))
        final_state.extend(self.services_requested)
        final_state.extend(self.services_ensured)
        final_state.extend(self.calculate_utility())

        return final_state
