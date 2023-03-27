import numpy as np
from RL.RLEnvironment.Action.IAction import Action


class ActionAssignment(Action):

    def explore(self):
        print("assignment explor ",np.random.randint(2, size=(self.num_services, self.grid_cell)))
        return np.random.randint(2, size=(self.num_services, self.grid_cell))

    def exploit(self, model, state):
        print("assignment exploit ")
        state = np.array(state).reshape([1, np.array(state).shape[0]])
        return np.array(model.predict(state)).reshape(self.num_services, self.grid_cell)

    def execute(self, state, action_decision,**kwargs):
        print("action ", action_decision)
        print("action shape :", action_decision.shape)
        state.supported_services = action_decision
        return state.calculate_state(state.supported_services)
