import pickle
from collections import deque

import numpy as np
from matplotlib import pyplot as plt



filename1  = "C://Users//Windows dunya//Downloads//action_masking_occ_wasting_req_period3_phase1//ratio_of_occupancy_decentralized//ratio_of_occupancy0.pkl"
# filename2 = "C://Users//Windows dunya//Downloads//action_masking_occ_wasting_req_period3_phase2//ratio_of_occupancy_decentralized//ratio_of_occupancy0.pkl"
# filename3 = "C://Users//Windows dunya//Downloads//action_masking_occ_wasting_req_period3_phase3//ratio_of_occupancy_decentralized//ratio_of_occupancy0.pkl"
# filename4 = "C://Users//Windows dunya//Downloads//action_masking_occ_wasting_req_period3_phase4//ratio_of_occupancy_decentralized//ratio_of_occupancy0.pkl"

def plotting(filesname,queue):
    for i in range(4):
        with open(filesname[i], 'rb') as file:
            try:
                while True:
                    loaded_value = pickle.load(file)
                    queue.append(loaded_value)
            except EOFError:
                pass
    return queue
filesname=[filename1,filename2,filename3,filename4]
dequeu = plotting(filesname,dequeu)
print(len(dequeu))
for i in dequeu:
    print(i)
    print("\n")
print("Folder contents copied successfully.")


def rolling_average(data, window_size):
    # Convert the data to a NumPy array with float type
    data_array = np.array(data, dtype=np.float64)

    # Pad the data with NaN values at the beginning to maintain the length of the output
    padded_data = np.pad(data_array, (window_size-1, 0), mode='constant', constant_values=np.nan)

    # Calculate the rolling average using convolution with a window of ones
    weights = np.ones(window_size) / window_size
    rolling_avg = np.convolve(padded_data, weights, mode='valid')

    return rolling_avg

# Example usage:
window_size = 100
result = rolling_average(deque, window_size)
print(len(deque))
x_values = [i for i in range(len(result))]  # Adjust x-axis values

plt.plot(x_values, result, label=f'wifi_occupancy_ratio')
plt.xlabel('steps')
plt.ylabel('wifi_occupancy_ratio')
plt.legend()
plt.title(f'Rolling Average Plot (window={window_size})')
plt.grid(True)
plt.savefig('wifi_occupancy_ratio.svg', format='svg')

plt.show()
