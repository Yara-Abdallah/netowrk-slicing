import random

from Service.FactoryService import FactoryService
from Vehicle.IVehicle import Vehicle
from Utils.config import SERVICES_TYPES
import numpy as np

from Vehicle.VehicleOutletObserver import ConcreteObserver


class Car(Vehicle):

    def __str__(self):
        return f"car id : {self.id}  ,  outlets list which can serve the requests from this vehicle " \
               f": {self.outlets_serve}  , the requestes sent by this vehicle : {self.car_requests()} "

    def car_requests(self):

        service_mapping_car=[]
        types = ["ENTERTAINMENT", "SAFETY", "AUTONOMOUS"]


        for i in range(10):
            type_ = random.choice(types)
            factory = FactoryService(SERVICES_TYPES[type_]["REALTIME"],
                                     SERVICES_TYPES[type_]["BANDWIDTH"],
                                     SERVICES_TYPES[type_]["CRITICAL"])
            self.services.append(factory.produce_services(type_))
        for id,serv in enumerate(self.services) :
            service_mapping_car.append([self.__class__,serv])
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


car = Car(1)
observer = ConcreteObserver([[10, 10], [0, 1]])
car.attach(observer)
car.set_state(1, 1)
print(car.car_requests())
#print(car.send_request())
