from abc import abstractmethod
from Communications.IComs import Communications
from Outlet.IOutlet import Outlet


# noinspection PyAbstractClass
class Cellular(Outlet):

    def __init__(self, agent, coms: Communications, supported_services, *args, **kwargs):
        super().__init__(*args)
        self.agent = agent
        self.coms = coms
        self.supported_services = supported_services
        self.services_list = kwargs.get('services_list', [])
        self.vehicles_list = kwargs.get('vehicles_list', [])

    @abstractmethod
    def calculate_coverage_area(self):

        pass

    @abstractmethod
    def calculate_downlink(self):
        pass

    pass
