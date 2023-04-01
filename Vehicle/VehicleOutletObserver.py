from Environment.env_variables import outlet_radius


class Observer:
    def update(self, subject):
        pass


class ConcreteObserver(Observer):
    def __init__(self, outlet_pos, outlets):
        self.outlet_radius = outlet_radius
        self.outlet_pos = outlet_pos
        self.outlets = outlets

    def check(self, subject):
        def check_radius(i, outlet):
            print(i,outlet)
            if (outlet[0] - self.outlet_radius[i]) <= subject.x <= (
                outlet[0] + self.outlet_radius[i]
            ) and (outlet[1] - self.outlet_radius[i]) <= subject.y <= (
                outlet[1] + self.outlet_radius[i]
            ):
                return self.outlets[i]
        subject.outlets_serve = list(map(lambda outlet: check_radius(outlet[0], outlet[1]),enumerate(self.outlet_pos)))

    def update(self, subject):
        self.check(subject)
