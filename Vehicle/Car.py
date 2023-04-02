import random
import math
from Service.FactoryService import FactoryService
from Vehicle.IVehicle import Vehicle
from Utils.config import SERVICES_TYPES


class Car(Vehicle):
    def car_requests(self):
        self.services = []
        car_services = []
        types = [*SERVICES_TYPES.keys()]

        # for i in range(10):

        type_ = random.choice(types)
        factory = FactoryService(
            random.choice(SERVICES_TYPES[type_]["REALTIME"]),
            random.choice(SERVICES_TYPES[type_]["BANDWIDTH"]),
            random.choice(SERVICES_TYPES[type_]["CRITICAL"]),
        )
        self.services.append(factory.produce_services(type_))
        car_services = list(map(lambda x: [self.get_id(), self, x], self.services))
        return car_services

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
        def euclidian_distance(outlet):
            #print('sh', outlet)
            result = math.sqrt(
                (outlet.position[0] - self.x) ** 2 + (outlet.position[1] - self.y) ** 2
            )
            return result

        distance = list(map(lambda x: euclidian_distance(x), self.outlets_serve))
        return self.outlets_serve[distance.index(min(distance))]

    def send_request(self):
        outlet = self.greedy()
        outlet.services = []
        outlet.services.extend([outlet, self.car_requests()[0]])
        return outlet.services


# car = Car(1, 1, 1)
# observer = ConcreteObserver([[10, 10], [0, 1]], [ThreeG(outlet_types.get("3G"), 2, 3, 4, [5,3], 6, 7, 8),ThreeG(outlet_types.get("3G"), 2, 3, 4, [30,90], 6, 7, 8)])
# car.attach(observer)
# car.set_state(1, 1)
# print(car.send_request())
# print(car.send_request())
