import os
from dotenv import load_dotenv

load_dotenv()


class Bandwidth:
    _allocated: float

    def __init__(self, bandwidth_demand: int, criticality: int) -> None:
        self.bandwidth_demand = bandwidth_demand
        self.criticality = criticality

    @property
    def allocated(self):
        total_bandwidth = self.bandwidth_demand * float(os.getenv('BANDWIDTH_MIN'))
        change_in_bandwidth = self.criticality * total_bandwidth * float(os.getenv('CRITICAL_MIN'))
        self._allocated = total_bandwidth + change_in_bandwidth
        return self._allocated
