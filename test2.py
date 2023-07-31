import pickle
from collections import deque

import numpy as np
from matplotlib import pyplot as plt

filename  = "C://Users//Windows dunya//Downloads//action_masking_phase1_period3_occ_wasting_req//qvalue_decentralized_for_plotting//qvalue2.pkl"
# filename2 = "C://Users//Windows dunya//Downloads//action_masking_occ_wasting_req_period3_phase2//qvalue_decentralized_for_plotting//qvalue1.pkl"
# filename3 = "C://Users//Windows dunya//Downloads//action_masking_occ_wasting_req_period3_phase3//qvalue_decentralized_for_plotting//qvalue1.pkl"
# filename4 = "C://Users//Windows dunya//Downloads//action_masking_occ_wasting_req_period3_phase4//qvalue_decentralized_for_plotting//qvalue1.pkl"
# filename5 = "C://Users//Windows dunya//Downloads//decentralize_action_masking_occupancy_wasting_requests_period3_test2_on_3G_weights//utility_decentralized//utility1.pkl"
# # filename6 = "C://Users//Windows dunya//Downloads//decentralize_action_masking_occupancy_wasting_requests_period3_phase1//utility_decentralized//utility2.pkl"

# filename5 = "C://Users//Windows dunya//Downloads//decentralize_action_masking_last_scenario_phase5//utility_decentralized//utility2.pkl"
#
deque = []
with open(filename, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            deque.append(loaded_value)
    except EOFError:
        pass

# with open(filename2, 'rb') as file:
#     try:
#         n = 8
#         l=[]
#         while True:
#             loaded_value = pickle.load(file)
#             deque.append(loaded_value)
#     except EOFError:
#         pass
# # #
# with open(filename3, 'rb') as file:
#     try:
#         while True:
#             loaded_value = pickle.load(file)
#             deque.append(loaded_value)
#     except EOFError:
#         pass
# # # # #
# with open(filename4, 'rb') as file:
#     try:
#         while True:
#             loaded_value = pickle.load(file)
#             deque.append(loaded_value)
#     except EOFError:
#         pass
#
# with open(filename5, 'rb') as file:
#     try:
#         while True:
#             loaded_value = pickle.load(file)
#             deque.append(loaded_value)
#     except EOFError:
#         pass
#
#
# with open(filename6, 'rb') as file:
#     try:
#         while True:
#             loaded_value = pickle.load(file)
#             deque.append(loaded_value)
#     except EOFError:
#         pass


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
print(len(deque))
x_values = [i for i in range(len(result))]  # Adjust x-axis values
# x = [i * 320 for i in range(len(deque))]

# Plot the original data and the rolling average
# plt.plot(np.arange(len(deque)), deque, label='Original Data')
plt.plot(x_values, result, label=f'4G_qvalue')
plt.xlabel('episode')
plt.ylabel('4G_qvalue')
plt.legend()
plt.title(f'Rolling Average Plot (window={window_size})')
plt.grid(True)
plt.savefig('4G_qvalue.svg', format='svg')

plt.show()
