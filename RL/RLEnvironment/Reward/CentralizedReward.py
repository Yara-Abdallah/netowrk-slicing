from RL.RLEnvironment.Reward.Reward import Reward


class CentralizedReward(Reward):
    supported_services: [bool]

    def __init__(self):
        self.gridCell = 2
        self.num_services = 3
        self.state_shape = self.shape_state(self.num_services, self.gridCell)
        self._supported_services = np.zeros(self.state_shape)
