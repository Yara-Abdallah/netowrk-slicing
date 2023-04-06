from keras import Sequential
from keras.layers import Dense, Reshape
from keras.optimizers import Adam


class Model():
    def __init__(self, state_size = 7, action_size = 1, activation_function = "relu", loss_function = "mse", optimization_algorithm = Adam,
                 learning_rate = 0.5, output_activation = "sigmoid", **kwargs):
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
        model_.add(Reshape((1,1)))
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
