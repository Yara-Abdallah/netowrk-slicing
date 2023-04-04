from keras.optimizers import Adam

from Communications.BridgeCommunications.ComsThreeG import ComsThreeG
from Outlet.Cellular.ThreeG import ThreeG
from RL.Agent.Agent import Agent
from RL.RLAlgorithms.AbstractRL import AbstractRL
from RL.RLAlgorithms.Model import Model
from RL.RLEnvironment.Action.ActionResponse import ActionResponse
from RL.RLEnvironment.State.DecentralizedState import DeCentralizedState
from Service.Entertainment.Entertainment import FactoryEntertainment


class DQN(AbstractRL):
    def __init__(self, model, *args):
        super().__init__(*args)
        self.model = model


    # def create_model(self) -> Sequential:
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
service = FactoryEntertainment(100, 10, 2, 100, 15, [0.5,0.4,0.3])

outlet = ThreeG(0, comm, [1, 1, 1], 1, 1, [10, 15, 22],[10,20,30])
#outlet2 = ThreeG(0, comm, [0, 0, 1], 1, 1, [10, 15, 28])


d= DeCentralizedState()
d.allocated_power = outlet.power
d.power_factor = service.power_factor
#d.allocated_power = outlet2.power_distinct
d.power_factor = service.power_factor
d.update_state(outlet.request_buffer,1)
print("...... ",outlet.request_buffer)
state = d.calculate_state(outlet.request_buffer)
print(state)
model = Model(3, 6, 'relu', 'mse', Adam, 0.5, 'sigmoid').build_model()
agent = Agent(ActionResponse())
action, action_value = agent.chain(model,state,0.1)
print(">>>>>>  ",action_value)
state,_ = action.execute(d, action_value, outlet.request_buffer)
print(state)


