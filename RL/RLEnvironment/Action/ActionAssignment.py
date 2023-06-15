import numpy as np
from RL.RLEnvironment.Action.Action import Action


class ActionAssignment:
    def __init__(self):
        self.grid_cell = 3
        self.num_services = 3
        self._action_value_centralize = 0

    @property
    def action_value_centralize(self):
        return self._action_value_centralize
    @action_value_centralize.setter
    def action_value_centralize(self,val):
        self._action_value_centralize = val

    def explore(self):
        return np.random.randint(2, size=(self.num_services, self.grid_cell))

    def exploit(self, model, state):
        state = np.array(state).reshape([1, np.array(state).shape[0]])
        #np.array(model.predict(state, verbose=0).reshape(3, 3), )
        # x ,y , z =[],[],[]
        # x.append(np.array(model.predict(state, verbose=0).reshape(1,2), ))
        # x.append(np.array(model.predict(state, verbose=0).reshape(1,2), ))
        # x.append(np.array(model.predict(state, verbose=0).reshape(1, 2), ))
        # y.append(np.array(model.predict(state, verbose=0).reshape(1, 2), ))
        # y.append(np.array(model.predict(state, verbose=0).reshape(1, 2), ))
        # y.append(np.array(model.predict(state, verbose=0).reshape(1, 2), ))
        # z.append(np.array(model.predict(state, verbose=0).reshape(1, 2), ))
        # z.append(np.array(model.predict(state, verbose=0).reshape(1, 2), ))
        # z.append(np.array(model.predict(state, verbose=0).reshape(1, 2), ))
        # list_ = [x,y,z]
        # np.array(list_).reshape(3, 3)
        return np.array(model.predict(state, verbose=0).reshape(3, 3), )

    def execute(self, state, action_decision):
        # state.supported_services = action_decision
        # print(" state.calculate_state() : " , v )
        return state.calculate_state()
