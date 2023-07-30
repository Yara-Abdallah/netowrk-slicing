import copy
# import rx
# import rx.operators as ops
import numpy as np
from RL.RLEnvironment.State.State import State


class DeCentralizedState(State):
    allocated_power: [float]
    _services_ensured: int
    _services_requested: int
    _tower_capacity = 0.0
    _max_tower_capacity = 0.0
    _state_value_decentralize = [0.0] * 7
    _next_state_decentralize = [0.0] * 7

    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = DeCentralizedState.state_shape(self.num_services, self.grid_cell)
        self._allocated_power = np.zeros(3)
        self._supported_services = copy.deepcopy(self.allocated_power)
        self._services_ensured = 0
        self._services_requested = 0
        self._tower_capacity = 0.0
        self._index_service = 0
        self._mean_power_allocated_requests = np.zeros(self.num_services)
        self._action_value = 0
        self._number_requested_in_period = np.zeros(self.num_services)
        self._number_ensured_in_period = np.zeros(self.num_services)
        self._ratio_of_occupancy = 0



    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]

    @property
    def ratio_of_occupancy(self):
        return self._ratio_of_occupancy

    @ratio_of_occupancy.setter
    def ratio_of_occupancy(self, value):
        self._ratio_of_occupancy = value

    @property
    def mean_power_allocated_requests(self):
        return self._mean_power_allocated_requests

    @mean_power_allocated_requests.setter
    def mean_power_allocated_requests(self, value):
        self._mean_power_allocated_requests = value

    @property
    def number_requested_in_period(self):
        return self._number_requested_in_period

    @number_requested_in_period.setter
    def number_requested_in_period(self, value):
        self._number_requested_in_period = value

    @property
    def number_ensured_in_period(self):
        return self._number_ensured_in_period

    @number_ensured_in_period.setter
    def number_ensured_in_period(self, value):
        self._number_ensured_in_period = value

    @property
    def index_service(self):
        return self._index_service

    @index_service.setter
    def index_service(self,value):
        self._index_service = value
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
    def max_tower_capacity(self):
        return self._max_tower_capacity

    @max_tower_capacity.setter
    def max_tower_capacity(self, value):
        self._max_tower_capacity = value

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
        self._allocated_power = power_array

    @supported_services.setter
    def supported_services(self, supported_array):
        self._supported_services = supported_array

    def resetsate(self):
        self._services_requested = 0
        self._services_ensured = 0
        self._allocated_power = np.zeros(self.num_services)
        # out.dqn.environment.reward.reward_value = 0
        self.ratio_of_occupancy = 0
        self.mean_power_allocated_requests = np.zeros(self.num_services)
        self.state_value_decentralize = [0.0] * 7
        self._number_ensured_in_period = 0
        self._number_requested_in_period = 0

        self.tower_capacity = self.max_tower_capacity

    def calculate_state(self):
        final_state = []
        # final_state.append(self.max_tower_capacity)
        # final_state.append(self.tower_capacity)
        # if isinstance(self._action_value, np.ndarray):
        #    final_state.append(self._action_value.item())
        # else:
        #     final_state.append(self._action_value)
        final_state.append(self._ratio_of_occupancy)
        final_state.append(self._services_requested)
        final_state.extend(self._mean_power_allocated_requests)
        final_state.append(self._number_requested_in_period)
        final_state.append(self._number_ensured_in_period)
        # final_state.append(self.index_service)
        # if isinstance(self._supported_services[self.index_service], np.ndarray):
        #     final_state.append(self._supported_services[self.index_service])
        # else:
        #     final_state.append(self._supported_services[self.index_service])
        # final_state.append(self._services_requested[self.index_service])
        # final_state.append(self._services_ensured[self.index_service])
        # final_state.append(self._allocated_power[self.index_service])
        if len(final_state) == 0:
            final_state = [0.0] * 7
        return final_state

    def calculate_initial_state(self):
        state = []
        state.append(self.tower_capacity)
        state.append(self._mean_power_allocated_requests)
        if isinstance(self._supported_services[0], np.ndarray):
            state.extend([i.item() for i in self._supported_services])
        else:
            state.extend(self._supported_services)

        state.extend(self._allocated_power)
        return state
