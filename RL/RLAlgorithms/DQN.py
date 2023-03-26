from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from RL.RLAlgorithms.AbstractRL import AbstractRL
from RL.RLAlgorithms.Model import Model
from RL.Agent.IAgent import Agent
from RL.RLEnvironment.Action.ActionAssignment import ActionAssignment
from RL.RLEnvironment.RLEnvironment import RLEnvironment
from Communications.BridgeCommunications.ComsThreeG import ComsThreeG
from Outlet.Cellular.ThreeG import ThreeG
from RL.RLEnvironment.State.CentralizedState import CentralizedState


class DQN(AbstractRL):
    def __init__(self, model, *args):
        super().__init__(*args)
        self.model = model

    #def create_model(self) -> Sequential:
    #    return self.model.build_model()

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

comm = ComsThreeG(0, 0, 0, 0, 0)
outlet = ThreeG(0, comm, [1, 1, 1], 1, 1, [10, 15, 22])
outlet2 = ThreeG(0, comm, [0, 0, 1], 1, 1, [10, 15, 28])
c = CentralizedState()
c.allocated_power = outlet.power_distinct
c.supported_services = outlet.supported_services_distinct
c.allocated_power = outlet2.power_distinct
c.supported_services = outlet2.supported_services_distinct
c.filtered_powers = c.allocated_power
state = c.calculate_state(c.supported_services)
print(state)
model = Model(3, 6, 'relu', 'mse', Adam, 0.5, 'sigmoid').build_model()
agent = Agent(ActionAssignment())
action, action_value = agent.chain(model,state,0.9)
print(action.execute(c, action_value))
# env = RLEnvironment()
env = ''
"""a = DQN(model, agent, env)
print(a.agents)
a.env = env
a.agents = agent"""
print(model.summary())
