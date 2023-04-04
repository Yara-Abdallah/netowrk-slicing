from abc import ABCMeta, abstractmethod

from keras import Sequential
from keras.layers import Dense, Reshape
from numpy import ndarray

from RL.RLMeta import RLMeta, rlabc


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

    def build_model(self) -> Sequential:
        model_ = Sequential()
        model_.add(Dense(24, input_dim=self.state_size, activation=self.activation_function))
        model_.add(Dense(24, activation=self.activation_function))
        model_.add(Dense(self.action_size, activation=self.output_activation))
        model_.add(Reshape((3, 3)))
        model_.compile(loss=self.loss_function,
                       optimizer=self.optimization_algorithm(learning_rate=self.learning_rate))
        return model_

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
