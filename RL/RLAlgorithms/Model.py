from abc import ABCMeta, abstractmethod
from RL.RLMeta import RLMeta, rlabc


@rlabc
class Model():
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
        self.load_weights(filename)
        pass

    def save(self, filename):
        """ Save model to file. """
        self.load_weights(filename)
        pass

    def predict(self, state):
        """ Predict value based on state. """
        pass
