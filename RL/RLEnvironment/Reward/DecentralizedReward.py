import math

from RL.RLEnvironment.Reward.Reward import Reward
import numpy as np


class DeCentralizedReward(Reward):
    _services_ensured: int
    _services_requested: int



    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = DeCentralizedReward.state_shape(self.num_services, self.grid_cell)
        self._services_ensured = 0
        self._services_requested = 0
        self._prev_utility = 0
        self.reward_value = 0
        self._dx_t = 0.0
        self._dx_t_prev = 0.0
        self._coeff = 0
        self._period_reward_decentralize = []
        self._episode_reward_decentralize = []
        self._throughput_weight = 0.5
        self._throughput_derivation_weight = 0.5
        self.utility = 0
        self.rolling_sum_reward = 0
        self.rolling_sum_reward_320 = 0

    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]

    @property
    def prev_utility(self):
        return self._prev_utility

    @prev_utility.setter
    def prev_utility(self,value):
        self._prev_utility = value

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
    def services_ensured(self, value):
        self._services_ensured = value




    @property
    def reward_value(self):
        return self._reward_value

    @reward_value.setter
    def reward_value(self, r):
        self._reward_value = r

    def calculate_utility(self):
        print("self._services_requested : ", self.services_requested)
        print("self._services_ensured : ", self.services_ensured)
        if (self.services_ensured ) == 0 and (
                self.services_requested ) == 0:
            return 0
        elif (self.services_ensured ) != 0 and (
                self.services_requested ) != 0:

            return self.services_ensured / self.services_requested
        else:
             return 0


    def resetreward(self):
        self.reward_value = 0
        self.services_requested = 0
        self.services_ensured = 0
        self.utility = 0
        self.prev_utility = 0
    def calculate_reward2(self,requested,ensured):
        # self.utility  = self.calculate_utility()
        if requested != 0 and ensured != 0 :
            self.utility = ensured / requested
        else :
            self.utility = 0
        # print("utility : ",self.utility)
        # print("prev_utility : ",self._prev_utility)
        derivation_throughput = self.utility - self._prev_utility
        # print("derivation_throughput  : ", derivation_throughput )
        if self.utility == 0.0 :
            return -1
        else :
            return self._throughput_derivation_weight * math.tanh(derivation_throughput) + self._throughput_weight * self.utility
    def calculate_reward(self, x, action, c, max_capacity):
        if action == 0:
            action = -1
        reward = 0
        if x > 0:
            if action == 1:
                reward = action * math.pow(math.sqrt(x / max_capacity), -1 * action)
                # print("reward is : ", reward)
                return reward
            elif action == -1:
                reward = action * math.pow(math.sqrt(x / max_capacity), -1 * action)
                # print("reward is : ", reward)
                return reward
        elif x < 0:
            # print(" x is smaller : ..................  ",)
            alpha = 1 / c
            reward = -1 * action * math.pow(alpha, 2) * math.pow(x, 2)
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
