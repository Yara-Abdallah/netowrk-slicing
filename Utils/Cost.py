import os

from Utils.Bandwidth import Bandwidth
from dotenv import load_dotenv
import os
from Utils import config as cf

load_dotenv()


class Cost:
    def __init__(self, bandwidth: Bandwidth, realtime: int, logger) -> None:
        self.realtime = realtime
        self.bit_rate = bandwidth.allocated
        self._cost: float = 0.0
        self.logger = logger

    @property
    def cost(self):
        return self._cost

    def cost_setter(self, realtime_value):
        if realtime_value in cf.REALTIME_BANDWIDTH.get('WIFI'):
            self._cost = self.bit_rate
            self.logger.log(f"Set cost to {self._cost} for WIFI")
        elif realtime_value in cf.REALTIME_BANDWIDTH.get('3G'):
            self._cost = self.bit_rate * 1.1
            self.logger.log(f"Set cost to {self._cost} for 3G")
        elif realtime_value in cf.REALTIME_BANDWIDTH.get('4G'):
            self._cost = self.bit_rate * 1.3
            self.logger.log(f"Set cost to {self._cost} for 4G")
        elif realtime_value in cf.REALTIME_BANDWIDTH.get('5G'):
            self._cost = self.bit_rate * 1.5
            self.logger.log(f"Set cost to {self._cost} for 5G")
        elif realtime_value in cf.REALTIME_BANDWIDTH.get("SATELLITE"):
            self._cost = self.bit_rate * 2
            self.logger.log(f"Set cost to {self._cost} for SATELLITE")

    def __str__(self):
        raise NotImplementedError()


class RequestCost(Cost):

    @property
    def cost(self):
        cost = self._cost * float(os.getenv('MB_COST'))
        self.logger.log(f"RequestCost: {cost}")
        return cost

    def __str__(self):
        fee = self._cost * float(os.getenv("MB_COST"))
        self.logger.log(f"Request fee : {fee}")
        return f'Request Fee: {fee}'


class TowerCost(Cost):
    @property
    def cost(self):
        cost = self._cost * float(os.getenv('KW_COST'))
        self.logger.log(f"Tower Cost: {cost}")
        return cost

    def __str__(self):
        return f'Request Fee: {self.cost}'

from Utils.Log_ing import Logger , logger

log = Logger('cost.log',logger.INFO)
band=Bandwidth(2,3)
cost=Cost(band,3,log)
cost.cost_setter(9)
print(cost.cost)