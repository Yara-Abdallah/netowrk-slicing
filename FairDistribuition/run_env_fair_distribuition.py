import math

import traci
from Environment import env_variables
import xml.etree.ElementTree as ET
import random
from uuid import uuid4

from FairDistribuition.FairDistribuition import FairDistribuition
from Greedy.greedy import Greedy
from GridCell.GridCell import GridCell
from Outlet.Sat.sat import Satellite
from Utils.Bandwidth import Bandwidth
from Utils.Cost import TowerCost, RequestCost
from Utils.PerformanceLogger import PerformanceLogger
from Utils.config import outlet_types, Grids
from Vehicle.Car import Car
from Outlet.Cellular.FactoryCellular import FactoryCellular
from Vehicle.VehicleOutletObserver import ConcreteObserver
import numpy as np
import matplotlib.pyplot as plt

fig, axs = plt.subplots(nrows=5, ncols=3, figsize=(100, 32))
fig.subplots_adjust(hspace=0.8)

lines_out_utility = []
lines_out_requested = []
lines_out_ensured = []


def plotting_Utility_Requested_Ensured():
    j = 0
    for i in range(5):
        row = 0
        line, line1, line2 = 0, 0, 0
        for index in range(3):
            if index == 0:
                color_str = 'b'
            elif index == 1:
                color_str = 'r'
            elif index == 2:
                color_str = 'g'
            line, = axs.flatten()[j].plot([], [], label=f"O{row + index + 1} utility", color=color_str)
            line1, = axs.flatten()[j + 1].plot([], [], label=f"O{row + index + 1} requested", color=color_str)
            line2, = axs.flatten()[j + 2].plot([], [], label=f"O{row + index + 1} ensured", color=color_str)
            lines_out_utility.append(line)
            lines_out_requested.append(line1)
            lines_out_ensured.append(line2)
        j += 3


plotting_Utility_Requested_Ensured()



fig_satellite, axs_satellite = plt.subplots(nrows=1, ncols=1, figsize=(30, 22))
fig_satellite.subplots_adjust(hspace=0.8)

lines_satellite_utility = 0
satellite_utility=[]
def plotting_satellite():
    lines_satellite_utility, = axs_satellite.plot([], [], label=f"satellite utility", color='b')
    return lines_satellite_utility


lines_satellite_utility = plotting_satellite()

