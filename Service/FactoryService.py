from Service.Entertainment.Entertainment import FactoryEntertainment
from Service.Safety.safety import FactorySafety
from Service.Telecomm.telecomm import FactoryTelecomm


# noinspection PyAbstractClass
class FactoryService:
    def __init__(self, *args):
        """
        *args: params
            Service init parameters; reference to Iservice.py
        """

        self.entertainment = FactoryEntertainment(*args)
        self.safety = FactorySafety(*args)
        self.telecom = FactoryTelecomm(*args)
        self.var = {"entertainment": self.entertainment,
                    "safety": self.safety,
                    "telecom": self.telecom}

    def produce_services(self, product):
        if product in self.var.keys():
            return self.var[product]
        raise Exception(f'{product} factory not available at the moment!')
