import numpy as np
import random
from RL.Agent.IAgent import AbstractAgent
from RL.RLEnvironment.Action.ActionChain import Exploit, Explore, FallbackHandler


class Agent(AbstractAgent):
    _grid_outlets = []
    _action_value = 0
    _outlets_id = []

    def __init__(self, *args):
        super().__init__(*args)
        self._outlets_id = []
        self._grid_outlets = []
        self._action_value = 0

    @property
    def outlets_id(self):
        return self._outlets_id

    @outlets_id.setter
    def outlets_id(self, id_):
        self._outlets_id = id_

    @property
    def grid_outlets(self):
        return self._grid_outlets

    @grid_outlets.setter
    def grid_outlets(self, list_):
        print("here : ", list_)
        self._grid_outlets = list_

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, a):
        self._action = a

    @property
    def action_value(self):
        return self._action_value

    @action_value.setter
    def action_value(self, a):
        self._action_value = a

    def replay_buffer_decentralize(self, batch_size, model):
        minibatch = random.sample(self.memory, batch_size)
        target = 0
        for state, action, reward, next_state in minibatch:
            target = reward
            if next_state is not None:
                next_state = np.array(next_state).reshape([1, np.array(next_state).shape[0]])
                # print("reward : ",reward)
                # print("model.predict(next_state, verbose=0)[0] : ",model.predict(next_state, verbose=0)[0])
                target = reward + self.gamma * np.argmax(model.predict(next_state, verbose=0)[0])
                # print("decentralize q value : ", target)
            state = np.array(state).reshape([1, np.array(state).shape[0]])
            target_f = np.round(model.predict(state, verbose=0))
            target_f[0][action] = target
            model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay
        return target

    def replay_buffer_centralize(self, batch_size, model):
        minibatch = random.sample(self.memory, batch_size)
        target = []
        for state, action, reward, next_state in minibatch:
            target = reward
            if next_state is not None:
                next_state = np.array(next_state).reshape([1, np.array(next_state).shape[0]])
                target = reward + self.gamma * np.argmax(model.predict(next_state, verbose=0)[0])
                # print("centralize q value : ", target)
            state = np.array(state).reshape([1, np.array(state).shape[0]])
            target_f = np.round(model.predict(state, verbose=0))
            target_f[0][action] = target
            # target = np.array(target).reshape([1, 9])
            model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay
        return target

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))

    def chain(self, model, state, epsilon):
        "A chain with a default first successor"
        test = np.random.rand()
        "Setting the first successor that will modify the payload"
        action = self.action
        handler = Exploit(action, model, state, Explore(action, FallbackHandler(action)))
        return action, np.where(handler.handle(test, epsilon) > 0.5, 1, 0)
