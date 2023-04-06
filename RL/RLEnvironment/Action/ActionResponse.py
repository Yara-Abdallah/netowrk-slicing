import numpy as np
from RL.RLEnvironment.Action.Action import Action


class ActionResponse:
    def __init__(self):
        self.grid_cell = 3
        self.num_services = 3


    def explore(self):
        c = np.random.randint(2, size=(1,))
        return c

    def exploit(self, model, state):
        state = np.array(state).reshape([1, np.array(state).shape[0]])
        c=np.array(model.predict(state)).reshape(1,1)
        return c[0]

    def execute(self, state, action):
        return state.calculate_state()
