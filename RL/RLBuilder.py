from Outlet.Cellular.ThreeG import ThreeG
from RL.AgentBuilder import ActionBuilder, AgentBuilder_
from RL.EnvBuilder import EnvironmentBuilder
from RL.RLAlgorithms.Centralized_DQN import DQN
from RL.RLAlgorithms.Model import Model
from keras.optimizers import Adam

from RL.RLEnvironment.Reward.CentralizedReward import CentralizedReward
from RL.RLEnvironment.State.CentralizedState import CentralizedState


class RLBuilder:
    def __init__(self,model,rl=None):
        if rl is None:
            self.rl = DQN(model)
        else:
            self.rl = rl
    def __str__(self):
        return f" agent : {self.rl.agents} , env : {self.rl.environment}"

    def environment(self):
        return EnvBuilder(self.rl)

    def agent(self):

        return AgentBuilder(self.rl)

    def build(self):
        return self.rl


class EnvBuilder(RLBuilder):
    def __init__(self, rl):
        super().__init__(rl)

    def build_env(self):
        self.rl.environment = EnvironmentBuilder().state().build_state(CentralizedState())\
            .reward().build_reward(CentralizedReward()).build()
        return self


class AgentBuilder(RLBuilder):
    def __init__(self, rl):
        super().__init__(rl)

    def build_agent(self):
        self.rl.agents = AgentBuilder_().action().build_action().build()
        return self


model_ = Model(3, 6, 'relu', 'mse', Adam, 0.5, 'sigmoid').build_model()
build = RLBuilder(model_)
builder = build \
    .agent() \
        .build_agent() \
    .environment()\
        .build_env() \
    .build()

print(builder.agents)
print(builder.environment)



#print(mb.agents.action)

#print(mb.environment.state)
#print(mb.environment.reward)
#print(mb.build())

#c=CentralizedState()
# state = mb.environment().build_env().state
# action_obj , action_value = mb.agent().build_agent().build().chain(model_,[10.0, 15.0],0.1)
# print(action_obj.execute(c, action_value))


# action, action_value = agent.chain(model,state,0.1)
# print(action.execute(c, action_value))
