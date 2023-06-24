import copy
# import rx
# import rx.operators as ops
import numpy as np
from RL.RLEnvironment.State.State import State


class DeCentralizedState(State):
    allocated_power: [float]
    _services_ensured: np.ndarray
    _services_requested: np.ndarray
    _services_ensured_prev: np.ndarray
    _services_requested_prev: np.ndarray
    _tower_capacity = 0.0
    _state_value_decentralize = [_tower_capacity, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0]
    _next_state_decentralize = [0.0] * 15

    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = DeCentralizedState.state_shape(self.num_services, self.grid_cell)
        self._allocated_power = np.zeros(3)
        self._supported_services = copy.deepcopy(self.allocated_power)
        self._services_ensured = np.zeros(self.num_services)
        self._services_requested = np.zeros(self.num_services)
        self._services_ensured_prev = np.zeros(self.num_services)
        self._services_requested_prev = np.zeros(self.num_services)
        self._tower_capacity = 0.0
        self._mean_power_allocated_requests = 0.0
        self._action_value = 0

    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]

    @property
    def mean_power_allocated_requests(self):
        return self._mean_power_allocated_requests

    @mean_power_allocated_requests.setter
    def mean_power_allocated_requests(self, value):
        self._mean_power_allocated_requests = value
    @property
    def action_value(self):
        return self._action_value
    @action_value.setter
    def action_value(self,value ):
        self._action_value = value
    @property
    def state_value_decentralize(self):
        return self._state_value_decentralize

    @state_value_decentralize.setter
    def state_value_decentralize(self, val):
        self._state_value_decentralize = val

    @property
    def next_state_decentralize(self):
        return self._next_state_decentralize

    @next_state_decentralize.setter
    def next_state_decentralize(self, val):
        self._next_state_decentralize = val

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
    def services_requested_prev(self):
        return self._services_requested_prev

    @services_requested_prev.setter
    def services_requested_prev(self, value):
        self._services_requested_prev = value

    @property
    def services_ensured_prev(self):
        return self._services_ensured_prev

    @services_ensured_prev.setter
    def services_ensured_prev(self, value: np.ndarray):
        self._services_ensured_prev = np.array(value)

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
        for i in range(3):
            if (self._services_ensured[i]) == 0 and (
                    self._services_requested[i]) == 0:
                percentage_array[i] = 0
            elif (self._services_ensured[i]) != 0 and (
                    self._services_requested[i]) != 0:
                percentage_array[i] = (self._services_ensured[i]) / (
                    self._services_requested[i])
            else:
                percentage_array[i] = 0

        return percentage_array

    def resetsate(self, tower_capacity):
        self._services_requested = np.zeros(self.num_services)
        self._services_ensured = np.zeros(self.num_services)
        self._tower_capacity = tower_capacity
        self._allocated_power = np.zeros(self.num_services)

    def calculate_state(self):
        final_state = []

        final_state.append(self.tower_capacity)
        if isinstance(self._action_value, np.ndarray):
           final_state.append(self._action_value.item())
        else :
            final_state.append(self._action_value)
        final_state.append(self._mean_power_allocated_requests)
        if isinstance(self._supported_services[0], np.ndarray):
            final_state.extend([i.item() for i in self._supported_services])
        else:
            final_state.extend(self._supported_services)
        final_state.extend(self._services_requested)
        final_state.extend(self._services_ensured)
        final_state.extend(self._allocated_power)
        if len(final_state) == 0:
            final_state = [0.0] * 15
        return final_state

    def calculate_initial_state(self):
        state = []
        state.append(self.tower_capacity)
        state.append(self._mean_power_allocated_requests)
        if isinstance(self._supported_services[0], np.ndarray):
            state.extend([i.item() for i in self._supported_services])
        else:
            state.extend(self._supported_services)
        state.extend(self._services_requested)
        state.extend(self._services_ensured)
        state.extend(self._allocated_power)
        return state
