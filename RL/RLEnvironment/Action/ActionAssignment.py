import numpy as np
from RL.RLEnvironment.Action.Action import Action


class ActionAssignment:
    def __init__(self):
        self.grid_cell = 3
        self.num_services = 3
        self._action_value_centralize = [[0] * 8 for _ in range(9)]
        self._action_objects = [[0] * 8 for _ in range(9)]
    @property
    def action_objects (self):
        return self._action_objects
    @action_objects.setter
    def action_objects(self,value):
        self._action_objects = value
    @property
    def action_value_centralize(self):
        return self._action_value_centralize
    @action_value_centralize.setter
    def action_value_centralize(self,val):
        self._action_value_centralize = val

    def explore(self):
        c = np.random.randint(2, size=(1,2))
        return np.argmax(c[0])

    def exploit(self, model, state):
        #return np.array(model.predict(state, verbose=0).reshape(3, 3), )
        state = np.array(state).reshape([1, np.array(state).shape[0]])
        c = np.array(model.predict(state, verbose=0)).reshape(1, 2)
        return np.argmax(c[0])

    def execute(self, state, action_decision):
        # state.supported_services = action_decision
        # print(" state.calculate_state() : " , v )
        return state.calculate_state()
