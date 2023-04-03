from Outlet.Cellular.ThreeG import ThreeG
from RL.AgentBuilder import ActionBuilder, AgentBuilder_
from RL.EnvBuilder import EnvironmentBuilder
from RL.ModelBuilder import ModelBuilder_
from RL.RLAlgorithms.Centralized_DQN import DQN
from RL.RLAlgorithms.Model import Model
from keras.optimizers import Adam

from RL.RLEnvironment.Reward.CentralizedReward import CentralizedReward
from RL.RLEnvironment.State.CentralizedState import CentralizedState


class RLBuilder:
    def __init__(self, rl=None):

        if rl is None:
            self.rl = DQN()
        else:
            self.rl = rl
    @property
    def model_(self):
        return ModelBuilder(self.rl)
    @property
    def environment(self):
        return EnvBuilder(self.rl)

    @property
    def agent(self):
        return AgentBuilder(self.rl)

    def build(self):
        return self.rl


class EnvBuilder(RLBuilder):
    def __init__(self, rl):
        super().__init__(rl)

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
    def __init__(self, rl):
        super().__init__(rl)

    def build_agent(self):
        print("self.rl.environment", self.rl)

        self.rl.agents = AgentBuilder_().action().build_action().build()
        return self

class ModelBuilder(RLBuilder):
    def __init__(self,rl):
        super().__init__(rl)

    def build_model(self):
        self.rl.model = ModelBuilder_().state_size().build_state_size(3) \
                          .action_size().build_action_size(4) \
                          .loss_func().build_loss_func("mse") \
                          .optimizer().build_optimizer(Adam) \
                          .activation_func().build_Activation("relu") \
                          .activation_func_output_layer().build_activation_output("sigmoid") \
                          .learning_rate().build_Learning_rate(0.5) \
                          .builder()

        return self



build = RLBuilder()
builder = build.agent.build_agent().environment.build_env().model_.build_model().build()

print(builder.agents)
print(builder.environment)
print(builder.model)
print("fuck", builder)
