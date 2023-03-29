import os

from Utils.Bandwidth import Bandwidth
from dotenv import load_dotenv
import os

from Utils import config as cf

load_dotenv()


class Cost:
    def __init__(self, bandwidth: Bandwidth, realtime: int) -> None:
        self.realtime = realtime
        self.bit_rate = bandwidth.allocated
        self._cost: float = 0.0

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

    @property
    def cost(self):
        return self._cost * float(os.getenv('MB_COST'))
    def __str__(self):
        return f'Request Fee: {self._cost * float(os.getenv("MB_COST"))}'


class TowerCost(Cost):
    @property
    def cost(self):
        return self._cost * float(os.getenv('KW_COST'))

    def __str__(self):
        return f'Request Fee: {self.cost}'
