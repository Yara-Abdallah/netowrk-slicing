import copy
import gc
import math
import os
import sys

import numpy
import psutil
import traci
from Environment import env_variables
import xml.etree.ElementTree as ET
import random as ra
from uuid import uuid4
from numpy import random as nump_rand
from Environment.visiulaiztion import plotting_reward_decentralize, plotting_reward_centralize, \
    plotting_Utility_Requested_Ensured, update_lines_outlet_utility, update_lines_outlet_requested, \
    update_lines_outlet_ensured, update_lines_reward_decentralized, update_lines_reward_centralized
from RL.RLBuilder import RLBuilder
from RL.RLEnvironment.Action.ActionAssignment import ActionAssignment
from RL.RLEnvironment.Reward.CentralizedReward import CentralizedReward
from RL.RLEnvironment.State.CentralizedState import CentralizedState
from Utils.Bandwidth import Bandwidth
from Utils.Cost import TowerCost, RequestCost
from Utils.PerformanceLogger import PerformanceLogger
from Utils.config import outlet_types
from Vehicle.Car import Car
from Outlet.Cellular.FactoryCellular import FactoryCellular
from Vehicle.VehicleOutletObserver import ConcreteObserver
import matplotlib.pyplot as plt
import matplotlib

results_dir = os.path.join(sys.path[0], 'results')
path4 = os.path.join(results_dir, 'centralized_weights')
path5 = os.path.join(results_dir, 'decentralized_weights')

p1 = os.path.join(results_dir, 'utility_requested_ensured')
p2 = os.path.join(results_dir, 'reward_decentralized')
p3 = os.path.join(results_dir, 'reward_centralized')
os.makedirs(p1, exist_ok=True)
os.makedirs(p2, exist_ok=True)
os.makedirs(p3, exist_ok=True)
os.makedirs(path4, exist_ok=True)
os.makedirs(path5, exist_ok=True)

matplotlib.use('agg')

fig_reward_decentralize, axs_reward_decentralize, lines_out_reward_decentralize = plotting_reward_decentralize()
fig_reward_centralize, axs_reward_centralize, lines_out_reward_centralize = plotting_reward_centralize()
fig, axs, lines_out_utility, lines_out_requested, lines_out_ensured = plotting_Utility_Requested_Ensured()


