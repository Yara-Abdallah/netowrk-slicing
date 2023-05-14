import os

import traci

# Get the current working directory
current_dir = os.getcwd()

network_path = current_dir + '\\Environment\\Area2\\map.sumocfg'
random_routes_path = current_dir + '\\Environment\\Area2\\map.rou.xml'

types_outlets = ['3G', '4G', '5G','wifi']

outlet_radius = [1000] * 39

outlets = {
    '3G': [],
    '4G': [],
    '5G': [],
    'wifi':[]

}
all_routes = []

number_cars_mean_std={
    'mean':50,
    'std':5
}

threashold_number_veh = 20

default_types_vehicles = [
    'DEFAULT_BIKETYPE',
    'DEFAULT_CONTAINERTYPE',
    'DEFAULT_PEDTYPE',
    'DEFAULT_TAXITYPE',
    'DEFAULT_VEHTYPE']

vehicles = {}
TIME = 1000
#10000 * 7


requests = []
period1 = 2000
period2 = 4000
period3 = 6000
period4 = 8000
period5 = 10000

decentralized_replay_buffer = 30
centralized_replay_buffer = 10 * 30
def get_position_vehicle(id_):
    try:
        p = round(traci.vehicle.getPosition(id_),4)
        return p
    except:
        return "id_vehicle is not found in env in this moment"
