import inspect
import warnings
from dataclasses import dataclass, field
from typing import List, Dict

from Outlet.IOutlet import Outlet
from Service.IService import Service
from Vehicle.Car import Car


@dataclass
class PerformanceLogger:
    service_requested: Dict[Car, Service] = field(default_factory=dict)
    services_requested: List[Dict[Car, Service]] = field(default_factory=list)
    services_handled: Dict[Outlet, Dict[Car, Service]] = field(default_factory=dict)
    request_costs: List[int] = field(default_factory=list)
    _power_costs: List[float] = field(default_factory=list)
    served_ratio: List[float] = field(default_factory=list)

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
                "power cost should be a appended and not set",
                category=UserWarning,
                filename=__file__,
                lineno=lineno,
            )
        else:
            self._power_costs.extend(value)





