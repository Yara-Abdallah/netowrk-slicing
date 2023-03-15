from .FiveG import FiveG
from .FourG import FourG
from .SubSixG import SubSixG
from .ThreeG import ThreeG
from .Wifi import Wifi


class FactoryCellular:
    def __init__(self, *args):
        self.three_gen = ThreeG(*args)
        self.four_gen = FourG(*args)
        self.five_gen = FiveG(*args)
        self.sub_six = SubSixG(*args)
        self.wifi = Wifi(*args)
        self.cellular_dict = {'3G': self.three_gen,
                              '4G': self.four_gen,
                              '5G': self.five_gen,
                              'Sub6G': self.sub_six,
                              'Wifi': self.wifi}

    def produce_cellular_outlet(self, product):
        if product in self.cellular_dict:
            return self.cellular_dict[product]
        raise Exception(f'{product} factory not available at the moment!')
