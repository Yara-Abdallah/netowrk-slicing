import math

from RL.RLEnvironment.Reward.Reward import Reward
import numpy as np


class DeCentralizedReward(Reward):
    _services_ensured: np.ndarray
    _services_requested: np.ndarray

    _services_ensured_prev: np.ndarray
    _services_requested_prev: np.ndarray

    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = DeCentralizedReward.state_shape(self.num_services, self.grid_cell)
        self._services_ensured = np.zeros(self.num_services)
        self._services_requested = np.zeros(self.num_services)
        self._services_ensured_prev = np.zeros(self.num_services)
        self._services_requested_prev = np.zeros(self.num_services)
        self.reward_value = 0
        self._dx_t = 0.0
        self._dx_t_prev = 0.0
        self._coeff = 0
        self._episode_reward_decentralize = 0

    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]

    @property
    def episode_reward_decentralize(self):
        return self._episode_reward_decentralize

    @episode_reward_decentralize.setter
    def episode_reward_decentralize(self, value):
        self._episode_reward_decentralize = value

    @property
    def coeff(self):
        return self._coeff

    @coeff.setter
    def coeff(self, coeff_value):
        self._coeff = coeff_value

    @property
    def dx_t(self):
        return self._dx_t

    @dx_t.setter
    def dx_t(self, d):
        self._dx_t = d

    @property
    def dx_t_prev(self):
        return self._dx_t_prev

    @dx_t_prev.setter
    def dx_t_prev(self, d):
        self._dx_t_prev = d

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
    def reward_value(self):
        return self._reward_value

    @reward_value.setter
    def reward_value(self, r):
        self._reward_value = r

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

    def resetreward(self):
        print("reset reward of decentralize")
        # self._services_requested = np.zeros(self.num_services)
        # self._services_ensured = np.zeros(self.num_services)

    def calculate_reward(self, x, action, c , max_capacity):
        if action == 0:
            action = -1
        reward = 0

        if x > 0:
            if action == 1:
                reward = action * math.pow(math.sqrt(x/max_capacity), -1 * action)
                # print("reward is : ", reward)
                return reward
            elif action == -1:
                reward = action * math.pow(math.sqrt(x/max_capacity), -1 * action)
                # print("reward is : ", reward)
                return reward
        elif x < 0:
            # print(" x is smaller : ..................  ",)
            alpha = 1 / c
            reward = -1 * action * math.pow(alpha,2) * math.pow(x, 2)
            # print("reward is : ", reward)
            return reward
        elif x == 0:
            # print("reward is : ", reward)
            return 1


    def coefficient(self, max_capacity, power_allocated_service, action, request_supported):
        if max_capacity > power_allocated_service and action == 1 and request_supported == 1:
            return 2
        elif max_capacity < power_allocated_service and action == 0 and request_supported == 0:
            return 2
        elif max_capacity < power_allocated_service and action == 0 and request_supported == 1:
            return 1
        elif max_capacity > power_allocated_service and action == 0 and request_supported == 0:
            return 1
        elif max_capacity > power_allocated_service and action == 1 and request_supported == 0:
            return -1
        elif max_capacity > power_allocated_service and action == 0 and request_supported == 1:
            return -3
        elif max_capacity < power_allocated_service and action == 1 and request_supported == 1:
            return -1
        elif max_capacity < power_allocated_service and action == 1 and request_supported == 0:
            return -3
