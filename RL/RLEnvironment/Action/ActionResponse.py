import random

import numpy as np
from RL.RLEnvironment.Action.Action import Action


class ActionResponse:
    def __init__(self):
        self.grid_cell = 3
        self.num_services = 3
        self._action_value_decentralize = 0
        self._action_flags = []

    @property
    def action_flags(self):
        return self._action_flags

    @action_flags.setter
    def action_flags(self, value):
        self._action_flags = value
    @property
    def action_value_decentralize(self):
        return self._action_value_decentralize
    @action_value_decentralize.setter
    def action_value_decentralize(self,val):
        self._action_value_decentralize = val


    def explore(self):
        c = np.random.randint(2, size=(1,2))
        # return np.argmax(c[0])
        return np.random.choice([0, 1])

    def exploit(self, model, state):

        state = np.array(state).reshape([1, np.array(state).shape[0]])
        c=np.array(model.predict(state , verbose=0)).reshape(1,2)
        return np.argmax(c[0])

    def execute(self, state, action):
        return state.calculate_state()
