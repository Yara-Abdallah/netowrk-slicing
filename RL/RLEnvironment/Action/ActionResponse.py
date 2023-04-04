import numpy as np
from RL.RLEnvironment.Action.Action import Action


class ActionResponse:
    def __init__(self):
        self.grid_cell = 3
        self.num_services = 3
        self.num_communication_requirement = 3
        self.num_statistical_information = 5

    def explore(self):
        c = np.random.randint(2, size=(1,))
        return c

    def exploit(self, model, state):
        return 1
        # state = np.array(state).reshape([1, np.array(state).shape[0]])
        # return np.array(model.predict(state)).reshape(self.num_communication_requirenment, self.num_statistical_information)

    def execute(self, state, action_decision, request_buffer):
        print(".... 111 11 ", action_decision)
        bool = state.update_state(request_buffer, action_decision)
        next_state = state.calculate_state(request_buffer)
        return next_state, bool
