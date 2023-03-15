from Outlet.Cellular.ICellular import Cellular


class ThreeG(Cellular):
    def __init__(self, agent, supported_services, services_list, vehicles_list):
        super().__init__()
        self.agent = agent
        self.supported_services = supported_services
        self.services_list = services_list
        self.vehicles_list = vehicles_list

    def calculate_coverage_area(self):
        return 1

    def calculate_downlink(self):
        return 2

