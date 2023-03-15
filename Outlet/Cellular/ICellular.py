from Outlet.IOutlet import Outlet

#noinspection PyAbstractClass
class Cellular(Outlet):

    def __init__(self, agent, supported_services, services_list, vehicles_list):
        super().__init__(_id, position, radius, power)
        self.agent = agent
        self.supported_services = supported_services
        self.services_list = services_list
        self.vehicles_list = vehicles_list

    pass
