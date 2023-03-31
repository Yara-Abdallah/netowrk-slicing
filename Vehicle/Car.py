import random
import math

from Outlet.Cellular.FactoryCellular import FactoryCellular
from Service.FactoryService import FactoryService
from Vehicle.IVehicle import Vehicle
from Utils.config import SERVICES_TYPES
import numpy as np

from Vehicle.VehicleOutletObserver import ConcreteObserver


class Car(Vehicle):
    # def __str__(self):
    #     return (
    #         f"car id : {self.id}  ,  outlets list which can serve the requests from this vehicle "
    #         f": {self.outlets_serve}  , the requestes sent by this vehicle : {self.car_requests()} "
    #     )

    def car_requests(self):
        self.services=[]
        service_mapping_car = []
        types = ["ENTERTAINMENT", "SAFETY", "AUTONOMOUS"]

        # for i in range(10):
        type_ = random.choice(types)
        factory = FactoryService(SERVICES_TYPES[type_]["REALTIME"],
                                 SERVICES_TYPES[type_]["BANDWIDTH"],
                                 SERVICES_TYPES[type_]["CRITICAL"])
        self.services.append(factory.produce_services(type_))
        for id, serv in enumerate(self.services):
            #print("service ...... ",serv)
            service_mapping_car.append([self.get_id(), self, serv])
        return service_mapping_car

    # def send_request(self):
    #     mapping  = dict(map(lambda x: (random.choice(self.services), x), self.outlets_serve))
    #     return mapping
    def get_id(self):
        return self.id

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

    def greedy(self):
        distance = []
        for i, outlet in enumerate(self.outlets_serve):
            distance.append(math.sqrt((outlet.position[0] - self.x) ** 2 + (outlet.position[1] - self.y) ** 2))
        return self.outlets_serve[distance.index(min(distance))]

    def send_request(self):
        outlet = self.greedy()
        outlet.services = []
        outlet.services.extend([outlet,self.car_requests()[0]])
        return outlet.services

#
# car = Car(1, 1, 1)
# observer = ConcreteObserver([[10, 10], [0, 1]])
# car.attach(observer)
# car.set_state(1, 1)
# print(car.send_request())
# print(car.send_request())
