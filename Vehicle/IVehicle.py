from abc import ABC


class Vehicle(ABC):
    def __init__(self, _id, speed, position, acceleration, services_list, available_roads):
        self.speed = speed
        self.position = position
        self.acceleration = acceleration
        self.services_list = services_list
        self.available_roads = available_roads
