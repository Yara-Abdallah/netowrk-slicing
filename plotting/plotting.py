import pickle
import numpy as np
from matplotlib import pyplot as plt
import os
import sys

paths = ["ratio_of_occupancy_decentralized//ratio_of_occupancy","reward_accumilated_decentralize//accu_reward","qvalue_decentralized_for_plotting//qvalue","utility_decentralized//utility"]
phases_number  = 1
def paths_reading_from(outlet_number):
    filesname = []
    for phase_number in range(phases_number):
        filesname.append(f"C://Users//Windows dunya//Downloads//result_occ_with_derivation//ratio_of_occupancy_decentralized//ratio_of_occupancy{1}.pkl")
    return filesname

results_dir = os.path.join(sys.path[0],
                           'action_masking_derivation_occ_serving_req_results')

accu_reward = os.path.join(results_dir, 'accu_reward')
qvalue = os.path.join(results_dir, 'qvalue')
serving_ratio = os.path.join(results_dir, 'serving_ratio')
occupancy = os.path.join(results_dir, 'occupancy')
os.makedirs(accu_reward, exist_ok=True)
os.makedirs(qvalue, exist_ok=True)
os.makedirs(serving_ratio, exist_ok=True)
os.makedirs(occupancy, exist_ok=True)

def read_data(filesname,queue):
    for i in range(phases_number):
        with open(filesname[i], 'rb') as file:
            try:
                while True:
                    loaded_value = pickle.load(file)
                    queue.append(loaded_value)
            except EOFError:
                pass
    return queue

def rolling_average(data, window_size):
    # Convert the data to a NumPy array with float type
    data_array = np.array(data, dtype=np.float64)

    # Pad the data with NaN values at the beginning to maintain the length of the output
    padded_data = np.pad(data_array, (window_size-1, 0), mode='constant', constant_values=np.nan)

    # Calculate the rolling average using convolution with a window of ones
    weights = np.ones(window_size) / window_size
    rolling_avg = np.convolve(padded_data, weights, mode='valid')

    return rolling_avg
def plotting(x_values,yvalues,window_size,towername,directory_path,yvalue_name):
    plt.plot(x_values, yvalues, label=f'{towername} {yvalue_name}')
    plt.xlabel('episode')
    plt.ylabel(f'{towername} {yvalue_name}')
    plt.legend()
    plt.title(f'Rolling Average Plot (window={window_size})')
    plt.grid(True)
    plt.savefig(os.path.join(directory_path,f'{towername} {yvalue_name}.svg'), format='svg')
    plt.show()
