from Environment.env_variables import outlet_radius
from Outlet.Cellular.FactoryCellular import FactoryCellular


class Observer:
    def update(self, subject):
        pass


class ConcreteObserver(Observer):
    def __init__(self, outlet_pos ,outlets):
        self.outlet_raduis = outlet_radius
        self.outlet_pos = outlet_pos
        self.outlets = outlets

    def check(self, subject):

        for i, o in enumerate(self.outlet_pos):
            if (subject.x >= (o[0] - self.outlet_raduis[i]) and subject.x <= (o[0] + self.outlet_raduis[i])) and (
                    subject.y >= (o[1] - self.outlet_raduis[i]) and subject.y <= (o[1] + self.outlet_raduis[i])):


                # print(self.outlet_pos)
                # factory = FactoryCellular(1, 1, [1, 1, 0], [o[0], o[1]], 10000, [10, 20, 30],
                #                           [10, 10, 10])
                #
                # outlet = factory.produce_cellular_outlet("5G")
                subject.outlets_serve.append(self.outlets[i])
            else:
                pass

    def update(self, subject):
        self.check(subject)



