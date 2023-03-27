import traci
import env_variables
import xml.etree.ElementTree as ET
import random
from uuid import uuid4

def prepare_route():
    path_file = 'F:\\Rachis_systems\\ns\Environment\Area\map.rou.xml'
    tree = ET.parse(path_file)
    root = tree.getroot()
    for child_root in root:
        # print(child_root.tag, child_root.attrib)
        id_ = child_root.attrib['id']
        for child in child_root:
            # print(child.tag, child.attrib)
            edges_ = list((child.attrib['edges']).split(' '))
            # print('the id: {}  , edges: {}'.format(id_, edges_))
            traci.route.add(id_, edges_)
            env_variables.all_routes.append(id_)


def prepare_types_vehicles():
    car = traci.vehicletype.VehicleType("car")




def generate_vehicles(number_vehicles):
    """
    It generates a random route for each vehicle and adds it to the simulation

    :param number_vehicles: number of vehicles to be generated
    """
    car = traci.vehicletype.getIDList()
    for i in range(number_vehicles):

        id_route_ = random.choice(env_variables.all_routes)

        uid = str(uuid4())

        traci.vehicle.add(vehID='Veh' + uid, routeID=id_route_)
        # traci.vehicle.setLength('Veh' + uid, Vehicle_characteristics['length'])
        # traci.vehicle.setMinGap('Veh' + uid, Vehicle_characteristics['min_cap'])
        # print('the route {} is to car {}'.format([edge1,edge2] , 'Veh'+uid))

net_path = 'F:\\Rachis_systems\\ns\Environment\Area\map.sumocfg'

sumoCmd = ["sumo-gui", "-c", net_path]
traci.start(sumoCmd)


def get_polygons():
    all_polygon_ = traci.polygon.getIDList()
    return all_polygon_


def get_builds(id_list):
    all_builds_ = []
    for id_poly in id_list:
        if traci.polygon.getType(id_poly) == 'building':
            all_builds_.append(id_poly)
    return all_builds_


def get_all_types_of_polygons(id_list):
    all_types_ = []
    for id_poly in id_list:
        all_types_.append(traci.polygon.getType(id_poly))
    return list(set(all_types_))


def get_types_of_poi():
    id_poi_ = traci.poi.getIDList()
    types_ = []
    for id in id_poi_:
        types_.append(traci.poi.getType(id))
    return set(types_)


def get_all_outlets():
    poi_ids = traci.poi.getIDList()
    for id_ in poi_ids:
        type_poi = traci.poi.getType(id_)
        if type_poi in env_variables.types_outlets:
            env_variables.outlets[type_poi].append(id_)


def get_routes():
    routes_ = traci.route.getIDList()
    env_variables.all_routes.extend(routes_)
    route_ = set(env_variables.all_routes)
    env_variables.all_routes = list(route_)

# print("count of polygons in network: {}".format(len(get_polygons())))
# print("count of builds in network: {}".format(len(get_builds(get_polygons()))))
# print("all types of polygons in network: {}".format((get_all_types_of_polygons((get_polygons())))))
# print('count of types: {}'.format((len(get_all_types_of_polygons((get_polygons()))))))
# print('count of poiS: {}'.format(traci.poi.getIDCount()))
# print('the count of poi in network: {}'.format(traci.poi.getIDCount()))
# print('the types of poi in network: {}'.format(get_types_of_poi()))
get_all_outlets()
prepare_route()
step = 0
# traci.polygon.
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    if step % 50 == 0:
        # generate_vehicles(10)
        # get_routes()
        # print(env_variables.all_routes)
        # print("the count of routes: {}".format(len(env_variables.all_routes)))
        # print("the count of vehicles: {}".format(traci.vehicle.getIDCount()))
        # print(traci.route.getIDList())
        print("in step {} the count veh is".format(step))
        print(traci.vehicle.getIDCount())
    if step == 0:

        # prepar_route()
        print('the vehicle types are: ')
        print(traci.vehicletype.getIDList())
        print(env_variables.outlets)
    # Returns a list of all objects in the network.
    step += 1
traci.close()
