from Outlet.Cellular.ICellular import Cellular


class Wifi(Cellular):

    def calculate_coverage_area(self):
        return 1

    def calculate_downlink(self):
        return 2
