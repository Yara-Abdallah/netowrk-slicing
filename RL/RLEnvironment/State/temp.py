import copy

import numpy as np
import rx
import rx.operators as ops

from Communications.BridgeCommunications.ComsThreeG import ComsThreeG
from Outlet.Cellular.ThreeG import ThreeG
from RL.RLEnvironment.State.State import State


class CentralizedState(State):
    allocated_power: [float]
    supported_services: [bool]
    indices = []
    accumulated_powers = []
    filtered_powers = []

    def __init__(self):
        super().__init__()
        self.gridCell = 2
        self.num_services = 3
        self.state_shape = CentralizedState.state_shape(self.num_services, self.gridCell)
        self._allocated_power = np.zeros(self.state_shape)
        self._supported_services = copy.deepcopy(self.allocated_power)

    @staticmethod
    def state_shape(num_services, gridCell):
        return [num_services, gridCell]

    @property
    def allocated_power(self):
        return self._allocated_power

    @property
    def supported_services(self):
        return self._supported_services

    @allocated_power.setter
    def allocated_power(self, power_array):
        self._allocated_power[:, power_array[1]] = power_array[0]

    @supported_services.setter
    def supported_services(self, supported_array):
        self._supported_services[:, supported_array[1]] = supported_array[0]

    def observer_sum(self, x):
        self.accumulated_powers.append(sum(x))

    def filter_power(self, x):
        print("... ", x[0], "    ", x[1])
        self.indices.append(x)

        x = list(map(self.filtered_powers[x[0]].__getitem__, x[1]))
        return x

    def calculate_state(self, binary):
        xs = rx.from_(binary)
        disposable = xs.pipe(
            ops.map_indexed(
                lambda x, i: (i, np.where(np.array(x) == 1.0))),

            ops.map(lambda x: [x[0], x[1][0]]),
            ops.map(self.filter_power))

        disposable.subscribe(self.observer_sum)
        return self.accumulated_powers


comm = ComsThreeG(0, 0, 0, 0, 0)
outlet = ThreeG(0, comm, [1, 1, 1], 1, 1, [10, 15, 22])
outlet2 = ThreeG(0, comm, [0, 0, 1], 1, 1, [10, 15, 28])

print(outlet.distinct)
print('..... ', outlet.power)
print(outlet2.distinct)
print('..... ', outlet2.power)

c = CentralizedState()
# print(c.calculate_state(4, 3))
c.allocated_power = outlet.power_distinct
c.supported_services = outlet.supported_services_distinct
c.allocated_power = outlet2.power_distinct
c.supported_services = outlet2.supported_services_distinct
print(c.allocated_power)
print(c.supported_services)
c.power = c.allocated_power
print(c.power)
print(c.calculate_state(c.supported_services))
# print(c.supported_services(*outlet.supported_services_distinct))
