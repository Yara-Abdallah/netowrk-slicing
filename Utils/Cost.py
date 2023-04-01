import os

from Utils.Bandwidth import Bandwidth
from dotenv import load_dotenv
import os
from Utils import config as cf
from Utils.FileLogging import log_method

load_dotenv()


class Cost:
    def __init__(self, bandwidth: Bandwidth, realtime: int) -> None:
        self.realtime = realtime
        self.bit_rate = bandwidth.allocated
        self._cost: float = 0.0
        # self.logger = logger

    # @log_method
    @property
    def cost(self):
        return self._cost

    def cost_setter(self, realtime_value):
        if realtime_value in cf.REALTIME_BANDWIDTH.get('WIFI'):
            self._cost = self.bit_rate
        elif realtime_value in cf.REALTIME_BANDWIDTH.get('3G'):
            self._cost = self.bit_rate * 1.1
        elif realtime_value in cf.REALTIME_BANDWIDTH.get('4G'):
            self._cost = self.bit_rate * 1.3
        elif realtime_value in cf.REALTIME_BANDWIDTH.get('5G'):
            self._cost = self.bit_rate * 1.5
        elif realtime_value in cf.REALTIME_BANDWIDTH.get("SATELLITE"):
            self._cost = self.bit_rate * 2

    def __str__(self):
        raise NotImplementedError()


class RequestCost(Cost):

    # @log_method
    @property
    def cost(self):
        cost = self._cost * float(os.getenv('MB_COST'))
        # self.logger.log(f"RequestCost: {cost}")
        return f'{cost:.2f}'

    # def __str__(self):
    #     fee = self._cost * float(os.getenv("MB_COST"))
    #     return f'Request Fee: {fee}'


class TowerCost(Cost):
    # @log_method
    @property
    def cost(self):
        cost = self._cost * float(os.getenv('KW_COST'))
        return cost

    # def __str__(self):
    #     return f'Request Fee: {self.cost}'

#
# band = Bandwidth(2, 3)
# tow=TowerCost(band, 3)
# tow.cost_setter(9)
# print(type(tow.cost))
# property_name = Cost.cost.fget
# property_name = property_name.__wrapped__.__name__
# value = cost_.cost
# print('property_name: ', property_name)
