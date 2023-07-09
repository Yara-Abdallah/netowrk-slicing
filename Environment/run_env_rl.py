import copy
import gc
import math
import os
import pickle
import sys
import shutil

import numpy
import numpy as np
import psutil
import traci
from Environment import env_variables
import xml.etree.ElementTree as ET
import random as ra
from uuid import uuid4
from numpy import random as nump_rand
from Environment.visiulaiztion import plotting_reward_decentralize, plotting_reward_centralize, \
    plotting_Utility_Requested_Ensured, update_lines_outlet_utility, update_lines_outlet_requested, \
    update_lines_outlet_ensured, update_lines_reward_decentralized, update_lines_reward_centralized, \
    plotting_Qvalue_decentralize, plotting_Qvalue_centralize, update_lines_Qvalue_decentralized, \
    update_lines_Qvalue_centralized

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

results_dir = os.path.join(sys.path[0], 'results3_exploit_decentralize')
path6 = os.path.join(results_dir, 'centralized_weights')
path7 = os.path.join(results_dir, 'decentralized_weights')
path_memory_centralize = os.path.join(results_dir,'centralize_memory')
path_memory_decentralize = os.path.join(results_dir,'decentralize_memory')
# prev_results_dir = "//content//drive//MyDrive//network_slicing//prev_results//"
p1 = os.path.join(results_dir, 'utility_requested_ensured')
p2 = os.path.join(results_dir, 'reward_decentralized')
p3 = os.path.join(results_dir, 'reward_centralized')
p4 = os.path.join(results_dir, 'qvalue_decentralized')
p5 = os.path.join(results_dir, 'qvalue_centralized')
# centralize_qvalue_path = os.path.join(prev_results_dir, 'qvalue_centralized_for_plotting')
# decentralize_qvalue_path = os.path.join(prev_results_dir, 'qvalue_decentralized_for_plotting')
prev_results_3tanh_dir = "//content//drive//MyDrive//network_slicing//results3_tanh//"
results1_explor_decentralize = "//content//drive//MyDrive//network_slicing//results2_explor_decentralize//"

prev_centralize_weights_path = os.path.join(prev_results_3tanh_dir,"centralized_weights//")
prev_decentralize_weights_path = os.path.join(results1_explor_decentralize,"decentralized_weights//")
# prev_centralize_memory_path = os.path.join(prev_results_4tanh_dir,"centralize_memory//")
prev_decentralize_memory_path = os.path.join(results1_explor_decentralize,"decentralize_memory//")
centralize_qvalue_path = os.path.join(results_dir,"qvalue_centralized_for_plotting//")
decentralize_qvalue_path = os.path.join(results_dir,"qvalue_decentralized_for_plotting//")
#
# if type_poi == '3G':
#                     val = 850
#                 elif type_poi == '4G':
#                     val = 1250
#                 elif type_poi == '5G':
#                     val = 10000
#                 elif type_poi == 'wifi':
#                     val = 550

# def set_max_capacity(self, type):
#     if type == "ThreeG":
#         return 25000
#     elif type == "FourG":
#         return 45000
#     elif type == "Wifi":
#         return 10500
os.makedirs(p1, exist_ok=True)
os.makedirs(p2, exist_ok=True)
os.makedirs(p3, exist_ok=True)
os.makedirs(p4, exist_ok=True)
os.makedirs(p5, exist_ok=True)
os.makedirs(path6, exist_ok=True)
os.makedirs(path7, exist_ok=True)
os.makedirs(path_memory_centralize, exist_ok=True)
os.makedirs(path_memory_decentralize, exist_ok=True)
os.makedirs(centralize_qvalue_path, exist_ok=True)
os.makedirs(decentralize_qvalue_path, exist_ok=True)


matplotlib.use('agg')

