network_path = 'H:\\work_projects\\network_slicing\\ns\\Environment\\Area\\map.sumocfg'
random_routes_path = 'H:\\work_projects\\network_slicing\\ns\\Environment\\Area\\map.rou.xml'

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

# position_of_oultets = []
vehicles_id_pos = []
TIME = 100
