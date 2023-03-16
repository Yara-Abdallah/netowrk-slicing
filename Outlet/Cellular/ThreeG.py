from Outlet.Cellular.ICellular import Cellular


class ThreeG(Cellular):

    def calculate_coverage_area(self):
        print(",,,,,,,,,,,,",self.coms.calculate_data_rate())

    def calculate_downlink(self):
        return 2
