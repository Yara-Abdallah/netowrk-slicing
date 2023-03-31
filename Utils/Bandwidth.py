import os
from dotenv import load_dotenv

load_dotenv()


class Bandwidth:
    def __init__(self, bandwidth_demand: int, criticality: int) -> None:
        self.bandwidth_demand = bandwidth_demand
        self.criticality = criticality
        self._allocated: int = 0

    @property
    def allocated(self):
        total_bandwidth = self.bandwidth_demand * 10
        change_in_bandwidth = self.criticality * total_bandwidth * 0.03
        #print(f"change amount in bandwidth (capacity) is >> : {change_in_bandwidth} MBps")
        total_bandwidth = total_bandwidth + change_in_bandwidth
        #print(f"new bandwidth (capacity) is >> : {total_bandwidth} MBps")
        self._allocated = total_bandwidth
        return self._allocated
