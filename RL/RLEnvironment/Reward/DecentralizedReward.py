
from RL.RLEnvironment.Reward.Reward import Reward
import numpy as np
class DeCentralizedReward(Reward):
    _services_ensured: np.ndarray
    _services_requested: np.ndarray

    def __init__(self):
        super().__init__()
        self.grid_cell = 3
        self.num_services = 3
        self.state_shape = DeCentralizedReward.state_shape(self.num_services, self.grid_cell)
        self._services_ensured = np.zeros(self.num_services)
        self._services_requested = np.zeros(self.num_services)
        self.reward_value = 0

    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]

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
    def reward_value(self):
        return self._reward_value

    @reward_value.setter
    def reward_value(self, r):
        self._reward_value = r


    def calculate_reward(self):
        percentage_array = np.zeros(self.num_services)
        for i, j in enumerate(self.services_requested):
            if j == 0:
                percentage_array[i] = 0
            else:
                percentage_array[i] = self.services_ensured[i] / self.services_requested[i]
        return percentage_array


