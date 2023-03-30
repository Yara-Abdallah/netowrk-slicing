import os

import traci

# Get the current working directory
current_dir = os.getcwd()

network_path = current_dir + '\\Environment\\Area\\map.sumocfg'
random_routes_path = current_dir + '\\Environment\\Area\\map.rou.xml'

types_outlets = ['3G', '4G', '5G', 'Wifi']

outlet_radius = [1000] * 39

outlets = {
    '3G': [],
    '4G': [],
    '5G': [],
    'wifi': [],
}
all_routes = []

default_types_vehicles = [
    'DEFAULT_BIKETYPE',
    'DEFAULT_CONTAINERTYPE',
    'DEFAULT_PEDTYPE',
    'DEFAULT_TAXITYPE',
    'DEFAULT_VEHTYPE']

vehicles = {}
TIME = 200


def get_position_vehicle(id_):
    try:
        return traci.vehicle.getPosition(id_)
    except:
        return "id_vehicle is not found in env in this moment"
