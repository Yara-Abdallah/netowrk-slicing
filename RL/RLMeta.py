from abc import ABCMeta, abstractmethod

from keras import Sequential
from keras.layers import Dense
from keras.optimizer_v2.adam import Adam


class RLMeta(type):
    def __new__(yara, name, bases, class_dict):
        class_ = super().__new__(yara, name, bases, class_dict)
        yara.agent = []
        yara.env = 'not yara'
        # call the parent class's __new__ method to create the class

        # make sure the new class has agent and env attributes
        if not hasattr(class_, 'agent') or not hasattr(class_, 'env'):
            raise NotImplementedError("Classes with RLMeta as metaclass must have 'agent' and 'env' attributes")

        return class_

    def get_agent_observation(cls):
        if cls.agent is None:
            raise ValueError("Agent is not initialized")
        print(cls.agent)

    def get_env_observation(cls):
        if cls.env is None:
            raise ValueError("Env is not initialized")
        return cls.env.observe()


def rlabc(cls):
    return ABCMeta(cls.__name__, cls.__bases__, dict(cls.__dict__))


@rlabc
class AbstractModel(metaclass=RLMeta):
    def __init__(self, state_size, action_size, activation_function, loss_function, optimization_algorithm,
                 learning_rate, output_activation, **kwargs):
        self.state_size = state_size
        self.action_size = action_size
        self.activation_function = activation_function
        self.loss_function = loss_function
        self.optimization_algorithm = optimization_algorithm
        self.learning_rate = learning_rate
        self.output_activation = output_activation

    def load(self, filename):
        """ Load model from file. """
        pass

    def save(self, filename):
        """ Save model to file. """

        pass

    @abstractmethod
    def create_model(self):
        pass

    @abstractmethod
    def predict(self, state):
        """ Predict value based on state. """
        pass


class DQN(AbstractModel):
    def __init__(self, *args):
        super().__init__(*args)

        self.model = self.create_model()

    def create_model(self) -> Sequential:
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation=self.activation_function))
        model.add(Dense(24, activation=self.activation_function))
        model.add(Dense(self.action_size, activation=self.output_activation))
        model.compile(loss=self.loss_function, optimizer=self.optimization_algorithm(learning_rate=self.learning_rate))
        return model

    # def load(self):
    #     self.load_weights(name)
    #
    # def save(self, filename):
    #     self.model.load_weights(name)


a = DQN(2, 2, 'relu', 'mse', Adam, 0.5, 'linear')
print(a.model.summary())
