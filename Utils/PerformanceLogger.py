import inspect
import warnings
from dataclasses import dataclass, field
from typing import List, Dict
from RL.Agent.Agent import Agent
from Vehicle.IVehicle import Vehicle
from Service.IService import Service
from Outlet.IOutlet import Outlet


class SingletonMeta(type):
    """
    Metaclass that ensures only one instance of a class is created.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


@dataclass
class PerformanceLogger(metaclass=SingletonMeta):
    _services_type: str = ""
    requested_services: List[Dict[Vehicle, Service]] = field(default_factory=list)
    handled_services: Dict[Outlet, Dict[Vehicle, Service]] = field(default_factory=dict)

    _outlet_services_power_allocation: Dict[Outlet, List[float]] = field(default_factory=dict)
    _outlet_services_power_allocation_current: Dict[Outlet, List[float]] = field(default_factory=dict)

    _outlet_services_requested_number: Dict[Outlet, List[int]] = field(default_factory=dict)
    _outlet_services_ensured_number: Dict[Outlet, List[int]] = field(default_factory=dict)
    _outlet_services_requested_number_with_action_period: Dict[Outlet, List[int]] = field(default_factory=dict)
    _outlet_services_ensured_number_with_action_period: Dict[Outlet, List[int]] = field(default_factory=dict)
    _outlet_services_power_allocation_with_action_period: Dict[Service, float] = field(default_factory=dict)
    _outlet_services_power_allocation_for_all_requested: Dict[Service, List[float]] = field(default_factory=dict)

    _outlet_occupancy: Dict[Outlet, float] = field(default_factory=dict)
    _outlet_utility: Dict[Outlet, float] = field(default_factory=dict)
    _gridcell_utility: Dict[Outlet, float] = field(default_factory=dict)
    _decentralized_reward: Dict[Agent, float] = field(default_factory=dict)
    _decentralize_z_c: Dict[Outlet, int] = field(default_factory=dict)
    _decentralize_action_value: Dict[Outlet, int] = field(default_factory=dict)
    _centralized_reward: Dict[Agent, float] = field(default_factory=dict)
    _service_power_allocate: Dict[Service, float] = field(default_factory=dict)
    _request_costs: List[int] = field(default_factory=list)
    _power_costs: List[float] = field(default_factory=list)
    served_ratio: List[float] = field(default_factory=list)

    @property
    def gridcell_utility(self):
        return self._gridcell_utility

    def set_gridcell_utility(self, outlet, utility):
        if outlet not in self._gridcell_utility:
            self._gridcell_utility[outlet] = {}
        self._gridcell_utility[outlet] = utility

    @property
    def decentralize_z_c(self):
        return self._decentralize_z_c

    def set_decentralize_z_c(self, outlet, value):
        if outlet not in self._decentralize_z_c:
            self._decentralize_z_c[outlet] = {}
        self._decentralize_z_c[outlet] = value

    @property
    def decentralize_action_value(self):
        return self._decentralize_action_value

    def set_decentralize_action_value(self, outlet, value):
        if outlet not in self._decentralize_action_value:
            self._decentralize_action_value = {}
        self._decentralize_action_value[outlet] = value

    @property
    def service_power_allocate(self):
        return self._service_power_allocate

    def set_service_power_allocate(self, outlet, cost):
        if outlet not in self._service_power_allocate:
            self._service_power_allocate[outlet] = {}
        self._service_power_allocate[outlet] = cost

    @property
    def outlet_services_power_allocation_current(self):
        return self._outlet_services_power_allocation_current

    def set_outlet_services_power_allocation_current(self, outlet, cost):
        if outlet not in self._outlet_services_power_allocation_current:
            self._outlet_services_power_allocation_current[outlet] = {}
        self._outlet_services_power_allocation_current[outlet] = cost

    @property
    def centralized_reward(self):
        return self._centralized_reward

    def set_centralized_reward(self, outlet, reward):
        if outlet not in self._centralized_reward:
            self._centralized_reward[outlet] = {}
        self._centralized_reward[outlet] = reward

    @property
    def decentralized_reward(self):
        return self._decentralized_reward

    def set_decentralized_reward(self, outlet, reward):
        if outlet not in self._decentralized_reward:
            self._decentralized_reward[outlet] = {}
        self._decentralized_reward[outlet] = reward

    @property
    def outlet_occupancy(self):
        return self._outlet_occupancy

    def set_outlet_occupancy(self, outlet, occupancy):
        if outlet not in self._outlet_occupancy:
            self._outlet_occupancy[outlet] = {}
        self._outlet_occupancy[outlet] = occupancy

    @property
    def outlet_utility(self):
        return self._outlet_utility

    def set_outlet_utility(self, outlet, utility):
        if outlet not in self._outlet_utility:
            self._outlet_utility[outlet] = {}
        self._outlet_utility[outlet] = utility

    @property
    def services_type(self):
        return self._services_type

    @services_type.setter
    def services_type(self, value):
        self._services_type = value

    @property
    def outlet_services_ensured_number(self):
        return self._outlet_services_ensured_number

    def set_outlet_services_ensured_number(self, outlet, num):
        if outlet not in self._outlet_services_ensured_number:
            self._outlet_services_ensured_number[outlet] = {}
        self._outlet_services_ensured_number[outlet] = num

    @property
    def outlet_services_requested_number(self):
        return self._outlet_services_requested_number

    def set_outlet_services_requested_number(self, outlet, num):
        if outlet not in self._outlet_services_requested_number:
            self._outlet_services_requested_number[outlet] = {}
        self._outlet_services_requested_number[outlet] = num

    @property
    def outlet_services_power_allocation(self):
        return self._outlet_services_power_allocation

    def set_outlet_services_power_allocation(self, outlet, service):
        if outlet not in self._outlet_services_power_allocation:
            self._outlet_services_power_allocation[outlet] = {}
        self._outlet_services_power_allocation[outlet] = service

    @property
    def outlet_services_ensured_number_with_action_period(self):
        return self._outlet_services_ensured_number_with_action_period

    def set_outlet_services_ensured_number_with_action_period(self, outlet, num):
        if outlet not in self._outlet_services_ensured_number_with_action_period:
            self._outlet_services_ensured_number_with_action_period[outlet] = {}
        self._outlet_services_ensured_number_with_action_period[outlet] = num

    @property
    def outlet_services_requested_number_with_action_period(self):
        return self._outlet_services_requested_number_with_action_period

    def set_outlet_services_requested_number_with_action_period(self, outlet, num):
        if outlet not in self._outlet_services_requested_number_with_action_period:
            self._outlet_services_requested_number_with_action_period[outlet] = {}
        self._outlet_services_requested_number_with_action_period[outlet] = num

    @property
    def outlet_services_power_allocation_with_action_period(self):
        return self._outlet_services_power_allocation_with_action_period

    def set_outlet_services_power_allocation_with_action_period(self, outlet, service):
        if outlet not in self._outlet_services_power_allocation_with_action_period:
            self._outlet_services_power_allocation_with_action_period[outlet] = {}
        self._outlet_services_power_allocation_with_action_period[outlet] = service

    @property
    def outlet_services_power_allocation_for_all_requested(self):
        return self._outlet_services_power_allocation_for_all_requested

    def set_outlet_services_power_allocation_for_all_requested(self, outlet, service):
        if outlet not in self._outlet_services_power_allocation_for_all_requested:
            self._outlet_services_power_allocation_for_all_requested[outlet] = {}
        self._outlet_services_power_allocation_for_all_requested[outlet]=service

    @property
    def service_requested(self):
        return self.requested_services

    @service_requested.setter
    def service_requested(self, value):
        self.requested_services.append(value)

    @property
    def service_handled(self):
        return self.handled_services

    def set_service_handled(self, outlet, car, service):
        if outlet not in self.handled_services:
            self.handled_services[outlet] = {}
        new_value = {car : service}
        self.handled_services[outlet].update(new_value)


    @property
    def request_costs(self):
        return self._request_costs

    @request_costs.setter
    def request_costs(self, value):
        print("inside request cost setter  :  >>>>> ", value)
        self._request_costs.append(value)

    @property
    def power_costs(self) -> List[float]:
        return self._power_costs

    @power_costs.setter
    def power_costs(self, value: List[float] | int) -> None:
        if not isinstance(value, List):
            self._power_costs.append(value)
            current_frame = inspect.currentframe()
            lineno = current_frame.f_back.f_lineno
            warnings.warn_explicit(
                "power cost should be appended and not set",
                category=UserWarning,
                filename=__file__,
                lineno=lineno,
            )
        else:
            self._power_costs.extend(value)

    def reset_state_decentralize_requirement(self):
        for key in self._outlet_services_requested_number:
            self._outlet_services_requested_number[key] = [0, 0, 0]
        for key in self._outlet_services_ensured_number:
            self._outlet_services_ensured_number[key] = [0, 0, 0]
        for key in self._outlet_services_power_allocation:
            self._outlet_services_power_allocation[key] = [0, 0, 0]
        for key in self.handled_services:
            self.handled_services[key] = {}
