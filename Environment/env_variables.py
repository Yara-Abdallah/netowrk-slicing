import os

import traci
from pathlib import Path

# Get the current working directory
# current_dir = os.getcwd()

# network_path = current_dir + '\\Environment\\Area2\\map.sumocfg'
# random_routes_path = current_dir + '\\Environment\\Area2\\map.rou.xml'


# network_path = current_dir + '\\Environment\\Network\\cross intersection.sumocfg'
# random_routes_path = current_dir + '\\Environment\\Network\\cross_intersection.rou.xml'
#

current_dir = Path(__file__).resolve().parent
network_path = os.path.join(current_dir, "Network", "cross intersection.sumocfg")
random_routes_path = os.path.join(current_dir, "Network", "cross_intersection.rou.xml")

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

#10000 * 7
Threshold_of_utility = 0.1
Threshold_of_utility_acc = 0.5

requests = []
period1 = 256
period2 = 512
period3 = 786
period4 = 1024
period5 = 1280

ENTERTAINMENT_RATIO = 0
SAFETY_RATIO = 0
AUTONOMOUS_RATIO = 0

number_of_days = 7
episodes = 5 * number_of_days
TIME = 1280 * number_of_days
day_time = 1280

decentralized_replay_buffer = 30
centralized_replay_buffer = 32
def get_position_vehicle(id_):
    try:
        p = round(traci.vehicle.getPosition(id_),4)
        return p
    except:
        return "id_vehicle is not found in env in this moment"
