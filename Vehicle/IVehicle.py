from abc import ABC
from typing import List


class Vehicle(ABC):
    # TODO: replace int with road object in annotation
    def __init__(self, _id: int, speed: float, position: List[float],
                 acceleration: float, path: List[int], **kwargs):
        """
           Parameters
           ----------
            speed : float
               The frequency used by the service.
            position : list
               x,y coordinates of the vehicle in the environment
            acceleration : float
               at how mush rate the vehicle increments it's speed
            path : list[Road]
                roads path of the vehicle
            services : list[Service]

        """
        self.speed = speed
        self.position = position
        self.acceleration = acceleration
        self.path = path
        self.services = kwargs.get('services', [])
