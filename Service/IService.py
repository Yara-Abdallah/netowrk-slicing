from abc import ABC, abstractmethod


class Service(ABC):
    def __init__(self, frequency, spectrum, data_rate, energy_consumption, transition_delay, list_communication):
        self.frequency = frequency
        self.spectrum = spectrum
        self.data_rate = data_rate
        self.energy_consumption = energy_consumption
        self.transition_delay = transition_delay
        self.list_communication = list_communication

    @abstractmethod
    def calculate_arrival_rate(self):
        pass
