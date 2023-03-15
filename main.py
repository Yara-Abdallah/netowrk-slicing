# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Outlet.Cellular.ThreeG import ThreeG
from RL.Agent.IAgent import Agent
from Service.IService import Service
from Vehicle.Car import Car


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    #service = Service(100, 10, 2, 100, 15, [])
    #agent = Agent(100, 0.9, 0.9, 0.9, 32, 50)

    car = Car(1, 100, [2, 2], 50, 1, [1, 2, 3, 4])
    outlet = ThreeG([1, 1, 0], 1, car, 1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
