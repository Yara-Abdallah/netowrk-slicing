from Vehicle.IVehicle import Vehicle
class Car(Vehicle):
    def __init__(self,_id, speed, position, acceleration, services_list, available_roads):
        super().__init__(_id, speed, position, acceleration, services_list, available_roads)