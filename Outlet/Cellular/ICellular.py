from abc import abstractmethod
from Communications.IComs import Communications
from Outlet.IOutlet import Outlet


# noinspection PyAbstractClass
class Cellular(Outlet):

    """
    outlet from type cellular is the abstract class for different types ground towers
    """

    def __init__(self, agent, coms: Communications, supported_services, *args, **kwargs):
        """
            Parameters
            ----------
            agent : Agent
                RL agent from type outlet agent.
            coms : Communications
                the communication that will take the request to the outlet .
            supported_services : [bool]
                services that will the vehicle send it to outlet .
            services_list : [Services]
                services that will the vehicle send it to outlet (the outlet will responsed to it).
            vehicles_list : [Vehicles]
                The vehicles that demand a service from this outlet.

        """

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
