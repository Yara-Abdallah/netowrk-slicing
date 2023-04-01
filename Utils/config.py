from enum import Enum

import numpy as np

# from Outlet.Cellular.FactoryCellular import FactoryCellular

SERVICES_TYPES = {
    "ENTERTAINMENT": {
        "REALTIME": np.arange(start=5, stop=9 + 1),
        "BANDWIDTH": np.arange(start=8, stop=10 + 1),
        "CRITICAL": np.arange(start=1, stop=2 + 1),
    },
    "SAFETY": {
        "REALTIME": np.arange(start=9, stop=10 + 1),
        "BANDWIDTH": np.arange(start=1, stop=3 + 1),
        "CRITICAL": np.arange(start=9, stop=10 + 1),
    },
    "AUTONOMOUS": {
        "REALTIME": np.arange(start=9, stop=10 + 1),
        "BANDWIDTH": np.arange(start=7, stop=8 + 1),
        "CRITICAL": np.arange(start=8, stop=10 + 1),
    },
}

REALTIME_BANDWIDTH = {
    "WIFI": list(range(1, 3)),
    "3G": list(range(3, 5)),
    "4G": list(range(5, 7)),
    "5G": list(range(7, 9)),
    "SATELLITE": list(range(9, 10)),
}

CRITICAL_BANDWIDTH = {}

outlet_types = {
    "3G": {
        "NUM_ANTENNAS": [1, 2],
        "CHANNEL_BANDWIDTH": np.arange(1.25, 5, 0.25),
        "CODING_RATE": [1 / 2, 1 / 3],
        "MODULATION_ORDER": [4],
        "AVERAGE_SYMBOLS_PER_SLOT": np.arange(12, 20, 1),
        "NUM_SLOTS_PER_FRAME": [15],
        "NUM_FRAMES_PER_SECOND": [10],
    },
    "4G": {
        "NUM_ANTENNAS": [3, 4],
        "CHANNEL_BANDWIDTH": np.arange(1.5, 20, 0.5),
        "CODING_RATE": [1 / 2, 2 / 3, 3 / 4],
        "MODULATION_ORDER": [4, 6, 8],
        "AVERAGE_SYMBOLS_PER_SLOT": [12, 13, 14],
        "NUM_SLOTS_PER_FRAME": [10],
        "NUM_FRAMES_PER_SECOND": [20],
    },
    "5G": {
        "NUM_ANTENNAS": [1],
        "CHANNEL_BANDWIDTH": np.arange(100, 200, 5),
        "CODING_RATE": [1 / 2, 2 / 3, 3 / 4, 4 / 5, 5 / 6],
        "MODULATION_ORDER": [4, 6, 8, 10],
        "AVERAGE_SYMBOLS_PER_SLOT": [12, 13, 14],
        "NUM_SLOTS_PER_FRAME": [10],
        "NUM_FRAMES_PER_SECOND": [60],
    },
}



# print(BuildMaxCapacity(outlet_types['FOUR_G']).max_capacity)
def relation_between_criticality_and_bandwidth(criticality, total_bandwidth):
    total_bandwidth = total_bandwidth * 10
    change_in_bandwidth = criticality * total_bandwidth * 0.03
    print(f"change amount in bandwidth (capacity) is : {change_in_bandwidth} MBps")
    total_bandwidth = total_bandwidth + change_in_bandwidth
    print(f"new bandwidth (capacity) is : {total_bandwidth} MBps")
    return total_bandwidth



# relation_between_criticality_and_bandwidth(
#     SERVICES_TYPES["ENTERTAINMENT"]["CRITICAL"],
#     real_total_capacity
# )

# factory = FactoryCellular(1, 1, [1, 1, 0], [10, 15], 10000, real_total_capacity,
#                           [10, 10, 10])
#
# outlet = factory.produce_cellular_outlet("5G")
# print("outlet object total power : ", outlet.power)
