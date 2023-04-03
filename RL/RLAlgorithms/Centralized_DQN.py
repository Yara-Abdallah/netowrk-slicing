from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from RL.RLAlgorithms.AbstractRL import AbstractRL


# from RL.RLAlgorithms.Model import Model
# from RL.Agent.Agent import Agent
# from RL.RLEnvironment.Action.ActionAssignment import ActionAssignment
# from RL.RLEnvironment.RLEnvironment import RLEnvironment
# from Communications.BridgeCommunications.ComsThreeG import ComsThreeG
# from Outlet.Cellular.ThreeG import ThreeG
# from RL.RLEnvironment.State.CentralizedState import CentralizedState
# from RL.RLEnvironment.State.DecentralizedState import DeCentralizedState
#

class DQN(AbstractRL):
    def init(self, *args):
        super().init(*args)

    # def create_model(self) -> Sequential:
    #    return self.model.build_model()

    def __str__(self):
        return f"evironment :  {self._environment} , agents : {self._agents} , model : {self._model}"

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, m):
        self._model = m

    def load(self, filename):
        self.model.load(filename)

    def save(self, filename):
        self.model.save(filename)

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, e):
        self._environment = e

    @property
    def agents(self):
        return self._agents

    @agents.setter
    def agents(self, a):
        self._agents = a

    def create_model(self):
        print("1")

# comm = ComsThreeG(0, 0, 0, 0, 0)
# outlet = ThreeG(0, comm, [1, 1, 1], 1, 1, [10, 15, 22],[10,20,30])
# outlet2 = ThreeG(0, comm, [0, 0, 1], 1, 1, [10, 15, 28],[10,20,30])
# c = CentralizedState()
#
# c.allocated_power = outlet.power_distinct
# c.supported_services = outlet.supported_services_distinct
# c.allocated_power = outlet2.power_distinct
# c.supported_services = outlet2.supported_services_distinct
# c.filtered_powers = c.allocated_power
# state = c.calculate_state(c.supported_services)
# print(state)
# model = Model(3, 6, 'relu', 'mse', Adam, 0.5, 'sigmoid').build_model()
#
# agent = Agent(ActionAssignment())
# action, action_value = agent.chain(model,state,0.1)
# print(action.execute(c, action_value))

# d= DeCentralizedState()
# # env = RLEnvironment()
# env = ''
# """a = DQN(model, agent, env)
# print(a.agents)
# a.env = env
# a.agents = agent"""
# print(model.summary())