fig_reward_decentralize, axs_reward_decentralize, lines_out_reward_decentralize = plotting_reward_decentralize()
fig_reward_centralize, axs_reward_centralize, lines_out_reward_centralize = plotting_reward_centralize()
fig, axs, lines_out_utility, lines_out_requested, lines_out_ensured = plotting_Utility_Requested_Ensured()
fig_Qvalue_decentralize, axs_Qvalue_decentralize, lines_out_Qvalue_decentralize = plotting_Qvalue_decentralize()
fig_Qvalue_centralize, axs_Qvalue_centralize, lines_out_Qvalue_centralize = plotting_Qvalue_centralize()


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
                    val = 2250
                elif type_poi == '5G':
                    val = 10000
                elif type_poi == 'wifi':
                    val = 550
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
        sumo_cmd = ["sumo", "-c", env_variables.network_path]
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

    def ensured_service_aggrigation(self, outlet_services_ensured_number, outlet, service_type, flag):
        if str(service_type) == "FactorySafety":
            service_ensured_value = outlet_services_ensured_number[outlet][0]
            # if action_value == 1:
            if flag == -1 and service_ensured_value != 0:
                outlet_services_ensured_number[outlet][0] = int(service_ensured_value) + flag
            if flag == 1:
                outlet_services_ensured_number[outlet][0] = int(service_ensured_value) + flag

        elif str(service_type) == "FactoryEntertainment":
            service_ensured_value = outlet_services_ensured_number[outlet][1]
            # if action_value == 1:
            if flag == -1 and service_ensured_value != 0:
                outlet_services_ensured_number[outlet][1] = int(service_ensured_value) + flag
            if flag == 1:
                outlet_services_ensured_number[outlet][1] = int(service_ensured_value) + flag

        elif str(service_type) == "FactoryAutonomous":
            service_ensured_value = outlet_services_ensured_number[outlet][2]
            # if action_value == 1:
            if flag == -1 and service_ensured_value != 0:
                outlet_services_ensured_number[outlet][2] = int(service_ensured_value) + flag
            if flag == 1:
                outlet_services_ensured_number[outlet][2] = int(service_ensured_value) + flag

    """"""

    def services_aggregation(self, outlet_services_requested_number, outlet, service_type, flag):
        # print("outlet_services_requested_number: ... ", outlet_services_requested_number[outlet])
        if str(service_type) == "FactorySafety":
            num = outlet_services_requested_number[outlet][0]
            if flag == -1 and num != 0:
                outlet_services_requested_number[outlet][0] = int(num) + flag
            elif flag == 1:
                outlet_services_requested_number[outlet][0] = int(num) + flag

        elif str(service_type) == "FactoryEntertainment":
            num = outlet_services_requested_number[outlet][1]
            if flag == -1 and num != 0:
                outlet_services_requested_number[outlet][1] = int(num) + flag
            if flag == 1:
                outlet_services_requested_number[outlet][1] = int(num) + flag
        elif str(service_type) == "FactoryAutonomous":
            num = outlet_services_requested_number[outlet][2]
            if flag == -1 and num != 0:
                outlet_services_requested_number[outlet][2] = int(num) + flag
            if flag == 1:
                outlet_services_requested_number[outlet][2] = int(num) + flag

    def power_aggregation(self, outlet_services_power_allocation, outlet, service_type, service, flage):
        # if outlet not in outlet_services_power_allocation:
        #     outlet_services_power_allocation[outlet]= [0.0, 0.0, 0.0]

        if str(service_type) == "FactorySafety":

            x = outlet_services_power_allocation[outlet][0]
            # if action_value == 1:
            if flage == 1:
                outlet_services_power_allocation[outlet][0] = float(x) + float(
                    service.service_power_allocate)
            elif flage == -1 and x != 0:
                outlet_services_power_allocation[outlet][0] = float(x) - float(
                    service.service_power_allocate)



        elif str(service_type) == "FactoryEntertainment":
            x = outlet_services_power_allocation[outlet][1]
            # if action_value == 1:
            if flage == 1:
                outlet_services_power_allocation[outlet][1] = float(x) + float(
                    service.service_power_allocate)
            elif flage == -1 and x != 0:
                outlet_services_power_allocation[outlet][1] = float(x) - float(
                    service.service_power_allocate)


        elif str(service_type) == "FactoryAutonomous":
            x = outlet_services_power_allocation[outlet][2]
            # if action_value == 1:
            if flage == 1:
                outlet_services_power_allocation[outlet][2] = float(x) + float(
                    service.service_power_allocate)
            elif flage == -1 and x != 0:
                outlet_services_power_allocation[outlet][2] = float(x) - float(
                    service.service_power_allocate)

    def add_value_to_pickle(self, path, value):
        mode = 'wb' if not os.path.exists(path) else 'ab'
        with open(path, mode) as file:
            pickle.dump(value, file)

        # with open(path, "a+") as file:
        #
        #     lines = file.readlines()
        #
        #     if not lines:  # Check if lines is empty
        #         file.write(str(value))
        #         file.write("\n")
        #     else:
        #         file.write("\n")
        #         file.write(str(value))
            #     line = lines[-1]
            #     if line != "":
            #         values = line.strip().split()
            #         if len(values) == 320:
            #             file.write("\n")
            #         else:
            #             file.write(" ")
            #             file.write(str(value))

    def accumulate_until_sum_limit(self, lst, target_sum):
        accumulated_values = []
        current_sum = 0
        counter = 0

        for value in reversed(lst):
            if current_sum + value <= target_sum:
                counter += 1
                accumulated_values.append(value)
                current_sum += value

                if current_sum == target_sum:
                    break

        return accumulated_values[::-1], counter

    def requests_buffering(self, car, observer, performance_logger, steps, previous_period):
        car.attach(observer)
        car.set_state(float(round(traci.vehicle.getPosition(car.id)[0], 4)),
                      float(round(traci.vehicle.getPosition(car.id)[1], 4)))

        # car.add_satellite(outlets[-1])
        info = car.send_request()
        if info != None:
            service = info[1][2]
            outlet = info[0]
            # print("outlet type is 1 --> : ", outlet.__class__.__name__)
            if service.request_supported(outlet):
                if outlet not in performance_logger.handled_services:
                    performance_logger.set_service_handled(outlet, car, service)
                if outlet in performance_logger.handled_services:
                    performance_logger.handled_services[outlet].update({car: service})

                request_bandwidth = Bandwidth(service.bandwidth, service.criticality)
                request_cost = RequestCost(request_bandwidth, service.realtime)
                request_cost.cost_setter(service.realtime)

                if outlet not in performance_logger.outlet_services_requested_number:
                    performance_logger.set_outlet_services_requested_number(outlet, [0, 0, 0])

                if outlet not in performance_logger.outlet_services_ensured_number:
                    performance_logger.set_outlet_services_ensured_number(outlet, [0, 0, 0])

                if outlet not in performance_logger.outlet_services_requested_number_with_action_period:
                    performance_logger.set_outlet_services_requested_number_with_action_period(outlet, [0, 0, 0])

                if outlet not in performance_logger.outlet_services_ensured_number_with_action_period:
                    performance_logger.set_outlet_services_ensured_number_with_action_period(outlet, [0, 0, 0])

                if outlet not in performance_logger.outlet_services_power_allocation_with_action_period:
                    performance_logger.set_outlet_services_power_allocation_with_action_period(outlet, [0.0, 0.0, 0.0])

                if outlet not in performance_logger.outlet_services_power_allocation_current:
                    performance_logger.set_outlet_services_power_allocation_current(outlet, [0.0, 0.0, 0.0])

                if outlet not in performance_logger.outlet_services_power_allocation:
                    performance_logger.set_outlet_services_power_allocation(outlet, [0.0, 0.0, 0.0])

                if outlet not in performance_logger.outlet_services_power_allocation_for_all_requested:
                    performance_logger.set_outlet_services_power_allocation_for_all_requested(outlet, [0.0, 0.0, 0.0])

                service.service_power_allocate = request_bandwidth.allocated
                if len(outlet.power_distinct[0]) == 0:
                    outlet.power = [0.0, 0.0, 0.0]

                tower_cost = TowerCost(request_bandwidth, service.realtime)
                tower_cost.cost_setter(service.realtime)

                self.services_aggregation(performance_logger.outlet_services_requested_number, outlet,
                                          service.__class__.__name__, 1)
                self.services_aggregation(performance_logger.outlet_services_requested_number_with_action_period,
                                          outlet, service.__class__.__name__, 1)
                self.power_aggregation(performance_logger.outlet_services_power_allocation_with_action_period, outlet,
                                       service.__class__.__name__, service, 1)
                self.power_aggregation(performance_logger.outlet_services_power_allocation_for_all_requested, outlet,
                                       service.__class__.__name__, service, 1)
                self.ensured_service_aggrigation(performance_logger.outlet_services_ensured_number_with_action_period,
                                                 outlet, service.__class__.__name__, 1)

    def decentralize_period(self, performance_logger, gridcells_dqn, step):
        for gridcell in gridcells_dqn:
            req1 = numpy.zeros(3)
            ens1 = numpy.zeros(3)
            power = numpy.zeros(3)
            for i, outlet in enumerate(gridcell.agents.grid_outlets):
                for service_index in range(3):
                    if outlet.dqn.environment.state.supported_services[service_index] == 1:
                        if outlet in performance_logger.handled_services:
                            # flag = True

                            # outlet._max_capacity = outlet.set_max_capacity(outlet.__class__.__name__)
                            gridcell.environment.state._max_capacity_each_outlet[i] = outlet._max_capacity
                            # print("max capacity : ",outlet._max_capacity )
                            # print("outlet._current_capacity : ", outlet.current_capacity)
                            gridcell.environment.state._capacity_each_tower[i] = outlet.current_capacity
                            outlet.dqn.environment.state.state_value_decentralize[service_index][
                                0] = outlet.current_capacity
                            outlet.dqn.environment.state.tower_capacity = outlet.current_capacity
                            outlet.dqn.environment.state.max_tower_capacity = outlet._max_capacity
                            outlet.dqn.environment.state.supported_services = outlet.supported_services
                            outlet.dqn.environment.state.action_value = outlet.dqn.agents.action_value
                            outlet.dqn.environment.state.index_service = service_index
                            # print("state_value_decentralize : ",outlet.dqn.environment.state.state_value_decentralize)

                            if step <= 10:
                                outlet.dqn.environment.state.state_value_decentralize[
                                    service_index] = outlet.dqn.environment.state.calculate_state()
                            # print("outlet.dqn.environment.state.supported_services : ",outlet.dqn.environment.state.supported_services)
                            # print("decentralize state : ",outlet.dqn.environment.state.state_value_decentralize[service_index])
                            action_decentralize, outlet.dqn.agents.action.command.action_value_decentralize , flag = outlet.dqn.agents.exploitation(
                                outlet.dqn.model,
                                outlet.dqn.environment.state.state_value_decentralize[service_index],
                                )
                            outlet.dqn.agents.action_value = outlet.dqn.agents.action.command.action_value_decentralize
                            x = 0
                            outlet.dqn.environment.state.action_value = outlet.dqn.agents.action_value

                            if outlet.dqn.agents.action_value == 1:
                                Z = outlet.current_capacity
                                C = sum(
                                    performance_logger.outlet_services_power_allocation_with_action_period[outlet])
                                if outlet.current_capacity - C <= 0:
                                    outlet.current_capacity = 0
                                else:
                                    outlet.current_capacity = outlet.current_capacity - C
                                # print(" z in action 1 : ", Z)
                                # print(" c in action 1 : ", C)
                                x = Z - C
                                number_of_requests_in_this_period = sum(
                                    performance_logger.outlet_services_requested_number_with_action_period[outlet])
                                if number_of_requests_in_this_period != 0:
                                    outlet.dqn.environment.state.mean_power_allocated_requests = C / number_of_requests_in_this_period
                                else:
                                    outlet.dqn.environment.state.mean_power_allocated_requests = 0

                                outlet.dqn.environment.state.services_requested = \
                                    performance_logger.outlet_services_requested_number_with_action_period[outlet]

                                outlet.power = performance_logger.outlet_services_power_allocation_with_action_period[
                                    outlet]

                                outlet.dqn.environment.state.allocated_power = outlet.power
                                outlet.dqn.environment.state.tower_capacity = outlet.current_capacity

                                outlet.dqn.environment.state.services_ensured = \
                                    performance_logger.outlet_services_ensured_number_with_action_period[
                                        outlet]

                                # for ind in range(3):
                                performance_logger.outlet_services_ensured_number[outlet][service_index] = \
                                    performance_logger.outlet_services_ensured_number[
                                        outlet][service_index] + outlet.dqn.environment.state.services_ensured[
                                        service_index]

                                performance_logger.outlet_services_power_allocation[outlet][service_index] = \
                                    performance_logger.outlet_services_power_allocation[
                                        outlet][service_index] + outlet.dqn.environment.state.allocated_power[
                                        service_index]

                            elif outlet.dqn.agents.action_value == 0:

                                Z = outlet.current_capacity
                                C = sum(
                                    performance_logger.outlet_services_power_allocation_with_action_period[outlet])
                                # print(" z in action 0 : ",Z)
                                # print(" c in action 0 : ",C)
                                x = Z - C
                                number_of_requests_in_this_period = sum(
                                    performance_logger.outlet_services_requested_number_with_action_period[outlet])
                                if number_of_requests_in_this_period != 0:
                                    outlet.dqn.environment.state.mean_power_allocated_requests = C / number_of_requests_in_this_period
                                else:
                                    outlet.dqn.environment.state.mean_power_allocated_requests = 0

                                outlet.power = performance_logger.outlet_services_power_allocation_with_action_period[
                                    outlet]

                                outlet.dqn.environment.state.allocated_power = outlet.power

                                outlet.dqn.environment.state.services_requested = \
                                    performance_logger.outlet_services_requested_number_with_action_period[outlet]
                                outlet.dqn.environment.state.services_ensured = [0, 0, 0]
                                performance_logger.set_outlet_services_ensured_number_with_action_period(outlet,
                                                                                                         [0, 0, 0])
                            outlet.dqn.environment.state.action_value = outlet.dqn.agents.action.command.action_value_decentralize
                            outlet.dqn.environment.state.next_state_decentralize[
                                service_index] = action_decentralize.execute(
                                outlet.dqn.environment.state,
                                outlet.dqn.agents.action.command.action_value_decentralize)
                            # print("decenlraize next state value :   ",outlet.dqn.environment.state.next_state_decentralize[service_index] )

                            outlet.dqn.environment.reward.reward_value = outlet.dqn.environment.reward.calculate_reward(
                                x, outlet.dqn.agents.action.command.action_value_decentralize,
                                sum(performance_logger.outlet_services_power_allocation_with_action_period[outlet]),
                                outlet._max_capacity)
                            # self.add_value_to_text(
                            #     f"H://work_projects//network_slicing//ns//results//reward_decentralize{i}.txt",
                            #     outlet.dqn.environment.reward.reward_value)
                            # self.add_value_to_text(
                            #     f"H://work_projects//network_slicing//ns//results//action_decentralize{i}.txt",
                            #     outlet.dqn.agents.action_value)
                            # print("decentralize flag : ",flag)
                            # print("dec ",outlet.dqn.environment.state.state_value_decentralize[service_index])
                            # print("dec ",outlet.dqn.agents.action.command.action_value_decentralize)
                            # print("dec ",outlet.dqn.environment.reward.reward_value)
                            # print("dec ",outlet.dqn.environment.state.next_state_decentralize[service_index])
                            if isinstance(outlet.dqn.agents.action.command.action_value_decentralize , np.ndarray):
                                outlet.dqn.agents.action.command.action_value_decentralize = outlet.dqn.agents.action.command.action_value_decentralize.item()
                            outlet.dqn.agents.remember(flag,
                                outlet.dqn.environment.state.state_value_decentralize[service_index],
                                outlet.dqn.agents.action.command.action_value_decentralize,
                                outlet.dqn.environment.reward.reward_value,
                                outlet.dqn.environment.state.next_state_decentralize[service_index])

                            outlet.dqn.environment.state.state_value_decentralize[service_index] = \
                            outlet.dqn.environment.state.next_state_decentralize[service_index]

                            if len(outlet.power_distinct[0]) == 0:
                                outlet.power = [0.0, 0.0, 0.0]

                            outlet.distinct = gridcell.agents.outlets_id[i]
                            # gridcell.environment.state.allocated_power = outlet.power_distinct
                            gridcell.environment.state.supported_services = outlet.supported_services_distinct
                            # for ind in range(3):
                            req1[service_index] = req1[service_index] + \
                                                  performance_logger.outlet_services_requested_number[outlet][
                                                      service_index]
                            ens1[service_index] = ens1[service_index] + \
                                                  performance_logger.outlet_services_ensured_number[outlet][
                                                      service_index]
                            power[service_index] = power[service_index] + \
                                                   performance_logger.outlet_services_power_allocation[outlet][
                                                       service_index]
                # print("outlet requested : ",performance_logger.outlet_services_requested_number[outlet])
                # print("outlet ensured : ", performance_logger.outlet_services_ensured_number[outlet])
                # print("req1 : ",req1)
                # print("ens1 : ",ens1)
            # if flag == True:
            gridcell.environment.state.services_requested = req1
            gridcell.environment.reward.services_requested = req1
            gridcell.environment.state.services_ensured = ens1
            gridcell.environment.reward.services_ensured = ens1
            gridcell.environment.state.average_power_allocate = power
            # print("gridcell requested : ", gridcell.environment.state.services_requested)
            # print("gridcell ensured : ", gridcell.environment.state.services_ensured)

    def centralize_nextstate_reward(self, gridcells_dqn):
        for gridcell in gridcells_dqn:
            # print("state value centralize : ", gridcell.environment.state.state_value_centralize)
            next_states = []
            rewards = []
            utility_value_centralize = 0
            index_of_service = 0
            outlets = gridcell.agents.grid_outlets
            for ind in outlets :
                print("type : ",ind.__class__.__name__,"  current capacity : ",ind.current_capacity)
            index_of_outlet = -1
            for i in range(9):
                index_of_service = i % 3
                if i % 3 == 0:
                    index_of_outlet += 1

                gridcell.environment.state.index_service = index_of_service
                gridcell.environment.state.index_outlet = index_of_outlet
                gridcell.environment.state.max_capacity_each_outlet[index_of_service] = outlets[
                    index_of_outlet]._max_capacity
                gridcell.environment.state.capacity_each_tower[index_of_service] = outlets[
                    index_of_outlet].current_capacity
                gridcell.environment.state.services_requested_for_outlet = outlets[
                    index_of_outlet].dqn.environment.state.services_requested
                gridcell.environment.state.services_ensured_for_outlet = outlets[
                    index_of_outlet].dqn.environment.state.services_ensured
                gridcell.environment.state.allocated_power = outlets[index_of_outlet].power_distinct
                next = gridcell.environment.state.calculate_state()
                next_states.append(next)
                # print("next state value centralize : ", next)

            for i in range(3):
                utility_value_centralize = gridcell.environment.reward.calculate_utility(i)

                dx = utility_value_centralize - gridcell.environment.state.utility_value_centralize_prev

                if dx > 0 and utility_value_centralize >= env_variables.Threshold_of_utility:
                    rewards.append(utility_value_centralize * 10)

                elif dx < 0 and utility_value_centralize < env_variables.Threshold_of_utility:
                    rewards.append(utility_value_centralize * -10)

                elif dx > 0 and utility_value_centralize <= env_variables.Threshold_of_utility:
                    rewards.append(dx)
                elif dx < 0 and utility_value_centralize > env_variables.Threshold_of_utility:
                    rewards.append(dx)

                elif dx == 0 and utility_value_centralize <= env_variables.Threshold_of_utility:
                    rewards.append(dx * 0.2)
                elif dx == 0 and utility_value_centralize > env_variables.Threshold_of_utility:
                    rewards.append(dx * 0.2)
            for i in range(len(rewards)):
                rewards[i] = 1 / (1 + math.pow(math.e, -1 * rewards[i]))

            gridcell.environment.state.next_state_centralize = next_states
            gridcell.environment.reward.reward_value = rewards * 3
            for index in range(9):
                gridcell.agents.remember(gridcell.agents.action.command.action_flags[index],
                                         gridcell.environment.state.state_value_centralize[index],
                                         gridcell.agents.action.command.action_value_centralize[index],
                                         gridcell.environment.reward.reward_value[index],
                                         gridcell.environment.state.next_state_centralize[index])

            gridcell.environment.state.state_value_centralize = gridcell.environment.state.next_state_centralize
            gridcell.environment.state.services_requested_prev = gridcell.environment.state.services_requested
            gridcell.environment.reward.services_requested_prev = gridcell.environment.reward.services_requested
            gridcell.environment.state.services_ensured_prev = gridcell.environment.state.services_ensured
            gridcell.environment.reward.services_ensured_prev = gridcell.environment.reward.services_ensured
            gridcell.environment.state.utility_value_centralize_prev = utility_value_centralize

    def centralize_state_action(self, gridcells_dqn, step, performance_logger):
        number_of_services = 3
        state = 0
        performance_logger.number_of_periods_until_now = 1
        for gridcell in gridcells_dqn:
            states = []
            actions = []
            actions_objects = []
            list_flags = []

            # if step > 2:
            #     if step > env_variables.advisor_period[0] and step <= env_variables.advisor_period[1]:
            #         flags = gridcell.agents.heuristic_action(gridcell,
            #                                                  performance_logger.outlet_services_power_allocation_for_all_requested,
            #                                                  performance_logger.outlet_services_requested_number,
            #                                                  performance_logger.number_of_periods_until_now)
            #         list_flags.extend(flags)
            for j, outlet in enumerate(gridcell.agents.grid_outlets):
                supported = []

                for i in range(number_of_services):
                    gridcell.environment.state.index_outlet = j
                    gridcell.environment.state.index_service = i
                    if step <= 2:
                        list_flags.append(0)
                        gridcell.environment.state.max_capacity_each_outlet[j] = outlet._max_capacity
                        gridcell.environment.state.capacity_each_tower[j] = outlet.current_capacity
                        gridcell.environment.state.services_requested_for_outlet = outlet.dqn.environment.state.services_requested
                        gridcell.environment.state.services_ensured_for_outlet = outlet.dqn.environment.state.services_ensured
                        if len(outlet.power_distinct[0]) == 0:
                            outlet.power = [0.0, 0.0, 0.0]
                        gridcell.environment.state.allocated_power = outlet.power_distinct

                        state = gridcell.environment.state.calculate_state()
                        states.append(state)
                        action = ra.randint(0, 1)
                        actions.append(action)
                        gridcell.environment.state.supported_service = action
                        supported.append(action)


                count_zero = 0
                if step <= 2:
                    for ind in range(3):
                        if supported[ind] == 0:
                            count_zero += 1
                    if count_zero == 3:
                        supported[0] = 1
                    outlet.supported_services = supported

                if step > 2:

                    # if step > env_variables.advisor_period[0]  and  step <= env_variables.advisor_period[1] :
                    #     flags = gridcell.agents.heuristic_action(gridcell,
                    #                                           performance_logger.outlet_services_power_allocation_for_all_requested,
                    #                                           performance_logger.outlet_services_requested_number,
                    #                                           performance_logger.number_of_periods_until_now)
                    #     list_flags.extend(flags)


                    if step > env_variables.exploitation_exploration_period[0]  and  step <= env_variables.exploitation_exploration_period[1] :
                        outlet.supported_services = []
                        for serv_index in range(number_of_services):
                            action_centralize, action, flag = gridcell.agents.chain(
                                gridcell.model,
                                gridcell.environment.state.state_value_centralize[j],
                                gridcell.agents.epsilon)

                            if isinstance(action,np.ndarray):
                                action = action.item()
                            outlet.supported_services.append(action)
                            list_flags.append(flag)

                    if env_variables.advisor_period[0] < step <= env_variables.advisor_period[1]:
                        # if step > env_variables.advisor_period[0]  and  step <= env_variables.advisor_period[1]:
                        outlet.supported_services = []

                        for serv_index in range(number_of_services):
                            action_centralize, action, flag = gridcell.agents.exploitation(
                                gridcell.model,
                                gridcell.environment.state.state_value_centralize[j],
                            )
                            # print("flag  exploitaion : ",flag)
                            # actions_objects.append(action_centralize)
                            if isinstance(action,np.ndarray):
                                action = action.item()
                            outlet.supported_services.append(action)
                            list_flags.append(flag)

                    actions.extend(outlet.supported_services)
                print("outlet.supported_services : ", outlet.supported_services)
                outlet.dqn.environment.state.supported_services = outlet.supported_services

            # gridcell.agents.action.command.action_objects = actions_objects
            gridcell.agents.action.command.action_value_centralize = actions
            gridcell.agents.action.command.action_flags = list_flags
            # print("gridcell.agents.action.command.action_objects :  ", gridcell.agents.action.command.action_objects)
            # print("gridcell.agents.action.command.action_value_centralize : ", gridcell.agents.action.command.action_value_centralize)
            # print("lists of flags  : ", gridcell.agents.action.command.action_flags)
            # del actions_objects
            if step <= 2:
                gridcell.environment.state.state_value_centralize = states





    def terminate_service(self, veh, outlets, performance_logger):
        for out in outlets:
            # if out in performance_logger.handled_services:
            #     if veh in performance_logger.handled_services[out] and veh not in env_variables.vehicles:
            #         print("terminate first condition ")
            #         serv = performance_logger.handled_services[out][veh]
            #         self.services_aggregation(performance_logger.outlet_services_requested_number, out,
            #                                   serv.__class__.__name__, -1)
            #
            #         self.ensured_service_aggrigation(performance_logger.outlet_services_ensured_number, out,
            #                                          serv.__class__.__name__,
            #                                          -1)
            #         self.power_aggregation(performance_logger.outlet_services_power_allocation,
            #                                out,
            #                                serv.__class__.__name__, serv, -1)
            #         # print("free on request 1 out of route ")
            #         if out.current_capacity + serv.service_power_allocate < out._max_capacity :
            #             out.current_capacity = out.current_capacity + serv.service_power_allocate
            #             removed_value = performance_logger.handled_services[out].pop(veh)
            #             del removed_value
            #             del serv
            # else:
            #     out.current_capacity = out.current_capacity

            if out not in veh.outlets_serve:
                if out in performance_logger.handled_services:
                    if veh in performance_logger.handled_services[out]:
                        print("terminate second condition ")
                        serv = performance_logger.handled_services[out][veh]
                        self.services_aggregation(performance_logger.outlet_services_requested_number, out,
                                                  serv.__class__.__name__, -1)

                        self.ensured_service_aggrigation(performance_logger.outlet_services_ensured_number, out,
                                                         serv.__class__.__name__, -1)
                        self.power_aggregation(performance_logger.outlet_services_power_allocation,
                                               out,
                                               serv.__class__.__name__, serv, -1)
                        if out.current_capacity + serv.service_power_allocate < out._max_capacity:
                            out.current_capacity = out.current_capacity + serv.service_power_allocate
                            if out.current_capacity >= out._max_capacity:
                                out.current_capacity = out._max_capacity
                            removed_value = performance_logger.handled_services[out].pop(veh)
                            del removed_value
                            del serv

            else:
                out.current_capacity = out.current_capacity

    def run(self):

        steps = 0
        average_qvalue_centralize = []
        # Initialize previous_steps variable
        previous_steps = 0
        frame_rate_for_sending_requests = 1
        previous_steps_sending = 0
        previous_period = 0
        snapshot_time = 5
        previous_steps_centralize = 0
        previous_steps_centralize_action = 0
        previouse_steps_reseting = 0
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
        gc.collect(0)
        build = []
        for i in range(1):
            build.append(RLBuilder())
            gridcells_dqn.append(
                build[i].agent.build_agent(ActionAssignment()).environment.build_env(CentralizedReward(),
                                                                                     CentralizedState()).model_.build_model(
                    "centralized", 12, 2).build())
            print(" path6  : ",path6)
            gridcells_dqn[i].model.load_weights(os.path.join(prev_centralize_weights_path, f'weights_{i}.hdf5'))
            # gridcells_dqn[i].agents.fill_memory(gridcells_dqn[i].agents.memory , os.path.join(prev_centralize_memory_path, f'centralize_buffer.pkl'))
            gridcells_dqn[i].agents.grid_outlets = self.Grids.get(f"grid{i + 1}")
            gridcells_dqn[i].agents.outlets_id = list(range(len(gridcells_dqn[i].agents.grid_outlets)))

        for i in range(1):
            for index, outlet in enumerate(gridcells_dqn[i].agents.grid_outlets):
                outlet.dqn.model.load_weights(os.path.join(prev_decentralize_weights_path, f'weights_{index}.hdf5'))
                outlet.dqn.agents.fill_memory(outlet.dqn.agents.memory , os.path.join(prev_decentralize_memory_path, f'decentralize_buffer{index}.pkl'))
                temp_outlets.append(outlet)
                # print("outlet : ", outlet.__class__.__name__)

        while step < env_variables.TIME:
            # print("env_variables.vehicles : ",env_variables.vehicles)
            # print("............................... : ", performance_logger.handled_services)

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
            # if 0 <= step <= env_variables.period1:
            #     env_variables.number_cars_mean_std['mean'] = 85
            #     env_variables.number_cars_mean_std['std'] = 2
            #     env_variables.threashold_number_veh = 25
            #     env_variables.ENTERTAINMENT_RATIO = 0.2
            #     env_variables.AUTONOMOUS_RATIO = 0.3
            #     env_variables.SAFETY_RATIO = 0.5
            # day time
            # elif env_variables.period1 + 10 < step <= env_variables.period2:
            #     env_variables.number_cars_mean_std['mean'] = 100
            #     env_variables.number_cars_mean_std['std'] = 2
            #     env_variables.threashold_number_veh = 50
            #     env_variables.ENTERTAINMENT_RATIO = 0.3
            #     env_variables.AUTONOMOUS_RATIO = 0.3
            #     env_variables.SAFETY_RATIO = 0.4

            # elif env_variables.period2 + 10 < step <= env_variables.period3:
            env_variables.number_cars_mean_std['mean'] = 150
            env_variables.number_cars_mean_std['std'] = 2
            env_variables.threashold_number_veh = 85
            env_variables.ENTERTAINMENT_RATIO = 0.6
            env_variables.AUTONOMOUS_RATIO = 0.2
            env_variables.SAFETY_RATIO = 0.2

            # elif env_variables.period3 + 10 < step <= env_variables.period4:
            #     env_variables.number_cars_mean_std['mean'] = 100
            #     env_variables.number_cars_mean_std['std'] = 2
            #     env_variables.threashold_number_veh = 50
            #     env_variables.ENTERTAINMENT_RATIO = 0.3
            #     env_variables.AUTONOMOUS_RATIO = 0.3
            #     env_variables.SAFETY_RATIO = 0.4
            #
            # elif env_variables.period4 + 10 < step <= env_variables.period5:
            #     env_variables.number_cars_mean_std['mean'] = 85
            #     env_variables.number_cars_mean_std['std'] = 2
            #     env_variables.threashold_number_veh = 25
            #     env_variables.ENTERTAINMENT_RATIO = 0.2
            #     env_variables.AUTONOMOUS_RATIO = 0.3
            #     env_variables.SAFETY_RATIO = 0.5

            # if steps - previous_steps_sending == frame_rate_for_sending_requests:
            #     previous_steps_sending = steps
            number_of_cars_will_send_requests = round(len(list(env_variables.vehicles.values())) * 0.1)
            vehicles = ra.sample(list(env_variables.vehicles.values()), number_of_cars_will_send_requests)
            list(map(lambda veh: self.requests_buffering(veh, observer, performance_logger, steps, previous_period),
                     vehicles))
            if steps == 2:
                self.centralize_state_action(gridcells_dqn, steps, performance_logger)

            if steps - previous_period >= 10:
                previous_period = steps
                self.decentralize_period(performance_logger, gridcells_dqn, step)
                for i, outlet in enumerate(gridcells_dqn[0].agents.grid_outlets):
                    performance_logger.outlet_services_ensured_number_with_action_period[outlet] = [0, 0, 0]
                    performance_logger.outlet_services_requested_number_with_action_period[outlet] = [0, 0, 0]
                    performance_logger.outlet_services_power_allocation_with_action_period[outlet] = [0, 0, 0]
                    # performance_logger.outlet_services_power_allocation_without_accumilated_with_action_period[
                    #     outlet] = []
                list(map(lambda veh: self.terminate_service(veh, outlets, performance_logger),
                         env_variables.vehicles.values()))

            if steps - previous_steps_centralize_action >= 40:
                previous_steps_centralize_action = steps
                self.centralize_nextstate_reward( gridcells_dqn)
                self.centralize_state_action(gridcells_dqn, step, performance_logger)



            for axs_ in [axs, axs_Qvalue_centralize,
                         axs_Qvalue_decentralize]:
                if hasattr(axs_, 'flatten'):
                    for ax in axs_.flatten():
                        ax.legend()
                        ax.relim()
                        ax.autoscale_view()
                else:
                    axs_.legend()
                    axs_.relim()
                    axs_.autoscale_view()

            if axs is axs:
                fig.canvas.draw()
            # elif axs is axs_reward_decentralize:
            #     fig_reward_decentralize.canvas.draw()
            # elif axs is axs_reward_centralize:
            #     fig_reward_centralize.canvas.draw()
            elif axs is axs_Qvalue_centralize:
                axs_Qvalue_centralize.canvas.draw()
            elif axs is axs_Qvalue_decentralize:
                axs_Qvalue_decentralize.canvas.draw()

            if steps - prev == snapshot_time:
                prev = steps
                path1 = os.path.join(p1, f'snapshot')
                path2 = os.path.join(p2, f'snapshot')
                path3 = os.path.join(p3, f'snapshot')
                path4 = os.path.join(p4, f'snapshot')
                path5 = os.path.join(p5, f'snapshot')
                fig.set_size_inches(10, 8)
                fig_reward_centralize.set_size_inches(15, 10)
                fig_reward_decentralize.set_size_inches(30, 20)  # set physical size of plot in inches
                fig_Qvalue_centralize.set_size_inches(15, 10)
                fig_Qvalue_decentralize.set_size_inches(30, 20)
                fig.savefig(path1 + '.svg', dpi=300)
                # fig_reward_decentralize.savefig(path2 + '.svg', dpi=300)
                # fig_reward_centralize.savefig(path3 + '.svg', dpi=300)
                fig_Qvalue_decentralize.savefig(path4 + '.svg', dpi=300)
                fig_Qvalue_centralize.savefig(path5 + '.svg', dpi=300)
            else:
                plt.close(fig)
                # plt.close(fig_reward_decentralize)
                # plt.close(fig_reward_centralize)
                plt.close(fig_Qvalue_centralize)
                plt.close(fig_Qvalue_decentralize)

            if steps - previous_steps >= env_variables.decentralized_replay_buffer:
                previous_steps = steps
                qvalue = []
                for ind, gridcell_dqn in enumerate(gridcells_dqn):
                    for i, outlet in enumerate(gridcell_dqn.agents.grid_outlets):
                        if len(outlet.dqn.agents.memory) > 31:
                            # print("replay buffer of decentralize ")
                            outlet.qvalue = outlet.dqn.agents.replay_buffer_decentralize(30,
                                                                                         outlet.dqn.model)
                            qvalue.append(outlet.qvalue)

            # if steps - previous_steps_centralize >= env_variables.centralized_replay_buffer:
            #     previous_steps_centralize = steps
            #     for ind, gridcell_dqn in enumerate(gridcells_dqn):
            #         if len(gridcell_dqn.agents.memory) >= 64:
            #             # print("replay buffer of centralize ")
            #             average_qvalue_centralize.append(gridcell_dqn.agents.replay_buffer_centralize(32,
            #                                                                                           gridcell_dqn.model))

            if steps - previouse_steps_reseting >= env_variables.episode_steps:
                # print("reset the environment : ")
                previouse_steps_reseting = steps
                list_ = []
                # avg_qvalue = (sum(average_qvalue_centralize) / len(average_qvalue_centralize))
                # print("avg_qvalue : ", avg_qvalue)
                for ind, gridcell_dqn in enumerate(gridcells_dqn):
                    # gridcell_dqn.environment.reward.gridcell_reward_episode = sum(
                    #     gridcell_dqn.environment.reward.reward_value)
                    # update_lines_reward_centralized(lines_out_reward_centralize, steps, gridcells_dqn)
                    # update_lines_Qvalue_centralized(lines_out_Qvalue_centralize, steps, avg_qvalue
                    #                                 )

                    # self.add_value_to_pickle(
                    #         os.path.join(centralize_qvalue_path, f'qvalue.pkl'),
                    #         avg_qvalue)
                    update_lines_outlet_utility(lines_out_utility, steps, temp_outlets)
                    update_lines_outlet_requested(lines_out_requested, steps, temp_outlets)
                    update_lines_outlet_ensured(lines_out_ensured, steps, temp_outlets)
                    update_lines_Qvalue_decentralized(lines_out_Qvalue_decentralize, steps, temp_outlets)
                    update_lines_reward_decentralized(lines_out_reward_decentralize, steps, temp_outlets)

                    for i, out in enumerate(gridcell_dqn.agents.grid_outlets):
                        self.add_value_to_pickle(
                            os.path.join(decentralize_qvalue_path, f'qvalue{i}.pkl'),
                            out.qvalue)
                        out.dqn.environment.reward.episode_reward_decentralize = out.dqn.environment.reward.reward_value
                        # print("out.qvalue  : ", out.qvalue)
                        # self.add_value_to_text(
                        #     f"H://work_projects//network_slicing//ns//results//qvalue{i}.txt",
                        #     out.qvalue)

                        # out.dqn.environment.state.resetsate(out._max_capacity)
                        out.dqn.environment.reward.reward_value = 0
                        out.dqn.environment.state.mean_power_allocated_requests = 0.0
                        # out.dqn.environment.state.state_value_decentralize = out.dqn.environment.state.calculate_state()
                        out.dqn.environment.state.state_value_decentralize = [[0.0] * 17 for _ in range(3)]
                        out.current_capacity = out._max_capacity
                        # print("the max : ", out._max_capacity)
                        # print("reset capacity : ", out.current_capacity)
                        list_.append(out._max_capacity)

                    gridcell_dqn.environment.reward.resetreward()
                    gridcell_dqn.environment.state.resetsate(list_)
                    gridcell_dqn.environment.reward.reward_value = 0
                    states = []
                    for j, outlet in enumerate(gridcell_dqn.agents.grid_outlets):
                        for i in range(3):
                            gridcell_dqn.environment.state.index_outlet = j
                            gridcell_dqn.environment.state.index_service = i
                            state = gridcell_dqn.environment.state.calculate_state()
                            states.append(state)
                    gridcell_dqn.environment.state.state_value_centralize = states
                performance_logger.reset_state_decentralize_requirement()
                average_qvalue_centralize = []

            step += 1

            if step == env_variables.TIME:
                # for i in range(1):
                #     print()
                    # gridcells_dqn[i].model.save_weights(os.path.join(path6, f'weights_{i}.hdf5'))
                    # gridcells_dqn[i].agents.free_up_memory(gridcells_dqn[i].agents.memory , os.path.join(path_memory_centralize, f'centralize_buffer.pkl'))

                for index, g in enumerate(temp_outlets):
                    g.dqn.model.save_weights(os.path.join(path7, f'weights_{index}.hdf5'))
                    g.dqn.agents.free_up_memory(g.dqn.agents.memory,os.path.join(path_memory_decentralize, f'decentralize_buffer{index}.pkl'))


                # shutil.copytree(results_dir, prev_results_dir)
                print("Folder contents copied successfully.")




        plt.close()
        traci.close()
