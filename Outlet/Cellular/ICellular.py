from Outlet.IOutlet import Outlet


# noinspection PyAbstractClass
class Cellular(Outlet):
    _id, position, radius, power = 0,0,0,0
    def __init__(self, agent, supported_services, services_list, vehicles_list,*args):
        super().__init__(*args)
        self.agent = agent
        self.supported_services = supported_services
        self.services_list = services_list
        self.vehicles_list = vehicles_list

    pass