class Environment:
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
            # print(child_root.tag, child_root.attrib)
            id_ = child_root.attrib['id']
            for child in child_root:
                # print(child.tag, child.attrib)
                edges_ = list((child.attrib['edges']).split(' '))
                # print('the id: {}  , edges: {}'.format(id_, edges_))
                self.route.add(id_, edges_)
                env_variables.all_routes.append(id_)

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
                # self.poi.add(id_, position_[0], position_[1],color=(255, 255, 0,255), size=100)
                raduis = 0.0
                if str(type_poi) == 'wifi':
                    raduis = 100.0
                elif str(type_poi) == '3G':
                    raduis = 500.0
                elif str(type_poi) == '4G':
                    raduis = 1000.0
                elif str(type_poi) == '5G':
                    raduis = 10000.0
                factory = FactoryCellular(outlet_types[str(type_poi)], 1, 1, [1, 1, 0], id_,
                                          [position_[0], position_[1]],
                                          raduis, [],
                                          [10, 10, 10])
                outlet = factory.produce_cellular_outlet(str(type_poi))
                outlet.outlet_id = id_
                outlet.radius = raduis
                outlets.append(outlet)

        list(map(lambda x: append_outlets(x), poi_ids))

        satellite = Satellite(1, 1, [1, 1, 0], 0, [0, 0],
                              10000000000, [],
                              [10, 10, 10])
        outlets.append(satellite)

        return outlets

    @staticmethod
    def fill_grids(outlets):
        Grids = {
            "grid1": [],
            "grid2": [],
            "grid3": [],
            "grid4": [],
        }
        grids = [outlets[i:i + 3] for i in range(0, len(outlets), 3)]

        def grid_namer(i, grid):
            name = "grid" + str(i + 1)
            Grids[name] = grid

        list(map(lambda x: grid_namer(x[0], x[1]), enumerate(grids)))
        return Grids

    def select_outlets_to_show_in_gui(self):
        """
        select outlets in network to display type of each outlet
        """
        from itertools import chain
        array = list(map(lambda x: x, chain(*list(map(lambda x: x[1], env_variables.outlets.items())))))
        list(map(lambda x: self.gui.toggleSelection(x[0], 'poi'), map(lambda x: x, array)))

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

        list(map(add_vehicle, random.choices(all_routes, k=number_vehicles)))

    def starting(self):
        """
        The function starts the simulation by calling the sumoBinary, which is the sumo-gui or sumo
        depending on the nogui option
        """
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
            env_variables.vehicles[id_] = None

        list(map(remove_vehicle, ids_arrived))

    def add_new_vehicles(self):
        """
        Add vehicles which inserted into the road network in this time step.
        the add to env_variables.vehicles (dictionary)
        """
        ids_new_vehicles = self.simulation.getDepartedIDList()

        def create_vehicle(id_):
            env_variables.vehicles[id_] = Car(id_, 0, 0)

        list(map(create_vehicle, ids_new_vehicles))

    def outlets_logging(self, outlet_num, outlet, cars):
        return f"Outlet {outlet_num} : -> {outlet}   -  Number Of Cars Which Send Request To It -> {len(cars)} \n "

    def car_services_logging(self, car_num, car, service):
        return f"  The Car {car_num} Which Send To It -> : {car} \n" \
               f"     And Its Services Is  ->  : {service} \n"

    def logging_the_final_results(self, performance_logger):
        service_handled = performance_logger.service_handled

        for i, outer_key in enumerate(service_handled):
            num = 0
            print(self.outlets_logging(i, outer_key, service_handled[outer_key]))
            for key, value in performance_logger.service_handled[outer_key].items():
                num += 1
                print(self.car_services_logging(num, key, value))

    def get_current_vehicles(self):
        """
        :return: vehicles that running in road network in this time step
        """
        self.remove_vehicles_arrived()
        self.add_new_vehicles()
        return env_variables.vehicles

    def ensured_service_aggrigation(self, performance_logger, outlet, service_type, action_value):

        if outlet not in performance_logger._outlet_services_ensured_number:
            performance_logger.set_outlet_services_ensured_number(outlet, [0, 0, 0])

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

    def services_aggregation(self, performance_logger, outlet, service_type, request_cost):
        if outlet not in performance_logger._outlet_services_requested_number:
            performance_logger.set_outlet_services_requested_number(outlet, [0, 0, 0])

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

    def euclidian_distance(self,outlet,car):
        result = math.sqrt(
            (outlet.position[0] - car.x) ** 2 + (outlet.position[1] - car.y) ** 2
        )
        return result

    def calculate_outlet_utility(self, outlet):
        if sum(outlet.services_requested) == 0 and sum(
                outlet.services_ensured) == 0:
            outlet.utility = 0
        elif sum(outlet.services_requested) != 0 and sum(
                outlet.services_ensured) != 0:
            outlet.utility = np.round((sum(outlet.services_ensured) / sum(
                outlet.services_requested)) * 10)
        elif sum(outlet.services_ensured) == 0:
            outlet.utility = 0


    def requested_ensured_aggregation(self,outlet,performance_logger,car, service,request_bandwidth,request_cost,greedy,tower_cost):

        if outlet._max_capacity != 0 and outlet._max_capacity > request_bandwidth.allocated:
            performance_logger.set_service_handled(outlet, car, service)
            performance_logger.set_service_power_allocate(service, request_bandwidth.allocated)

            # print(f"outlet type {outlet.__class__.__name__} , max capacity {outlet._max_capacity} , request_capacity : {request_bandwidth.allocated}")
            self.services_aggregation(performance_logger, outlet, service.__class__.__name__, request_cost.cost)
            # print(f"capacity is: {outlet._max_capacity} MBps outlet type : {outlet.__class__.__name__}")
            outlet._max_capacity = outlet._max_capacity - request_bandwidth.allocated
            # print(f"tower capacity after send request from  {car.get_id()} : ->  {outlet._max_capacity} \n ")
            tower_cost.cost = outlet._max_capacity
            outlet.services_requested = performance_logger.outlet_services_requested_number[outlet]
            # print(f" outlet service requested : {outlet} , {outlet.services_requested}")
            self.ensured_service_aggrigation(performance_logger, outlet, service.__class__.__name__,
                                             greedy.request_response_reject)
            outlet.services_ensured = performance_logger.outlet_services_ensured_number[outlet]
            # print(f" outlet service ensured : {outlet} , {outlet.services_ensured}")

        if request_bandwidth.allocated > outlet.max_capacity:
            # print(f"outlet type {outlet.__class__.__name__} , max capacity {outlet._max_capacity} , request_capacity : {request_bandwidth.allocated}")
            self.services_aggregation(performance_logger, outlet, service.__class__.__name__, request_cost.cost)
            outlet.services_requested = performance_logger.outlet_services_requested_number[outlet]
    def car_interact(self, car, observer, performance_logger, gridcells_dqn, outlets, greedy):
        # car.outlets_serve.append(outlets[-1])

        car.attach(observer)
        car.set_state(car.get_x(), car.get_y())

        car.add_satellite(outlets[-1])

        info = car.send_request()
        car = info[1][1]
        service = info[1][2]
        outlet_ = info[0]
        # print("outlet name : ", outlet_.__class__.__name__)

        # print("outlet is : ", outlet)
        # print("outlet . max capacity : ",outlet.max_capacity)

        performance_logger.service_requested = {car: service}

        # .................................................................................................

        request_bandwidth = Bandwidth(service.bandwidth, service.criticality)
        request_cost = RequestCost(request_bandwidth, service.realtime)
        request_cost.cost_setter(service.realtime)
        # print(f"request cost from car {car.get_id()} : ->  {service.__class__.__name__, service.bandwidth, request_cost.cost} \n ")
        performance_logger.request_costs.append(request_cost.cost)

        tower_cost = TowerCost(request_bandwidth, service.realtime)
        tower_cost.cost_setter(service.realtime)
        performance_logger.power_costs.append(tower_cost.cost)
        # print(f"bandwidth_demand is:{request_bandwidth.allocated:.2f} ")

        if len(outlet_.power_distinct[0]) == 0:
            outlet_.power = [0.0, 0.0, 0.0]
            performance_logger.set_outlet_services_requested_number(outlet_, [0, 0, 0])
            performance_logger.set_outlet_services_ensured_number(outlet_, [0, 0, 0])
            performance_logger.set_outlet_utility(outlet_, 0.0)
            performance_logger.set_outlet_occupancy(outlet_, 0.0)

        utilities = []
        outlets_grid = []
        grid = 0
        grid_number = 0
        outlets_filtered = []
        distances=[]
        for ind, gridcell_dqn in enumerate(gridcells_dqn):
            gridcell_dqn.services_requested = [0, 0, 0]
            gridcell_dqn.services_ensured = [0, 0, 0]
            performance_logger.set_gridcell_utility(gridcell_dqn, 0.0)

            times = [0, 0, 0]

            for i, outlet in enumerate(gridcell_dqn.grid_outlets):
                if outlet_ == outlet:
                    grid = gridcell_dqn
                    grid_number = ind

                else :
                    self.calculate_outlet_utility(outlet)
                    if len(outlet.power_distinct[0]) == 0:
                        outlet.power = [0.0, 0.0, 0.0]
                        performance_logger.set_outlet_services_requested_number(outlet, [0, 0, 0])
                        performance_logger.set_outlet_services_ensured_number(outlet, [0, 0, 0])
                        performance_logger.set_outlet_utility(outlet, 0.0)

                    if outlet.__class__.__name__ == 'Satellite':
                        # print("satellite_utility : ", outlet.utility)
                        satellite_utility.append(outlet.utility)

                    self.requested_ensured_aggregation(outlet, performance_logger, info[1][1], service,
                                                       request_bandwidth, request_cost,greedy,tower_cost)





        # print("the grid is : ", grid)
        # print("the number of grid is : ", grid_number)
        if grid!=0:
            for i, outlet in enumerate(grid.grid_outlets):
                outlet.distinct = grid.outlets_id[i]
                if outlet in car.outlets_serve:
                    outlets_filtered.append(outlet)

            # print("outlets_filtered : ", outlets_filtered)

            for i, outlet in enumerate(outlets_filtered):

                self.calculate_outlet_utility(outlet)

                performance_logger.set_outlet_utility(outlet, outlet.utility)

                if len(outlet.power_distinct[0]) == 0:
                    outlet.power = [0.0, 0.0, 0.0]
                    performance_logger.set_outlet_services_requested_number(outlet, [0, 0, 0])
                    performance_logger.set_outlet_services_ensured_number(outlet, [0, 0, 0])
                    performance_logger.set_outlet_utility(outlet, 0.0)

                utilities.append(outlet.utility)
                distances.append(self.euclidian_distance(outlet, car))
                outlets_grid.append(outlet)

                grid.allocated_power = outlet.power_distinct
                grid.supported_services = outlet.supported_services_distinct

                grid.services_requested = grid.services_requested + outlet.services_requested
                grid.services_ensured = grid.services_ensured + outlet.services_ensured

                # print(f"service requested in grid {grid_number} , {grid.services_requested}")
                # print(f"service requested in outlet {i} , {outlet.services_requested}")
                #
                # print(f"service ensured in grid {grid_number} , {grid.services_ensured}")
                # print(f"service ensured in outlet {i} , {outlet.services_ensured}")
                #
                # print(f"utility of outlet {i} , {outlet.utility}")
                #
                # print("utilities ................................. ", utilities)
                # print("index distances ", utilities.index(min(utilities)))
                outlet = outlets_grid[utilities.index(min(utilities))]
                # print(f"minimum outlet : {outlet} , utility {outlet.utility} , its capacity is : {outlet._max_capacity}")


                for i in range(utilities.index(min(utilities))):
                    outlet = outlets_grid[i]
                    # print(f"outlet type {outlet.__class__.__name__} , max capacity {outlet._max_capacity} , request_capacity : {request_bandwidth.allocated}")
                    self.services_aggregation(performance_logger, outlet, service.__class__.__name__, request_cost.cost)
                    outlet.services_requested = performance_logger.outlet_services_requested_number[outlet]

                self.requested_ensured_aggregation(outlet,performance_logger,info[1][1], service,request_bandwidth,request_cost,greedy,tower_cost)

    def terminate_service(self, veh, outlets, performance_logger):
        for out in outlets:
            if out not in veh.outlets_serve:
                if out in performance_logger.handled_services:
                    if veh in performance_logger.handled_services[out]:
                        serv = performance_logger.handled_services[out][veh]
                        out._max_capacity = out._max_capacity + performance_logger.service_power_allocate[serv]
            else:
                out._max_capacity = out._max_capacity

    def run(self):
        gridcells_dqn = []
        self.starting()
        fair_distribuition = FairDistribuition()

        outlets = self.get_all_outlets()
        self.Grids = self.fill_grids(outlets)
        step = 0
        print("\n")
        outlets_pos = self.get_positions_of_outlets(outlets)
        observer = ConcreteObserver(outlets_pos, outlets)
        performance_logger = PerformanceLogger()

        gridcell1 = GridCell()
        gridcell1.grid_outlets = self.Grids.get("grid1")
        gridcell1.outlets_id = list(range(len(gridcell1.grid_outlets)))
        gridcell2 = GridCell()
        gridcell2.grid_outlets = self.Grids.get("grid2")
        gridcell2.outlets_id = list(range(len(gridcell2.grid_outlets)))

        gridcell3 = GridCell()
        gridcell3.grid_outlets = self.Grids.get("grid3")
        gridcell3.outlets_id = list(range(len(gridcell3.grid_outlets)))

        gridcell4 = GridCell()
        gridcell4.grid_outlets = self.Grids.get("grid4")
        gridcell4.outlets_id = list(range(len(gridcell4.grid_outlets)))

        gridcell5 = GridCell()
        gridcell5.grid_outlets = self.Grids.get("grid5")
        gridcell5.outlets_id = list(range(len(gridcell5.grid_outlets)))

        # gridcell6 = GridCell()
        # gridcell6.grid_outlets = self.Grids.get("grid6")
        # gridcell6.outlets_id = list(range(len(gridcell6.grid_outlets)))
        #
        # gridcell7 = GridCell()
        # gridcell7.grid_outlets = self.Grids.get("grid7")
        # gridcell7.outlets_id = list(range(len(gridcell7.grid_outlets)))

        gridcells_dqn.append(gridcell1)
        gridcells_dqn.append(gridcell2)
        gridcells_dqn.append(gridcell3)
        gridcells_dqn.append(gridcell4)
        gridcells_dqn.append(gridcell5)
        # gridcells_dqn.append(gridcell6)
        # gridcells_dqn.append(gridcell7)

        steps = 0

        # Initialize previous_steps variable
        previous_steps = 0
        snapshot_time = 2
        prev = 0
        temp_outlet_reward = []
        poi_ids = traci.poi.getIDList()
        temp_outlets = []

        for i in range(5):
            for index, outlet in enumerate(gridcells_dqn[i].grid_outlets):
                temp_outlets.append(outlet)

        while step < env_variables.TIME:
            steps += 1
            traci.simulationStep()
            print("step is ....................................... ", step)
            self.get_current_vehicles()
            if step == 0:
                self.generate_vehicles(250)
                self.select_outlets_to_show_in_gui()
            list(map(lambda veh: self.car_interact(veh, observer, performance_logger, gridcells_dqn, outlets,
                                                   fair_distribuition),
                     env_variables.vehicles.values()))

            # list(map(lambda veh: self.terminate_service(veh, outlets, performance_logger),
            #          env_variables.vehicles.values()))
            v_number = 0
            for veh in env_variables.vehicles.values():
                v_number += 1
                self.terminate_service(veh, outlets, performance_logger),

            for i in range(5):
                for index, outlet in enumerate(gridcells_dqn[i].grid_outlets):
                    self.update_outlet_color(outlet.outlet_id, outlet.utility)

            for j, line in enumerate(lines_out_utility):
                x_data, y_data = line.get_data()
                x_data = np.append(x_data, steps)
                y_data = np.append(y_data, temp_outlets[j].utility)
                # print(x_data.shape, " utility ", y_data.shape, "outlet num : ", j, " value : ",temp_outlets[j].utility)  # print the shape
                line.set_data(x_data, y_data)

            for j, line1 in enumerate(lines_out_requested):
                x_data, y_data = line1.get_data()
                x_data = np.append(x_data, steps)
                y_data = np.append(y_data, sum(temp_outlets[j].services_requested))
                # print(x_data.shape, " requested ", y_data.shape, "outlet num : ", j, " value : ",
                #       sum(temp_outlets[j].services_requested))  # print the shape

                line1.set_data(x_data, y_data)

            for j, line2 in enumerate(lines_out_ensured):
                x_data, y_data = line2.get_data()
                x_data = np.append(x_data, steps)
                y_data = np.append(y_data, sum(temp_outlets[j].services_ensured))
                # print(x_data.shape, " 3 ", y_data.shape, "outlet num : ", j, " value : ",
                #       sum(temp_outlets[j].services_ensured))  # print the shape

                line2.set_data(x_data, y_data)

            for j, utility in enumerate(satellite_utility):
                x_data, y_data = lines_satellite_utility.get_data()
                x_data = np.append(x_data, steps)
                y_data = np.append(y_data,utility)
                lines_satellite_utility.set_data(x_data, y_data)

            for ax in axs.flatten():
                ax.legend()
                ax.relim()
                ax.autoscale_view()

            axs_satellite.legend()
            axs_satellite.relim()
            axs_satellite.autoscale_view()

            # fig_satellite.canvas.draw()
            fig.canvas.draw()

            if steps - prev == snapshot_time:
                prev = steps
                path1 = f'I://Documents//fair_distribuition_utility//snapshot{steps}'
                path2 = f'I://Documents//fair_distribuition_satellite//snapshot{steps}'
                fig.savefig(path1 + '.png')
                fig_satellite.savefig(path2 + '.png')

                plt.pause(0.001)

            if steps % 2 == 0:
                plt.pause(0.001)

            step += 1
            if step == 24 * 60 * 7:
                self.logging_the_final_results(performance_logger)
                break

        plt.show()
        plt.close()
        traci.close()
