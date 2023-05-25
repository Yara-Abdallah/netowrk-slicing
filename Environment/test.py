from RL.Agent.Agent import Agent
from RL.RLAlgorithms.CentralizeModel import CentralizeModel
from RL.RLAlgorithms.Centralized_DQN import CentralizeDQN
from RL.RLEnvironment.Action.ActionAssignment import ActionAssignment
from RL.RLEnvironment.Action.ActionController import ActionController
from RL.RLEnvironment.RLEnvironment import RLEnvironment
from RL.RLEnvironment.Reward.CentralizedReward import CentralizedReward
from RL.RLEnvironment.State.CentralizedState import CentralizedState

agent1 = Agent()
controller = ActionController()
action1 = ActionAssignment()
controller.command = action1
agent1.action = controller

reward1 = CentralizedReward()
state1 = CentralizedState()

enviroment1 = RLEnvironment()
enviroment1.state = state1
enviroment1.reward = reward1

model1 = CentralizeModel()
DQN1 = CentralizeDQN()
DQN1.environment = enviroment1
DQN1.agents = agent1
DQN1.model = model1


def outlets_logging(self, outlet_num, outlet, cars):
    return f"Outlet {outlet_num} : -> {outlet}   -  Number Of Cars Which Send Request To It -> {len(cars)} \n "


def car_services_logging(self, car_num, car, service):
    return f"  The Car {car_num} Which Send To It -> : {car} \n" \
           f"     And Its Services Is  ->  : {service} \n"


def logging_the_final_results(self, performance_logger):
    service_handled = performance_logger.service_handled

    for i, outer_key in enumerate(service_handled):
        num = 0
        print(self.outlets_logging(i, outer_key, service_handled[outer_key]))
        for key, value in performance_logger.service_handled[outer_key].items():
            num += 1
            print(self.car_services_logging(num, key, value))