from Outlet.Cellular.ThreeG import ThreeG
from RL.AgentBuilder import ActionBuilder, AgentBuilder_
from RL.EnvBuilder import EnvironmentBuilder
from RL.RLAlgorithms.Centralized_DQN import DQN
from RL.RLAlgorithms.Model import Model
from keras.optimizers import Adam

from RL.RLEnvironment.Reward.CentralizedReward import CentralizedReward
from RL.RLEnvironment.State.CentralizedState import CentralizedState


class RLBuilder:
    def __init__(self, model, rl=None):
        self.model = model
        if rl is None:
            self.rl = DQN(model)
        else:
            self.rl = rl

    @property
    def environment(self):
        return EnvBuilder(self.rl, self.model)

    @property
    def agent(self):
        return AgentBuilder(self.rl, self.model)

    def build(self):
        return self.rl


class EnvBuilder(RLBuilder):
    def __init__(self, rl, model):
        super().__init__(model,rl)

    def build_env(self):
        self.rl.environment = (
            EnvironmentBuilder()
            .state()
            .build_state(CentralizedState())
            .reward()
            .build_reward(CentralizedReward())
            .build()
        )
        print("self.rl.environment", self.rl)
        return self


class AgentBuilder(RLBuilder):
    def __init__(self, rl, model):
        super().__init__(model,rl)

    def build_agent(self):
        print("self.rl.environment", self.rl)

        self.rl.agents = AgentBuilder_().action().build_action().build()
        return self


model = Model(3, 6, "relu", "mse", Adam, 0.5, "sigmoid").build_model()

build = RLBuilder(model)
builder = build.agent.build_agent().environment.build_env().build()

print(builder.agents)
print(builder.environment)
print("fuck", builder)