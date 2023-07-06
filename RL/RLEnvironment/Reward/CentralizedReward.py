import numpy as np

from RL.RLEnvironment.Reward.Reward import Reward


class CentralizedReward(Reward):
    _services_ensured: np.ndarray
    _services_requested: np.ndarray

    _services_ensured_prev: np.ndarray
    _services_requested_prev: np.ndarray
    _reward_value = [[0] * 8 for _ in range(9)]

    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = CentralizedReward.state_shape(self.num_services, self.grid_cell)
        self._services_ensured = np.zeros(self.num_services)
        self._services_requested = np.zeros(self.num_services)
        self._services_ensured_prev = np.zeros(self.num_services)
        self._services_requested_prev = np.zeros(self.num_services)
        self._reward_value = [[0] * 8 for _ in range(9)]
        # self._reward_value = 0
        self._gridcell_reward_episode = 0

    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]

    @property
    def reward_value(self):
        return self._reward_value

    @reward_value.setter
    def reward_value(self, r):
        self._reward_value = r

    @property
    def gridcell_reward_episode(self):
        return self._gridcell_reward_episode

    @gridcell_reward_episode.setter
    def gridcell_reward_episode(self, r):
        self._gridcell_reward_episode = r

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


    def resetreward(self):
        print("reset reward of centralize")
        self._services_ensured_prev = np.zeros(self.num_services)
        self._services_requested_prev = np.zeros(self.num_services)
        self._services_requested = np.zeros(self.num_services)
        self._services_ensured = np.zeros(self.num_services)

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