from abc import ABC
from Service.IService import Service

from Service.Entertainment.Entertainment import FactoryEntertainment
from Service.Safety.safety import FactorySafety
from Service.Telecomm.telecomm import FactoryTelecomm


# noinspection PyAbstractClass
class FactoryService():
    def __init__(self, *args):
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
