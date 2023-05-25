from abc import abstractmethod
from Communications.IComs import Communications
from Outlet.IOutlet import Outlet
import numpy as np

from RL.RLBuilder import RLBuilder
from RL.RLEnvironment.Action.ActionResponse import ActionResponse
from RL.RLEnvironment.Reward.DecentralizedReward import DeCentralizedReward
from RL.RLEnvironment.State.DecentralizedState import DeCentralizedState
from Utils.config import outlet_types


# noinspection PyAbstractClass
class Cellular(Outlet):
    """
    outlet from type cellular is the abstract class for different types ground towers
    """

    _max_capacity: float

    def __init__(
            self, tower, agent, coms: Communications, supported_services, *args, **kwargs
    ):
        """
        Parameters
        ----------
        agent : Agent
            RL agent from type outlet agent.
        coms : Communications
            the communication that will take the request to the outlet .
        supported_services : [bool]
            services that will the vehicle send it to outlet .
        services_list : [Services]
            services that will the vehicle send it to outlet (the outlet will responsed to it).
        vehicles_list : [Vehicles]
            The vehicles that demand a service from this outlet.

        """

        super().__init__(*args)

        self.dqn = RLBuilder().agent.build_agent(ActionResponse()).environment.build_env(DeCentralizedReward(),
                                                                                         DeCentralizedState()).model_.build_model(
            "decentralized", 7, 2).build()
        self.agent = agent
        self.coms = coms
        self.supported_services = supported_services
        self.services = []
        self.vehicles = kwargs.get("vehicles_list", [])
        self._supported_services_distinct = []
        self._capacity: float = 0.0
        self.max_capacity = tower

    class BuildMaxCapacity:
        def calculate_max_capacity(
                self,
                num_antennas,
                channel_bandwidth,
                coding_rate,
                modulation_order,
                average_symbol_per_slot,
                num_slots_per_frame,
                num_frames_per_second,
        ):
            spectral_efficiency = modulation_order * coding_rate  # bits/symbol

            capacity_per_antenna = (
                                           channel_bandwidth
                                           * 1e6
                                           * spectral_efficiency
                                           * average_symbol_per_slot
                                           * num_slots_per_frame
                                           * num_frames_per_second
                                   ) / 1e6  # Mbps
            total_capacity = capacity_per_antenna * num_antennas
            real_total_capacity = total_capacity // 8 / 10
            # print(f"capacity is: {real_total_capacity} MBps")
            return real_total_capacity

        def randomized_tower_based_max_capacity(self, tower_type: dict):
            outlet = {}
            outlet_vals = []
            for k in tower_type:
                outlet[k] = np.random.choice(tower_type[k])
                outlet_vals = [*outlet.values()]
            real_total_capacity = self.calculate_max_capacity(*outlet_vals)
            return real_total_capacity

    @abstractmethod
    def calculate_coverage_area(self):
        pass

    @abstractmethod
    def calculate_downlink(self):
        pass

    @property
    def supported_services_distinct(self):
        return [self.supported_services, self._distinct]

    @property
    def max_capacity(self):
        return self._max_capacity

    @max_capacity.setter
    def max_capacity(self, value):
        self._max_capacity = (
            self.BuildMaxCapacity().randomized_tower_based_max_capacity(value)
        )

    # def get_state_reward_information(self, performance_logger, new_capacity):
    #     self.dqn.environment.state.allocated_power = self.power_distinct
    #     self.dqn.environment.state.tower_capacity = new_capacity
    #     self.dqn.environment.state.services_requested = performance_logger.outlet_services_requested_number[self]
    #     self.dqn.environment.reward.services_requested = performance_logger.outlet_services_requested_number[self]



