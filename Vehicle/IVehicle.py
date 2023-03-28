from abc import ABC
from typing import List


class Vehicle(ABC):
    # TODO: replace int with road object in annotation
    def __init__(self, _id: int,position: List[float], **kwargs):
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
        self.position = position
        self.services = kwargs.get('services', [])
        self.observers = []
        self.x = None
        self.y = None

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update(self)

    def set_state(self, x, y):
        self.x = x
        self.y = y
        self.notify()

    @property
    def x(self):
        return self.x

    @property
    def y(self):
        return self.y

    @x.setter
    def x(self,v):
        self.x=v

    @y.setter
    def y(self, v):
        self.y = v

