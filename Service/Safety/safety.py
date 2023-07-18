from Service.IService import Service


class FactorySafety(Service):
    def __init__(self,*args):
        super().__init__(*args)
        self._task_complexity = 0
        self._network_latency = 0
        # add weights for each parameter

    def calcualate_processing_time(self):
        return self._network_latency + self._task_complexity
    def calculate_arrival_rate(self):
        # TODO: add doc string

        return 2
