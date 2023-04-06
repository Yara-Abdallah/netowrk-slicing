import numpy as np
from RL.RLEnvironment.Action.Action import Action


class ActionAssignment:
    def __init__(self):
        self.grid_cell = 3
        self.num_services = 3

    def explore(self):
        return np.random.randint(2, size=(self.num_services, self.grid_cell))

    def exploit(self, model, state):
        #ValueError: cannot reshape array of size 6 into shape (1,2)
        state = np.array(state).reshape([1, np.array(state).shape[0]])
        return np.array(model.predict(state)).reshape(self.num_services, self.grid_cell)

    def execute(self, state, action_decision):
        state.supported_services = action_decision
        return state.calculate_state(state.supported_services)
