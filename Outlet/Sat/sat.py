from Outlet.IOutlet import Outlet


class Satellite(Outlet):
    """
    outlet from type Satellite is the abstract class for UAV
    """


    def calculate_coverage_area(self):
        """Returns
            -------
            nothing , it is an abstract method
               The coverage area that the tower will response the requests in it."""
        pass

    def calculate_downlink(self):
        """Returns
            -------
            nothing , it is an abstract method
               The downlink that the tower will use it for responsing the requests ."""
        pass
