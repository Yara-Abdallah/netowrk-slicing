from Communications.BridgeCommunications.ComsThreeG import ComsThreeG
from Outlet.Cellular.ThreeG import ThreeG
from RL.Agent.IAgent import Agent
from Service.Entertainment.Entertainment import FactoryEntertainment
from Service.FactoryService import FactoryService
from Vehicle.Car import Car


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    service = FactoryEntertainment(100, 10, 2, 100, 15, [1, 1, 1])
    agent = Agent(100, 0.9, 0.9, 0.9, 32, 50)
    car = Car(1, 100, [2, 2], 50, service, [1, 2, 3, 4])
    comm = ComsThreeG(0, 0, 0, 0, 0, 0, 0, 0, 0)
    outlet = ThreeG(agent, comm, [0.1, 0.1], 1, 1, 1, 1, services_list=[10, 3])
    factEnt = FactoryService(100, 10, 2, 100, 15, [1, 1, 1]).produce_services("entertainment")
    print(service.calculate_arrival_rate())
    print(outlet.calculate_coverage_area())

    print("yara")
