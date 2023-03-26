from abc import ABC, abstractmethod


class Service(ABC):

    def __init__(self, frequency: float, spectrum: float, data_rate: float, energy_consumption: float,
                 transition_delay: float,power_factor:float, **kwargs):
        """
            Parameters
            ----------
            frequency : float
                The frequency used by the service.
            spectrum : float
                Represents the collection of frequencies that make up a signal and their relative strengths.
            data_rate : float
                The data rate of the service
            energy_consumption : float
                The energy consumed by the service
            transition_delay : float
                The transition delay of the service
            communications : list[Communication]
                The communications that supported the service if not initialized set to empty array to be appended at runtime

            """
        self.frequency = frequency
        self.spectrum = spectrum
        self.data_rate = data_rate
        self.energy_consumption = energy_consumption
        self.transition_delay = transition_delay
        self.communication = kwargs.get('communications', [])
        self.power_factor = power_factor

    @abstractmethod
    def calculate_arrival_rate(self):
        """ the rate at which messages or packets are received by a system or a network over a period of time """
        pass