class Environment:
    size = 0
    data = {}
    Grids = {}

    def __init__(self):
        self.polygon = traci.polygon
        self.route = traci.route
        self.vehicle = traci.vehicle
        self.poi = traci.poi
        self.gui = traci.gui
        self.simulation = traci.simulation

    def get_polygons(self):
        all_polygon_ = self.polygon.getIDList()
        return all_polygon_

    def get_buildings(self):
        all_builds_ = []
        for id_poly in self.get_polygons():
            if self.polygon.getType(id_poly) == 'building':
                all_builds_.append(id_poly)
        return all_builds_

    def prepare_route(self):
        """
        add routes to env_variables
        where the routes generated by randomTrips and store in random_routes_path
        """
        tree = ET.parse(env_variables.random_routes_path)
        root = tree.getroot()
        for child_root in root:
            id_ = child_root.attrib['id']
            for child in child_root:
                # print(child.tag, child.attrib)
                # if child_root.tag == 'route':
                edges_ = list((child.attrib['edges']).split(' '))
                # print('the id: {}  , edges: {}'.format(id_, edges_))
                self.route.add(id_, edges_)
                env_variables.all_routes.append(id_)
        del tree
        del root

    def update_outlet_color(self, id_, value):
        color_mapping = {
            (9, 10): (64, 64, 64, 255),  # dark grey
            (6, 9): (255, 0, 0, 255),  # red
            (3, 6): (0, 255, 0, 255),  # green
            (1, 3): (255, 255, 0, 255)  # yellow
        }

        for val_range, color in color_mapping.items():
            if value >= val_range[0] and value <= val_range[1]:
                traci.poi.setColor(id_, color)
        del color_mapping

    def get_all_outlets(self):
        """
        get all outlets and add id with position to env variables
        """
        outlets = []
        poi_ids = traci.poi.getIDList()

        def append_outlets(id_):
            type_poi = traci.poi.getType(id_)

            if type_poi in env_variables.types_outlets:
                position_ = traci.poi.getPosition(id_)
                env_variables.outlets[type_poi].append((id_, position_))
                val = 0
                if type_poi == '3G':
                    val = 1000
                elif type_poi == '4G':
                    val = 5000
                elif type_poi == '5G':
                    val = 10000
                elif type_poi == 'wifi':
                    val = 700
                factory = FactoryCellular(outlet_types[str(type_poi)], 1, 1, [1, 1, 0], id_,
                                          [position_[0], position_[1]],
                                          10000, [],
                                          [10, 10, 10])

                outlet = factory.produce_cellular_outlet(str(type_poi))
                outlet.outlet_id = id_
                outlet.radius = val
                outlets.append(outlet)

        list(map(lambda x: append_outlets(x), poi_ids))

        # satellite = Satellite(1, [1, 1, 0], 0, [0, 0],
        #                       100000, [],
        #                       [10, 10, 10])
        # outlets.append(satellite)

        del poi_ids

        return outlets

    def distance(self, outlet1, outlet2):
        """Returns the Euclidean distance between two outlets"""
        return math.sqrt(
            (outlet1.position[0] - outlet2.position[0]) ** 2 + (outlet1.position[1] - outlet2.position[1]) ** 2)

    def fill_grids_with_the_nearest(self, outlets):
        sub_dis = []
        for j in outlets:
            dis = []
            for i in outlets:
                dis.append(self.distance(j, i))
            if len(dis) >= 3:
                sorted_dis = sorted(dis)
                min_indices = [dis.index(sorted_dis[i]) for i in range(3)]
                elements = [outlets[i] for i in min_indices]
                outlets = [element for index, element in enumerate(outlets) if index not in min_indices]
                sub_dis.append(elements)
        return sub_dis

    @staticmethod
    def fill_grids(grids):
        Grids = {
            "grid1": [],
            "grid2": [],
            "grid3": [],
            "grid4": [],
            "grid5": [],
            "grid6": [],
            "grid7": [],
        }

        def grid_namer(i, grid):
            name = "grid" + str(i + 1)
            Grids[name] = grid

        list(map(lambda x: grid_namer(x[0], x[1]), enumerate(grids)))
        return Grids

    def select_outlets_to_show_in_gui(self):
        """
        select outlets in .network to display type of each outlet
        """
        # for key in env_variables.outlets.keys():
        #     for _id,_ in env_variables.outlets[key]:
        #         self.gui.toggleSelection(_id, 'poi')
        from itertools import chain
        array = list(map(lambda x: x, chain(*list(map(lambda x: x[1], env_variables.outlets.items())))))
        list(map(lambda x: self.gui.toggleSelection(x[0], 'poi'), map(lambda x: x, array)))
        del array

    def get_positions_of_outlets(self, outlets):
        positions_of_outlets = []

        list(map(lambda x: positions_of_outlets.append(x.position), outlets))
        return positions_of_outlets

    def generate_vehicles(self, number_vehicles):
        """
        It generates vehicles and adds it to the simulation
        and get random route for each vehicle from routes in env_variables.py
        :param number_vehicles: number of vehicles to be generated
        """

        all_routes = env_variables.all_routes

        def add_vehicle(id_route_):
            uid = str(uuid4())
            self.vehicle.add(vehID=uid, routeID=id_route_)

            env_variables.vehicles[uid] = Car(uid, 0.0, 0.0)

        list(map(add_vehicle, ra.choices(all_routes, k=number_vehicles)))
        del all_routes

    def starting(self):
        """
        The function starts the simulation by calling the sumoBinary, which is the sumo-gui or sumo
        depending on the nogui option
        """

        os.environ['SUMO_NUM_THREADS'] = '8'
        # show gui
        # sumo_cmd = ["sumo-gui", "-c", env_variables.network_path]
        # dont show gui
        sumo_cmd = ["sumo-gui", "-c", env_variables.network_path]
        traci.start(sumo_cmd)

        # end the simulation and d

        self.prepare_route()

    def remove_vehicles_arrived(self):
        """
        Remove vehicles which removed from the road network ((have reached their destination) in this time step
        the add to env_variables.vehicles (dictionary)
        """
        ids_arrived = self.simulation.getArrivedIDList()

        def remove_vehicle(id_):
            # print("del car object ")
            del env_variables.vehicles[id_]

        if len(ids_arrived) != 0:
            list(map(remove_vehicle, ids_arrived))

    def add_new_vehicles(self):
        """
        Add vehicles which inserted into the road network in this time step.
        the add to env_variables.vehicles (dictionary)
        """
        ids_new_vehicles = traci.vehicle.getIDList()

        def create_vehicle(id_):
            env_variables.vehicles[id_] = Car(id_, 0, 0)

        list(map(create_vehicle, ids_new_vehicles))

    def get_current_vehicles(self):
        """
        :return: vehicles that running in road network in this time step
        """
        self.remove_vehicles_arrived()
        # self.add_new_vehicles()
        # return env_variables.vehicles

    def ensured_service_aggrigation(self, performance_logger, outlet, service_type, action_value):

        if str(service_type) == "FactorySafety":
            service_ensured_value = performance_logger.outlet_services_ensured_number[outlet][0]
            if action_value == 1:
                performance_logger.outlet_services_ensured_number[outlet][0] = int(service_ensured_value) + 1

        elif str(service_type) == "FactoryEntertainment":
            service_ensured_value = performance_logger.outlet_services_ensured_number[outlet][1]
            if action_value == 1:
                performance_logger.outlet_services_ensured_number[outlet][1] = int(service_ensured_value) + 1

        elif str(service_type) == "FactoryAutonomous":
            service_ensured_value = performance_logger.outlet_services_ensured_number[outlet][2]
            if action_value == 1:
                performance_logger.outlet_services_ensured_number[outlet][2] = int(service_ensured_value) + 1

    """"""

    def services_aggregation(self, performance_logger, outlet, service_type):

        if str(service_type) == "FactorySafety":
            num = performance_logger.outlet_services_requested_number[outlet][0]
            performance_logger.outlet_services_requested_number[outlet][0] = int(num) + 1

        elif str(service_type) == "FactoryEntertainment":
            num = performance_logger.outlet_services_requested_number[outlet][1]
            performance_logger.outlet_services_requested_number[outlet][1] = int(num) + 1

        elif str(service_type) == "FactoryAutonomous":
            num = performance_logger.outlet_services_requested_number[outlet][2]
            performance_logger.outlet_services_requested_number[outlet][2] = int(num) + 1

    def power_aggregation(self, performance_logger, outlet, service_type, request_cost, action_value):
        if outlet not in performance_logger._outlet_services_power_allocation:
            performance_logger.set_outlet_services_power_allocation(outlet, [0.0, 0.0, 0.0])

        if str(service_type) == "FactorySafety":

            x = performance_logger.outlet_services_power_allocation[outlet][0]
            if action_value == 1:
                performance_logger.outlet_services_power_allocation[outlet][0] = float(x) + float(
                    request_cost)


        elif str(service_type) == "FactoryEntertainment":
            x = performance_logger.outlet_services_power_allocation[outlet][1]
            if action_value == 1:
                performance_logger.outlet_services_power_allocation[outlet][1] = float(x) + float(
                    request_cost)


        elif str(service_type) == "FactoryAutonomous":
            x = performance_logger.outlet_services_power_allocation[outlet][2]
            if action_value == 1:
                performance_logger.outlet_services_power_allocation[outlet][2] = float(x) + float(
                    request_cost)

    def car_interact(self, car, observer, performance_logger, gridcells_dqn):
        # car.outlets_serve.append(outlets[-1])
        # print("car is : ", car )
        car.attach(observer)
        car.set_state(float(round(traci.vehicle.getPosition(car.id)[0], 4)),
                      float(round(traci.vehicle.getPosition(car.id)[1], 4)))

        # car.add_satellite(outlets[-1])
        info = car.send_request()
        if info != None:
            service = info[1][2]
            outlet = info[0]

            if outlet not in performance_logger.service_handled:
                performance_logger.set_service_handled(outlet, info[1][1], service)
            del info

            request_bandwidth = Bandwidth(service.bandwidth, service.criticality)
            request_cost = RequestCost(request_bandwidth, service.realtime)
            request_cost.cost_setter(service.realtime)
            req1 = [0, 0, 0]
            req2 = [0, 0, 0]
            ens1 = [0, 0, 0]
            ens2 = [0, 0, 0]
            if outlet not in performance_logger._outlet_services_requested_number:
                performance_logger.set_outlet_services_requested_number(outlet, [0, 0, 0])

            else:
                req1 = copy.copy(performance_logger.outlet_services_requested_number[outlet])
                outlet.dqn.environment.state.services_requested_prev = req1
                req2 = copy.copy(performance_logger.outlet_services_requested_number[outlet])
                outlet.dqn.environment.reward.services_requested_prev = req2

            if outlet not in performance_logger._outlet_services_ensured_number:
                performance_logger.set_outlet_services_ensured_number(outlet, [0, 0, 0])

            else:
                ens1 = copy.copy(performance_logger.outlet_services_ensured_number[
                                     outlet])
                outlet.dqn.environment.state.services_ensured_prev = ens1
                ens2 = copy.copy(performance_logger.outlet_services_ensured_number[
                                     outlet])
                outlet.dqn.environment.reward.services_ensured_prev = ens2

            outlet.dqn.environment.reward.dx_t_prev = outlet.dqn.environment.reward.dx_t
            # print(" dx_t_prev : ", outlet.dqn.environment.reward.dx_t_prev)
            # print("prev requested outlet : ",outlet.dqn.environment.state.services_requested_prev)
            # print("prev ensured outlet : ",outlet.dqn.environment.state.services_ensured_prev)

            gridcell = None

            for ind, gridcell_dqn in enumerate(gridcells_dqn):
                if outlet in gridcell_dqn.agents.grid_outlets:
                    gridcell = gridcell_dqn

            # print("prev requested gridcell : ", gridcell.environment.state.services_requested_prev)
            # print("prev ensured gridcell : ", gridcell.environment.state.services_ensured_prev)

            service.service_power_allocate = request_bandwidth.allocated
            self.services_aggregation(performance_logger, outlet, service.__class__.__name__)
            if len(outlet.power_distinct[0]) == 0:
                outlet.power = [0.0, 0.0, 0.0]
                # performance_logger.set_outlet_services_requested_number(outlet, [0, 0, 0])
                # performance_logger.set_outlet_services_ensured_number(outlet, [0, 0, 0])

            # print(f" outlet service requested : {outlet} , {outlet.dqn.environment.state.services_requested}")

            # print("outlet power is ........................ :  ", outlet.power)
            tower_cost = TowerCost(request_bandwidth, service.realtime)
            tower_cost.cost_setter(service.realtime)
            # print(f"bandwidth_demand is:{request_bandwidth.allocated:.2f} ")

            if outlet not in performance_logger._outlet_services_power_allocation:
                performance_logger.set_outlet_services_power_allocation(outlet, [0.0, 0.0, 0.0])

            sum_of_utility_of_all_outlets = [0, 0, 0]
            ratio_of_utility = [0, 0, 0]

            if gridcell != None:

                outlet.dqn.environment.state.services_requested = performance_logger.outlet_services_requested_number[
                    outlet]
                outlet.dqn.environment.reward.services_requested = performance_logger.outlet_services_requested_number[
                    outlet]

                outlet.power = performance_logger.outlet_services_power_allocation[outlet]

                outlet.dqn.environment.state.allocated_power = outlet.power
                outlet.dqn.environment.state.tower_capacity = outlet._max_capacity

                action_decentralize, outlet.dqn.agents.action.command.action_value_decentralize = outlet.dqn.agents.chain(
                    outlet.dqn.model,
                    outlet.dqn.environment.state.state_value_decentralize,
                    outlet.dqn.agents.epsilon)

                # print(f"{outlet.__class__.__name__} ,  action value : {outlet.dqn.agents.action.command.action_value_decentralize}")

                outlet.dqn.agents.action_value = outlet.dqn.agents.action.command.action_value_decentralize

                if outlet._max_capacity > request_bandwidth.allocated and outlet.dqn.agents.action_value == 1 and service.request_supported(
                        outlet):
                    self.ensured_service_aggrigation(performance_logger, outlet, service.__class__.__name__,
                                                     outlet.dqn.agents.action_value)

                    self.power_aggregation(performance_logger, outlet, service.__class__.__name__, request_cost.cost,
                                           outlet.dqn.agents.action_value)
                    outlet.power = performance_logger.outlet_services_power_allocation[outlet]

                    outlet._max_capacity = outlet._max_capacity - request_bandwidth.allocated
                    tower_cost.cost = outlet._max_capacity

                    outlet.dqn.environment.state.allocated_power = outlet.power
                    outlet.dqn.environment.state.tower_capacity = outlet._max_capacity
                    outlet.dqn.environment.state.services_ensured = performance_logger.outlet_services_ensured_number[
                        outlet]
                    outlet.dqn.environment.reward.services_ensured = performance_logger.outlet_services_ensured_number[
                        outlet]


                outlet.dqn.environment.state.next_state_decentralize = action_decentralize.execute(
                    outlet.dqn.environment.state,
                    outlet.dqn.agents.action.command.action_value_decentralize)


                if sum((numpy.array(outlet.dqn.environment.state.services_requested) - numpy.array(
                        outlet.dqn.environment.state.services_requested_prev))) == 0 and sum(
                    numpy.array(outlet.dqn.environment.state.services_ensured) - numpy.array(
                        outlet.dqn.environment.state.services_ensured_prev)) == 0:
                    outlet.utility = 0
                elif sum((numpy.array(outlet.dqn.environment.state.services_requested) - numpy.array(
                        outlet.dqn.environment.state.services_requested_prev))) != 0 and sum(
                    (numpy.array(outlet.dqn.environment.state.services_ensured) - numpy.array(
                        outlet.dqn.environment.state.services_ensured_prev))) != 0:
                    outlet.utility = int((sum(numpy.array(outlet.dqn.environment.state.services_ensured) - numpy.array(
                        outlet.dqn.environment.state.services_ensured_prev)) / sum(
                        numpy.array(
                            outlet.dqn.environment.state.services_requested) - numpy.array(
                            outlet.dqn.environment.state.services_requested_prev))) * 10)

                else:
                    outlet.utility = 0

                req1 = numpy.zeros(3)
                req2 = numpy.zeros(3)
                ens1 = numpy.zeros(3)
                ens2 = numpy.zeros(3)
                for i, outlet in enumerate(gridcell.agents.grid_outlets):
                    if len(outlet.power_distinct[0]) == 0:
                        outlet.power = [0.0, 0.0, 0.0]

                        # performance_logger.set_outlet_services_requested_number(outlet, [0, 0, 0])
                        # performance_logger.set_outlet_services_ensured_number(outlet, [0, 0, 0])

                    outlet.distinct = gridcell.agents.outlets_id[i]
                    gridcell.environment.state.allocated_power = outlet.power_distinct
                    gridcell.environment.state.supported_services = outlet.supported_services_distinct
                    gridcell.environment.state.filtered_powers = gridcell.environment.state.allocated_power

                    req1 = req1 + outlet.dqn.environment.state.services_requested
                    req2 = req2 + outlet.dqn.environment.reward.services_requested
                    ens1 = ens1 + outlet.dqn.environment.state.services_ensured
                    ens2 = ens2 + outlet.dqn.environment.reward.services_ensured
                    sum_of_utility_of_all_outlets = sum_of_utility_of_all_outlets + outlet.dqn.environment.reward.calculate_utility()

                gridcell.environment.state.services_requested = req1
                gridcell.environment.reward.services_requested = req2
                gridcell.environment.state.services_ensured = ens1
                gridcell.environment.reward.services_ensured = ens2

                utility_value_centralize = gridcell.environment.reward.calculate_utility()

                for index in range(3):
                    if sum_of_utility_of_all_outlets[index] != 0:
                        ratio_of_utility[index] = utility_value_centralize[index] / sum_of_utility_of_all_outlets[index]

                for outlet in gridcell.agents.grid_outlets:
                        dx_t = outlet.dqn.environment.reward.calculate_utility()
                        # print("dx_t :",dx_t)
                        outlet.dqn.environment.reward.dx_t = dx_t - outlet.dqn.environment.reward.dx_t_prev
                        averaging_value_utility_decentralize = sum(
                            outlet.dqn.environment.reward.dx_t * ratio_of_utility) / 3.0

                        coeff = outlet.dqn.environment.reward.coefficient(outlet._max_capacity,
                                                                          service.service_power_allocate,
                                                                          outlet.dqn.agents.action_value,
                                                                          service.request_supported(outlet))

                        outlet.dqn.environment.reward.reward_value = outlet.dqn.environment.reward.reward_value + (
                                averaging_value_utility_decentralize + (
                                    abs(averaging_value_utility_decentralize) * coeff))

                        outlet.dqn.agents.remember(outlet.dqn.environment.state.state_value_decentralize,
                                                   outlet.dqn.agents.action.command.action_value_decentralize,
                                                   outlet.dqn.environment.reward.reward_value,
                                                   outlet.dqn.environment.state.next_state_decentralize)

                        outlet.dqn.environment.state.state_value_decentralize = outlet.dqn.environment.state.next_state_decentralize

            if outlet.__class__.__name__ != "Satellite":
                del service
                del request_cost
                del tower_cost
                del request_bandwidth
                del sum_of_utility_of_all_outlets
                del ratio_of_utility
            del outlet
        del car

    def terminate_service(self, veh, outlets, performance_logger):
        for out in outlets:
            if out in performance_logger.service_handled:
                if veh in performance_logger.service_handled[out] and veh not in env_variables.vehicles:
                    serv = performance_logger.service_handled[out][veh]
                    out._max_capacity = out._max_capacity + serv.service_power_allocate
                    del performance_logger.service_handled[out][veh]
                    del serv

            if out not in veh.outlets_serve:
                if out in performance_logger.service_handled:
                    if veh in performance_logger.service_handled[out]:
                        serv = performance_logger.service_handled[out][veh]
                        out._max_capacity = out._max_capacity + serv.service_power_allocate
                        del performance_logger.service_handled[out][veh]
                        del serv


            else:
                out._max_capacity = out._max_capacity

    def run(self):

        steps = 0
        # Initialize previous_steps variable
        previous_steps = 0
        snapshot_time = 5
        previous_steps_centralize = 0
        previous_steps_centralize_action = 0
        prev = 0
        memory_threshold = 1500  # 3.5GB
        temp_outlets = []
        gridcells_dqn = []
        self.starting()

        outlets = self.get_all_outlets()
        self.Grids = self.fill_grids(self.fill_grids_with_the_nearest(outlets[:21]))
        step = 0
        print("\n")
        outlets_pos = self.get_positions_of_outlets(outlets)
        observer = ConcreteObserver(outlets_pos, outlets)
        performance_logger = PerformanceLogger()

        # set the maximum amount of memory that the garbage collector is allowed to use to 1 GB
        max_size = 273741824
        gc.set_threshold(700, max_size // gc.get_threshold()[1])
        #
        build = []
        for i in range(7):
            build.append(RLBuilder())
            gridcells_dqn.append(
                build[i].agent.build_agent(ActionAssignment()).environment.build_env(CentralizedReward(),
                                                                                     CentralizedState()).model_.build_model(
                    "centralized", 6, 9).build())
            gridcells_dqn[i].agents.grid_outlets = self.Grids.get(f"grid{i + 1}")
            gridcells_dqn[i].agents.outlets_id = list(range(len(gridcells_dqn[i].agents.grid_outlets)))

        for i in range(7):
            for index, outlet in enumerate(gridcells_dqn[i].agents.grid_outlets):
                temp_outlets.append(outlet)

        while step < env_variables.TIME:

            # for ind, grid in enumerate(gridcells_dqn):
            #     print(f"prev requested grid{ind} : ", grid.environment.state.services_requested_prev)
            #     print(f"prev ensured grid{ind} : ", grid.environment.state.services_ensured_prev)
            #     print(f"this requested grid{ind} : ", grid.environment.state.services_requested)
            #     print(f"this ensured grid{ind} : ", grid.environment.state.services_ensured)
            #     for i, out in enumerate(grid.agents.grid_outlets):
            #         print(f"prev requested out{i} : ", out.dqn.environment.state.services_requested_prev)
            #         print(f"prev ensured out{i} : ", out.dqn.environment.state.services_ensured_prev)
            #         print(f"this requested out{i} : ", out.dqn.environment.state.services_requested)
            #         print(f"this ensured out{i} : ", out.dqn.environment.state.services_ensured)
            #         print(f"dx_t_prev : ", out.dqn.environment.reward.dx_t_prev)
            #         print(f"dx_t : ", out.dqn.environment.reward.dx_t)
            #         print("reward value : ", out.dqn.environment.reward.reward_value)

            process = psutil.Process()
            memory_usage = process.memory_info().rss / 1024.0 / 1024.0  # Convert to MB
            # print(f"Memory usage at step {step}: {memory_usage:.2f} MB")
            if memory_usage > memory_threshold:
                gc.collect(0)

            gc.collect(0)
            steps += 1
            traci.simulationStep()
            if step == 0:
                number_cars = int(nump_rand.normal(loc=env_variables.number_cars_mean_std['mean'],
                                                   scale=env_variables.number_cars_mean_std['std']))
                self.generate_vehicles(number_cars)

            if traci.vehicle.getIDCount() <= env_variables.threashold_number_veh:
                number_cars = int(nump_rand.normal(loc=env_variables.number_cars_mean_std['mean'],
                                                   scale=env_variables.number_cars_mean_std['std']))
                self.generate_vehicles(number_cars)

            self.get_current_vehicles()
            print("step is ....................................... ", step)

            # night time
            if 0 <= step <= env_variables.period1:
                env_variables.number_cars_mean_std['mean'] = 85
                env_variables.number_cars_mean_std['std'] = 2
                env_variables.threashold_number_veh = 25
                env_variables.ENTERTAINMENT_RATIO = 0.2
                env_variables.AUTONOMOUS_RATIO = 0.3
                env_variables.SAFETY_RATIO = 0.5
            # day time
            elif env_variables.period1 + 10 < step <= env_variables.period2:
                env_variables.number_cars_mean_std['mean'] = 100
                env_variables.number_cars_mean_std['std'] = 2
                env_variables.threashold_number_veh = 50
                env_variables.ENTERTAINMENT_RATIO = 0.3
                env_variables.AUTONOMOUS_RATIO = 0.3
                env_variables.SAFETY_RATIO = 0.4

            elif env_variables.period2 + 10 < step <= env_variables.period3:
                env_variables.number_cars_mean_std['mean'] = 150
                env_variables.number_cars_mean_std['std'] = 2
                env_variables.threashold_number_veh = 85
                env_variables.ENTERTAINMENT_RATIO = 0.6
                env_variables.AUTONOMOUS_RATIO = 0.2
                env_variables.SAFETY_RATIO = 0.2

            elif env_variables.period3 + 10 < step <= env_variables.period4:
                env_variables.number_cars_mean_std['mean'] = 100
                env_variables.number_cars_mean_std['std'] = 2
                env_variables.threashold_number_veh = 50
                env_variables.ENTERTAINMENT_RATIO = 0.3
                env_variables.AUTONOMOUS_RATIO = 0.3
                env_variables.SAFETY_RATIO = 0.4

            elif env_variables.period4 + 10 < step <= env_variables.period5:
                env_variables.number_cars_mean_std['mean'] = 85
                env_variables.number_cars_mean_std['std'] = 2
                env_variables.threashold_number_veh = 25
                env_variables.ENTERTAINMENT_RATIO = 0.2
                env_variables.AUTONOMOUS_RATIO = 0.3
                env_variables.SAFETY_RATIO = 0.5

            number_of_cars_will_send_requests = round(len(list(env_variables.vehicles.values())) * 0.2)
            vehicles = ra.sample(list(env_variables.vehicles.values()), number_of_cars_will_send_requests)
            list(map(lambda veh: self.car_interact(veh, observer, performance_logger, gridcells_dqn),
                     vehicles))

            list(map(lambda veh: self.terminate_service(veh, outlets, performance_logger),
                     env_variables.vehicles.values()))

            update_lines_outlet_utility(lines_out_utility, steps, temp_outlets)
            update_lines_outlet_requested(lines_out_requested, steps, temp_outlets)
            update_lines_outlet_ensured(lines_out_ensured, steps, temp_outlets)
            update_lines_reward_decentralized(lines_out_reward_decentralize, steps, temp_outlets)
            update_lines_reward_centralized(lines_out_reward_centralize, steps, gridcells_dqn)

            for axs_ in [axs, axs_reward_decentralize, axs_reward_centralize]:
                for ax in axs_.flatten():
                    ax.legend()
                    ax.relim()
                    ax.autoscale_view()
                if axs is axs:
                    fig.canvas.draw()
                elif axs is axs_reward_decentralize:
                    fig_reward_decentralize.canvas.draw()
                else:
                    fig_reward_centralize.canvas.draw()

            if steps - prev == snapshot_time:
                prev = steps
                # path1 = f'I://Documents//utility_requested_ensured//snapshot{steps}'
                # path2 = f'I://Documents//reward_decentralized//snapshot{steps}'
                # path3 = f'I://Documents//reward_centralized//snapshot{steps}'

                path1 = os.path.join(p1, f'snapshot{steps}')
                path2 = os.path.join(p2, f'snapshot{steps}')
                path3 = os.path.join(p3, f'snapshot{steps}')
                print(" path3 : ", path3)
                fig.set_size_inches(10, 8)
                fig_reward_centralize.set_size_inches(15, 10)
                fig_reward_decentralize.set_size_inches(10, 8)  # set physical size of plot in inches
                fig.savefig(path1 + '.svg', dpi=300)
                fig_reward_decentralize.savefig(path2 + '.svg', dpi=300)
                fig_reward_centralize.savefig(path3 + '.svg', dpi=300)
            else:
                plt.close(fig)
                plt.close(fig_reward_decentralize)
                plt.close(fig_reward_centralize)

            if steps - previous_steps >= env_variables.decentralized_replay_buffer:
                previous_steps = steps

                for ind, gridcell_dqn in enumerate(gridcells_dqn):
                    for i, outlet in enumerate(gridcell_dqn.agents.grid_outlets):
                        # performance_logger.set_outlet_services_power_allocation(outlet, [0.0, 0.0, 0.0])
                        if len(outlet.dqn.agents.memory) > outlet.dqn.agents.batch_size:
                            print("replay buffer of decentralize ")
                            outlet.dqn.agents.replay_buffer_decentralize(outlet.dqn.agents.batch_size, outlet.dqn.model)
                        # outlet.dqn.environment.state.resetsate(outlet.max_capacity)

            if steps - previous_steps_centralize_action >= 40:
                previous_steps_centralize_action = steps
                for gridcell in gridcells_dqn:
                    gridcell.environment.state.state_value_centralize = gridcell.environment.state.calculate_state(
                        gridcell.environment.state.supported_services)

                    action_centralize, gridcell.agents.action.command.action_value_centralize = gridcell.agents.chain(
                        gridcell.model,
                        gridcell.environment.state.state_value_centralize,
                        gridcell.agents.epsilon)
                    gridcell.environment.state.next_state_centralize = action_centralize.execute(
                        gridcell.environment.state, gridcell.agents.action.command.action_value_centralize)
                    # del action_centralize

                    for k, outlet in enumerate(gridcell.agents.grid_outlets):
                        # print(" befor : outlet.supported_services : ", outlet.supported_services)
                        outlet.supported_services = gridcell.agents.action.command.action_value_centralize[:, k]
                        # print("after outlet.supported_services : ", outlet.supported_services )
                    utility_value_centralize = gridcell.environment.reward.calculate_utility()
                    averaging_value_utility_centralize = sum(utility_value_centralize) / 3.0

                    if averaging_value_utility_centralize < env_variables.Threshold_of_utility:

                        if averaging_value_utility_centralize == 0:
                            gridcell.environment.reward.reward_value = gridcell.environment.reward.reward_value + 0
                        else:
                            gridcell.environment.reward.reward_value = gridcell.environment.reward.reward_value + max(
                                -10, (averaging_value_utility_centralize - env_variables.Threshold_of_utility) * (
                                        env_variables.Threshold_of_utility / averaging_value_utility_centralize))
                    else:

                        gridcell.environment.reward.reward_value = gridcell.environment.reward.reward_value + (
                                (averaging_value_utility_centralize) * (
                                averaging_value_utility_centralize / env_variables.Threshold_of_utility))

                    gridcell.agents.remember(gridcell.environment.state.state_value_centralize,
                                             gridcell.agents.action.command.action_value_centralize,
                                             gridcell.environment.reward.reward_value,
                                             gridcell.environment.state.next_state_centralize)

                    gridcell.environment.state.services_requested_prev = gridcell.environment.state.services_requested
                    gridcell.environment.reward.services_requested_prev = gridcell.environment.reward.services_requested
                    gridcell.environment.state.services_ensured_prev = gridcell.environment.state.services_ensured
                    gridcell.environment.reward.services_ensured_prev = gridcell.environment.reward.services_ensured

                    gridcell.environment.state.state_value_centralize = gridcell.environment.state.next_state_centralize

            if steps - previous_steps_centralize >= env_variables.centralized_replay_buffer:
                previous_steps_centralize = steps
                for ind, gridcell_dqn in enumerate(gridcells_dqn):
                    if len(gridcell_dqn.agents.memory) >= 32:
                        print("replay buffer of centralize ")
                        gridcell_dqn.agents.replay_buffer_centralize(32,
                                                                     gridcell_dqn.model)

                    env_variables.Threshold_of_utility = env_variables.Threshold_of_utility + (
                            env_variables.Threshold_of_utility * env_variables.Threshold_of_utility_acc)

            step += 1

            if step == env_variables.TIME:
                for i in range(7):
                    gridcells_dqn[i].model.save(os.path.join(path4, f'weights_{i}.hdf5'))

                for index, g in enumerate(temp_outlets):
                    g.dqn.model.save(os.path.join(path5, f'weights_{index}.hdf5'))

        plt.close()
        traci.close()
