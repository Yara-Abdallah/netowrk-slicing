from abc import ABC
from typing import List

import traci


class Vehicle(ABC):
    # TODO: replace int with road object in annotation
    def __init__(self, id_, route_, **kwargs):
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

        self.id = id_
        self.route = route_
        self.services = kwargs.get('services', [])
        self.outlets_serve = []
        self.observers = []
        traci.vehicle.add(id_, route_)
        position = traci.vehicle.getPosition(id_)
        self.x = position[0]
        self.y = position[1]
