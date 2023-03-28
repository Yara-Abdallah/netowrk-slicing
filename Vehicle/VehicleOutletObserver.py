class Observer:
    def update(self, subject):
        pass


class ConcreteObserver(Observer):
    def __init__(self, outlets):
        self.outlet_raduis = [1000] * 39
        self.outlet_pos = outlets

    def check(self, subject):

        for i, o in enumerate(self.outlet_pos):
            # print("subject.x : ", subject.x)
            # print("o[0] : ", o[0])
            # print("subject.y : ", subject.y)
            # print("o[1] : ", o[1])
            if (subject.x >= (o[0] - self.outlet_raduis[i]) and subject.x <= (o[0] + self.outlet_raduis[i])) and (
                    subject.y >= (o[1] - self.outlet_raduis[i]) and subject.y <= (o[1] + self.outlet_raduis[i])):
                #print("accepted .. (", subject.x, "  ", subject.y, ") in range ", (o[0] - self.outlet_raduis[i])," to ", o[0] + self.outlet_raduis[i])
                subject.outlets_serve.append(o)
            else:
                pass
                #print("else")
        print("the serve outlets    .......    ", len(subject.outlets_serve))

    def update(self, subject):
        self.check(subject)



