import numpy as np

from RL.RLEnvironment.Reward.Reward import Reward


class CentralizedReward(Reward):
    _services_ensured: np.ndarray
    _services_requested: np.ndarray

    def __init__(self):
        super().__init__()
        self.grid_cell = 2
        self.num_services = 3
        self.state_shape = CentralizedReward.state_shape(self.num_services, self.grid_cell)
        self._services_ensured = np.zeros(self.num_services)

    @staticmethod
    def state_shape(num_services, grid_cell):
        return [num_services, grid_cell]

    def __call__(self):
        return self.reward_value

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
        self._services_ensured += np.array(value)

    def calculate_reward(self):
        percentage_array = self.services_ensured / self.services_requested
        self.reward_value = sum(percentage_array) / self.num_services
        return self.reward_value


# cr = CentralizedReward()
# cr.services_requested = np.array([30, 40, 10])
# cr.services_ensured = np.array([5, 10, 3])
# cr.services_ensured = np.array([3, 2, 1])
# cr.calculate_reward()
# print(cr())

