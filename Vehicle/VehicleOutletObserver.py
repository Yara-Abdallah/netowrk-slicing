from Outlet.Cellular.ThreeG import ThreeG
from Vehicle.Car import Car


class Observer:
    def update(self, subject):
        pass


class ConcreteObserver(Observer):
    def __init__(self):
        self.outlet_raduis = [20, 30, 40]
        self.outlet_pos = [[2, 2], [10, 5], [4, 8]]
        self.outlets = []

    def check(self, subject):
        for i, o in enumerate(self.outlets.position):
            print("subject.x : ", subject.x)
            print("o[0] : ", o[0])
            print("subject.y : ", subject.y)
            print("o[1] : ", o[1])
            if (subject.x >= (o[0] - self.outlets.radius[i]) and subject.x <= (o[0] + self.outlets.radius[i])) and (
                    subject.y >= (o[1] - self.outlets.radius[i]) and subject.y <= (o[1] + self.outlets.radius[i])):
                print("accepted .. (", subject.x, "  ", subject.y, ") in range ", (o[0] - self.outlets.radius[i]),
                      " to ", o[0] + self.outlets.radius[i])
                subject.services_list.append(o)
            else:
                print("else")

    def update(self, subject):
        self.check(subject)
        print("outlets can serve the vehicle is ", subject.services_list)


# Example usage

outlet1 = ThreeG(0, 1, [1, 1, 1], 1, 1, [10, 15, 22], [10, 20, 30])
outlet2 = ThreeG(0, 1, [1, 1, 1], 1, 1, [10, 15, 22], [10, 20, 30])
outlet3 = ThreeG(0, 1, [1, 1, 1], 1, 1, [10, 15, 22], [10, 20, 30])
outlet=[]
outlet.append(outlet1)
outlet.append(outlet2)
outlet.append(outlet3)

car = Car(0, [2, 3])
observer = ConcreteObserver()

car.attach(observer)

car.set_state(car.x, car.y)  # This should trigger the observer to update
