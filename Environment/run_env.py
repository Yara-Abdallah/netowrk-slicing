import traci
from Environment import env_variables
import xml.etree.ElementTree as ET
import random
from uuid import uuid4
from Outlet.Cellular.ThreeG import ThreeG
from Utils.Bandwidth import Bandwidth
from Utils.Cost import TowerCost, RequestCost
from Utils.PerformanceLogger import PerformanceLogger
from Utils.config import outlet_types
from Vehicle.Car import Car
from Outlet.Cellular.FactoryCellular import FactoryCellular
from Vehicle.VehicleOutletObserver import ConcreteObserver
#from Utils.FileLoggingInfo import Logger


class Environment:
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

    def get_all_outlets(self):
        """
        get all outlets and add id with position to env variables
        """
        outlets = []
        poi_ids = traci.poi.getIDList()
        for id_ in poi_ids:
            type_poi = traci.poi.getType(id_)
            if type_poi in env_variables.types_outlets:
                position_ = traci.poi.getPosition(id_)
                env_variables.outlets[type_poi].append((id_, position_))
                print()
                factory = FactoryCellular(outlet_types[str(type_poi)],1, 1, [1, 1, 0], [position_[0], position_[1]], 10000, [10, 20, 30],
                                          [10, 10, 10])
                outlet = factory.produce_cellular_outlet(str(type_poi))
                outlets.append(outlet)
        return outlets

    def select_outlets_to_show_in_gui(self):
        """
        select outlets in network to display type of each outlet
        """
        for key in env_variables.outlets.keys():
            for id_, _ in env_variables.outlets[key]:
                self.gui.toggleSelection(id_, 'poi')

    def get_positions_of_outlets(self):
        positions_of_outlets = []
        outlets = self.get_all_outlets()
        for out in outlets:
            positions_of_outlets.append(out.position)
        return positions_of_outlets, outlets

    def generate_vehicles(self, number_vehicles):
        """
        It generates vehicles and adds it to the simulation
        and get random route for each vehicle from routes in env_variables.py
        :param number_vehicles: number of vehicles to be generated
        """
        for i in range(number_vehicles):
            id_route_ = random.choice(env_variables.all_routes)
            uid = str(uuid4())
            self.vehicle.add(vehID=uid, routeID=id_route_)

    def starting(self):
        """
        The function starts the simulation by calling the sumoBinary, which is the sumo-gui or sumo
        depending on the nogui option
        """
        sumo_cmd = ["sumo-gui", "-c", env_variables.network_path]
        traci.start(sumo_cmd)
        self.get_all_outlets()
        self.prepare_route()

    def remove_vehicles_arrived(self):
        """
        Remove vehicles which removed from the road network ((have reached their destination) in this time step
        the add to env_variables.vehicles (dictionary)
        """
        ids_arrived = self.simulation.getArrivedIDList()
        for id_ in ids_arrived:
            del env_variables.vehicles[id_]

    def add_new_vehicles(self):
        """
        Add vehicles which inserted into the road network in this time step.
        the add to env_variables.vehicles (dictionary)
        """
        ids_new_vehicles = self.simulation.getDepartedIDList()
        for id_ in ids_new_vehicles:
            env_variables.vehicles[id_] = Car(id_, 0, 0)

    def outlets_logging(self, outlet_num, outlet ,cars):
        return f"Outlet {outlet_num} : -> {outlet}   -  Number Of Cars Which Send Request To It -> {len(cars)} \n "

    def car_services_logging(self, car_num, car, service):
        return f"  The Car {car_num} Which Send To It -> : {car} \n" \
               f"     And Its Services Is  ->  : {service} \n"

    def logging_the_final_results(self, performance_logger):
        service_handled = performance_logger.service_handled
        for i, outer_key in enumerate(service_handled):
            num = 0
            print(self.outlets_logging(i, outer_key,service_handled[outer_key]))
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

    def car_interact(self, car, observer, performance_logger):
        car.attach(observer)
        car.set_state(car.get_x(), car.get_y())
        info = car.send_request()
        car = info[1][1]
        service = info[1][2]
        outlet = info[0]
        performance_logger.service_requested = {car: service}
        performance_logger.set_service_handled(outlet, car, service)
        request_bandwidth = Bandwidth(service.bandwidth, service.criticality)
        request_cost = RequestCost(request_bandwidth, service.realtime)
        request_cost.cost_setter(service.realtime)
        cost = request_cost.cost
        print(f"request cost from car {car.get_id()} : ->  {service.__class__.__name__,service.bandwidth,cost} \n ")
        performance_logger.power_costs.append(cost)
        tower_cost=TowerCost(request_bandwidth, service.realtime)
        tower_cost.cost_setter(service.realtime)
        cost2 =   tower_cost.cost
        print(f"tower cost after send request from  {car.get_id()} : ->  {cost2} \n ")

        # print(f"performance logger service_requested >>>>>>>>>>> : {len(performance_logger.service_requested)} \n ")
        # print(f"performance logger services_handled  >>>>>>>>>>> : {((performance_logger.service_handled[outlet]))} \n ")

    def run(self):

        self.starting()
        step = 0
        print("\n")

        outlets_pos, outlets = self.get_positions_of_outlets()
        observer = ConcreteObserver(outlets_pos, outlets)
        performance_logger = PerformanceLogger()


        while step < env_variables.TIME:
            traci.simulationStep()
            print("step is ....................................... ", step)
            self.get_current_vehicles()

            # print('============================================================')
            # print('the vehicles in sumo: {}'.format(traci.vehicle.getIDCount()))
            # print('the vehicles in env: {}'.format(len(env_variables.vehicles)))
            # print('the arrived in env: {}'.format(len(traci.simulation.getArrivedIDList())))
            # print('the derpated in env: {}'.format(len(traci.simulation.getDepartedIDList())))

            if step == 0:
                self.generate_vehicles(150)
                self.select_outlets_to_show_in_gui()

            list(map(lambda veh: self.car_interact(veh, observer, performance_logger), env_variables.vehicles.values()))

            step += 1
            if step == 10:
                #print("........... ", (performance_logger.power_costs))
                self.logging_the_final_results(performance_logger)
                break

        traci.close()
