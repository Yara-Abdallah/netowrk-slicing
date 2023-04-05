import numpy as np
import random
from RL.Agent.IAgent import AbstractAgent
from RL.RLEnvironment.Action.ActionChain import Exploit, Explore, FallbackHandler


class Agent(AbstractAgent):
    _grid_outlets = []

    @property
    def grid_outlets(self):
        return self._grid_outlets

    @grid_outlets.setter
    def grid_outlets(self, list_):
        self._grid_outlets = list_

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, a):
        self._action = a

    def replay_buffer(self, batch_size, model):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state in minibatch:
            target = reward
            if next_state is not None:
                target = reward + self.gamma * np.max(model.predict(next_state, verbose=0)[0])
            target_f = model.predict(state, verbose=0)
            target_f[0][action] = target
            model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay

    def train(self,builder, **kwargs):
        ep_rewards = []
        for e in range(self.episodes):
            episode_reward = 0
            #state = builder.environment.state.resetState()
            state_value = builder.environment.state.calculate_state(builder.environment.state.supported_services)
            print("state value : ",state_value)
            print("state shape : ", np.array(state_value).shape[0])
            #state_value = np.array(state_value).reshape([1, np.array(state_value).shape[0]])
            for time in range(self.step):
                action, action_value = builder.agents.chain(builder.model, state_value, 0.1)
                print("action value : ", action_value)
                next_state = action.execute(builder.environment.state, action_value)
                print("next_state value : ", next_state)
                reward_value = builder.environment.reward.calculate_reward()
                print("reward value : ",reward_value)
                episode_reward += reward_value
                #next_state = np.reshape(next_state, [1, np.array(next_state).shape[1]])
                builder.agents.remember(state_value, action_value, reward_value, next_state)
                state_value = next_state
            ep_rewards.append(episode_reward)
            if len(builder.agents.memory) > self.batch_size:
                builder.agents.replay_buffer(self.batch_size, builder.model)

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))

    def chain(self, model, state, epsilon):
        "A chain with a default first successor"
        test = np.random.rand()
        "Setting the first successor that will modify the payload"
        action = self.action
        print("inside chain ,,, ", action)
        handler = Exploit(action, model, state, Explore(action, FallbackHandler(action)))
        # = np.where(handler.handle(test, epsilon) > 0.5, 1, 0)
        # handler.handle(test, epsilon)
        return action, np.where(handler.handle(test, epsilon) > 0.5, 1, 0)
