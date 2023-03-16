from abc import ABC, abstractmethod

"""
    Project a point on the surface of a sphere

    Parameters
    ----------
    point : Tuple[float,float,float]
        The coordinates of the point in Cartesian coordinates.
    sphere_center : Tuple[float,float,float]
        The center of the sphere in Cartesian coordinates.
    sphere_radius : float
        The radius of the sphere.

    Returns
    -------
    Tuple[float,float,float]
        The coordinates of the point projected on the surface of the sphere in Cartesian coordinates.

    Remarks
    -------
    Works 2D and 3D

    """


class Communications(ABC):
    def __init__(self, frequency, bandwidth, data_rate, latency, radius, modulation, encryption, error_correction,
                 interference):
        self.frequency = frequency
        self.bandwidth = bandwidth
        self.data_rate = data_rate
        self.latency = latency
        self.radius = radius
        self.modulation = modulation
        self.encryption = encryption
        self.error_correction = error_correction
        self.interference = interference

    @abstractmethod
    def propagation_range(self):
        pass

    def calculate_data_rate(self):
        pass
