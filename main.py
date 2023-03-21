from keras.optimizer_v2.adam import Adam

from Communications.BridgeCommunications.ComsThreeG import ComsThreeG
from Outlet.Cellular.ThreeG import ThreeG
from RL.Agent.Model.DQN import DQN
# from RL.Agent.IAgent import Agent
from Service.Entertainment.Entertainment import FactoryEntertainment
from Service.FactoryService import FactoryService
from Vehicle.Car import Car


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# class DQN(AbstractModel):
#     def create_model(self) -> Sequential:
#         model = Sequential()
#         model.add(Dense(24, input_dim=self.state_size, activation=self.activation_function))
#         model.add(Dense(24, activation=self.activation_function))
#         model.add(Dense(self.action_size, activation=self.output_activation))
#         model.compile(loss=self.loss_function, optimizer=self.optimization_algorithm(lr=self.learning_rate))
#         return model

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = DQN(2, 2, 'relu', 'mse', Adam, 0.5, 'linear')
    print(a.summary())

    print_hi('PyCharm')
    service = FactoryEntertainment(100, 10, 2, 100, 15, [1, 1, 1])
    # agent = Agent(100, 0.9, 0.9, 0.9, 32, 50)
    car = Car(1, 100, [2, 2], 50, service, [1, 2, 3, 4])
    comm = ComsThreeG(0, 0, 0, 0, 0, 0, 0, 0, 0)
    outlet = ThreeG(0, comm, [0.1, 0.1], 1, 1, 1, 1, services_list=[10, 3])
    factEnt = FactoryService(100, 10, 2, 100, 15, [1, 1, 1]).produce_services("entertainment")
    print(service.calculate_arrival_rate())
    print(outlet.calculate_coverage_area())

    print("yara")
