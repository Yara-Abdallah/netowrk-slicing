from Outlet.Cellular.ThreeG import ThreeG
from RL.RLEnvironment.RLEnvironment import RLEnvironment
import numpy as np

from Utils.config import outlet_types


class EnvironmentBuilder:
    def __init__(self, env=None):
        if env is None:
            self.env = RLEnvironment()
        else:
            self.env = env

    def __str__(self):
        return f" state : {self.env.state} , env : {self.env.reward}"

    def state(self):
        return StateBuilder(self.env)

    def reward(self):
        return RewardBuilder(self.env)

    def build(self):
        return self.env


class StateBuilder(EnvironmentBuilder):
    def __init__(self, env):
        super().__init__(env)

    def build_state(self, c ):
        outlet = ThreeG(outlet_types.get("3G"), 0, 1, [1, 1, 1], 1, 1, [10, 15, 22], [10, 20, 30])
        outlet2 = ThreeG(outlet_types.get("3G"), 0, 1, [1, 1, 1], 1, 1, [10, 5, 12], [10, 10, 40])

        c.allocated_power = outlet.power_distinct
        c.supported_services = outlet.supported_services_distinct
        c.allocated_power = outlet2.power_distinct
        c.supported_services = outlet2.supported_services_distinct
        c.filtered_powers = c.allocated_power

        state = c.calculate_state(c.supported_services[0])
        self.env.state = state
        print("state is : ", state)
        return self


class RewardBuilder(EnvironmentBuilder):
    def __init__(self, env):
        super().__init__(env)

    def build_reward(self, cr):
        cr.services_requested = np.array([30, 40, 10])
        cr.services_ensured = np.array([5, 10, 3])
        cr.services_ensured = np.array([3, 2, 1])
        reward = cr.calculate_reward()
        self.env.reward = reward
        print("reward is : ", reward)
        return self

# en = EnvironmentBuilder()
# en = en \
#     .state() \
#     .build_state("1") \
#     .reward() \
#     .build_reward("2") \
#
# print(en)
# print(en.build())
