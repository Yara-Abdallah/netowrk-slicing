import pickle
from collections import deque

import numpy as np
from matplotlib import pyplot as plt

filename  = "C://Users//Windows dunya//Downloads//decentralize_action_masking_last_scenario//qvalue_decentralized_for_plotting//qvalue0.pkl"
filename2 = "C://Users//Windows dunya//Downloads//decentralize_action_masking_last_scenario_phase2//qvalue_decentralized_for_plotting//qvalue0.pkl"

deque = []
with open(filename, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            deque.append(loaded_value)
    except EOFError:
        pass

with open(filename2, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            deque.append(loaded_value)
    except EOFError:
        pass

print(len(deque))
for i in deque:
    print(i)
    print("\n")
print("Folder contents copied successfully.")

import numpy as np
import matplotlib.pyplot as plt

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
window_size = 1
result = rolling_average(deque, window_size)
# print(result)
# print(len(data))
# print(len(result))
x_values = [i for i in range(len(result))]  # Adjust x-axis values
# x = [i * 320 for i in range(len(deque))]

# Plot the original data and the rolling average
# plt.plot(np.arange(len(deque)), deque, label='Original Data')
plt.plot(x_values, result, label=f'wifi_r_w_10 (window={window_size})')
plt.xlabel('steps')
plt.ylabel('qvalue')
plt.legend()
plt.title('Rolling Average Plot')
plt.grid(True)
plt.savefig('wifi_r_w_10.svg', format='svg')

plt.show()
