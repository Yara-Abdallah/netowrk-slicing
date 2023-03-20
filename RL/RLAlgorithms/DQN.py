from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from RL.RLAlgorithms.AbstractRL import AbstractRL
from RL.RLAlgorithms.Model import Model
from RL.Agent.IAgent import Agent
from RL.RLEnvironment.RLEnvironment import RLEnvironment



def single_agent(class_):
    original_agents = class_.agents
    oa = class_.agents.fget(class_)

    print(len(oa))
    #class_.agents = oa[0]
    return class_
@single_agent
class DQN(AbstractRL):
    def __init__(self, model, *args):
        super().__init__(*args)
        self.model = model

    def create_model(self) -> Sequential:
        model_ = Sequential()
        model_.add(Dense(24, input_dim=self.model.state_size, activation=self.model.activation_function))
        model_.add(Dense(24, activation=self.model.activation_function))
        model_.add(Dense(self.model.action_size, activation=self.model.output_activation))
        model_.compile(loss=self.model.loss_function,
                       optimizer=self.model.optimization_algorithm(learning_rate=self.model.learning_rate))
        return model_

    def load(self, filename):
        self.model.load(filename)

    def save(self, filename):
        self.model.save(filename)

    @property
    def env(self):
        return self._env

    @env.setter
    def env(self, e):
        self._env = e

    @property
    def agents(self):
        return self._agents

    @agents.setter
    def agents(self, a):
        self._agents = a


model = Model(2, 2, 'relu', 'mse', Adam, 0.5, 'linear')
agent = Agent()
env = RLEnvironment()
a = DQN(model,agent,env)
print(a.agents)
#
a.env = env
a.agents = agent
model = a.create_model()
print(model.summary())
