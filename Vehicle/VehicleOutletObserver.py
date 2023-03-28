from Environment.env_variables import outlet_radius

class Observer:
    def update(self, subject):
        pass


class ConcreteObserver(Observer):
    def __init__(self, outlet_pos):
        self.outlet_raduis = outlet_radius
        self.outlet_pos = outlet_pos

    def check(self, subject):

        for i, o in enumerate(self.outlet_pos):
            if (subject.x >= (o[0] - self.outlet_raduis[i]) and subject.x <= (o[0] + self.outlet_raduis[i])) and (
                    subject.y >= (o[1] - self.outlet_raduis[i]) and subject.y <= (o[1] + self.outlet_raduis[i])):
                subject.outlets_serve.append(o)
            else:
                pass
        print("the serve outlets    .......    ", len(subject.outlets_serve))

    def update(self, subject):
        self.check(subject)



