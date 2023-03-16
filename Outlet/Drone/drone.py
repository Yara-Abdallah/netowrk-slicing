from Outlet.IOutlet import Outlet

class Drone(Outlet):
    """
    outlet from type Air is the abstract class for UAV
    """
    def __init__(self, coms, height, data_rate, radius,*args):

        """
            Parameters
            ----------
            height : float
                height of zone that the drone will coverage it.
            data_rate : float
                the data rate of transition the request .
            radius : float
                radius of coverage area .
            coms : Communications
                the type of communication that will transfer the request.

        """
        super().__init__(*args)
        self.height = height
        self.data_rate = data_rate
        self.radius = radius
        self.coms = coms


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


