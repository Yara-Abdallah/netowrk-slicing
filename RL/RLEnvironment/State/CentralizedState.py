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
    supported_services: np.ndarray[int]
    indices = []
    accumulated_powers = []
    filtered_powers = []
    _services_ensured: np.ndarray[int]
    _services_requested: np.ndarray[int]
    _services_ensured_prev: np.ndarray[int]
    _services_requested_prev: np.ndarray[int]
    _capacity_each_tower = [0.0, 0.0, 0.0]
    _index_outlet: int
    _max_capacity_each_outlet = [0.0, 0.0, 0.0]
    _index_service: int
    _state_value_centralize = [[0.0] * 8 for _ in range(9)]
    _next_state_centralize = [[0.0] * 8 for _ in range(9)]
    _averaging_value_utility_centralize = 0.0
    _supported_service: int
    _utility_value_centralize_prev = 0.0

    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = CentralizedState.state_shape(self.num_services, self.grid_cell)
        self._allocated_power = 0
        self._supported_services = np.zeros((3, 3))
        self._services_ensured = np.zeros(3)
        self._services_requested = np.zeros(3)
        self._services_ensured_prev = np.zeros(3)
        self._services_requested_prev = np.zeros(3)
        self._capacity_each_tower = [0.0, 0.0, 0.0]
        self._averaging_value_utility_centralize_prev = 0.0
        self._index_outlet = 0
        self._max_capacity_each_outlet = [0.0, 0.0, 0.0]
        self._index_service = 0
        self._supported_service = 0
        self._utility_value_centralize_prev = 0.0

    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]

    @property
    def utility_value_centralize_prev(self):
        return self._utility_value_centralize_prev

    @utility_value_centralize_prev.setter
    def utility_value_centralize_prev(self, value):
        self._utility_value_centralize_prev = value

    @property
    def averaging_value_utility_centralize_prev(self):
        return self._averaging_value_utility_centralize_prev

    @averaging_value_utility_centralize_prev.setter
    def averaging_value_utility_centralize_prev(self, value):
        self._averaging_value_utility_centralize_prev = value

    @property
    def max_capacity_each_outlet(self):
        return self._max_capacity_each_outlet

    @max_capacity_each_outlet.setter
    def max_capacity_each_outlet(self, value):
        self._max_capacity_each_outlet = value

    @property
    def index_outlet(self):
        return self._index_outlet

    @index_outlet.setter
    def index_outlet(self, value):
        self._index_outlet = value

    @property
    def index_service(self):
        return self._index_service

    @index_service.setter
    def index_service(self, value):
        self._index_service = value

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
        self._services_requested_prev = value

    @property
    def services_ensured_prev(self):
        return self._services_ensured_prev

    @services_ensured_prev.setter
    def services_ensured_prev(self, value):
        self._services_ensured_prev = value

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
    def services_ensured(self, value):
        self._services_ensured = value

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
        # self._supported_services = supported_array

    @property
    def supported_service(self):
        return self._supported_service

    @supported_service.setter
    def supported_service(self, value):
        self._supported_service = value

    def observer_sum(self, x):
        self.accumulated_powers.append(sum(x))

    def filter_power(self, x):
        self.indices.append(x)
        x = list(map(self.filtered_powers[x[0]].__getitem__, x[1]))
        return x

    def calculate_utility(self, service_index):
        percentage_array = 0
        if (self._services_ensured[service_index] - self._services_ensured_prev[service_index]) == 0 and (
                self._services_requested[service_index] - self._services_requested_prev[service_index]) == 0:
            percentage_array = 0
        elif (self._services_ensured[service_index] - self._services_ensured_prev[service_index]) != 0 and (
                self._services_requested[service_index] - self._services_requested_prev[service_index]) != 0:

            percentage_array = (self._services_ensured[service_index] - self._services_ensured_prev[service_index]) / (
                    self._services_requested[service_index] - self._services_requested_prev[service_index])
        else:
            percentage_array = 0

        return percentage_array

    def resetsate(self, tower_capacity):
        self._services_requested = np.zeros(3)
        self._services_ensured = np.zeros(3)
        self._services_requested_prev = np.zeros(3)
        self._services_ensured_prev = np.zeros(3)
        self._capacity_each_tower = tower_capacity

    # def calculate_state(self, binary):
    #     temp = list(numpy.concatenate(binary).flat)
    #     count_zero = np.all(temp)
    #     if count_zero == False:
    #         self.accumulated _powers = []
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
        final_state.append(self.index_outlet)
        final_state.append(self.max_capacity_each_outlet[self.index_outlet])
        final_state.append(self.capacity_each_tower[self.index_outlet])
        final_state.append(self.index_service)
        # print(" (index_outlet:>>>>>>>>>>>>>>>>>>>>>>>> ", self.index_outlet)
        #
        # print(" (self.max in centralize state [:0]):>>>>>>>>>>>>>>>>>>>>>>>> ", self.max_capacity_each_outlet)
        #
        # print(" (self.services_requested[self.index_service] ", self.services_requested[self.index_service])
        # print(" list(self.supported_services[:0]) ",list(self.supported_services[:0]))
        # final_state.append(self.supported_services[:0])  .item()
        if isinstance(self.supported_service, np.ndarray):
            final_state.append((self.supported_services[self.index_service][self.index_outlet]).item())
        else:
            final_state.append(self.supported_services[self.index_service][self.index_outlet])
        final_state.append(self.services_requested[self.index_service])
        final_state.append(self.services_ensured[self.index_service])
        final_state.append(self.calculate_utility(self.index_service))
        # print("centralize next state : .......................... ", final_state)
        return final_state
