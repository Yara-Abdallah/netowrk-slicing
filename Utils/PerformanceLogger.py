import inspect
import warnings
from dataclasses import dataclass, field
from typing import List, Dict

from Outlet.Cellular.FactoryCellular import FactoryCellular
from Service.Entertainment.Entertainment import FactoryEntertainment
from Vehicle.Car import Car
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
    requested_services: List[Dict[Vehicle, Service]] = field(default_factory=list)
    handled_services: Dict[Outlet, Dict[Vehicle, Service]] = field(default_factory=dict)
    _request_costs: List[int] = field(default_factory=list)
    _power_costs: List[float] = field(default_factory=list)
    served_ratio: List[float] = field(default_factory=list)

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
        self.handled_services[outlet][car] = service

    @property
    def request_costs(self):
        return self._request_costs

    @request_costs.setter
    def request_costs(self, value):
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

