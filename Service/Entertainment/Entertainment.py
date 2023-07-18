from Service.IService import Service


class FactoryEntertainment(Service):
    """
    params: *args
        Service init parameters; reference to Iservice.py
    """
    def __init__(self,*args):
        super().__init__(*args)
        self._data_size = 0
        self._network_latency = 0
        # add weights for each parameter


    def calcualate_processing_time(self):
        return self._network_latency + self._data_size
    def calculate_arrival_rate(self):
        # TODO: add doc string
        return 1
