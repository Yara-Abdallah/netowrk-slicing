import pickle
import shutil
source_folder = 'H://work_projects//network_slicing//ns//results'
destination_folder = 'H://work_projects//network_slicing//ns//prev_results'
deque = []
deque_decentralize0=[]
deque_decentralize1=[]
deque_decentralize2=[]



filename = "C://Users//Windows dunya//Downloads//prev_results-20230706T103052Z-001//prev_results//qvalue_centralized_for_plotting//qvalue.pkl"
filename2 = "C://Users//Windows dunya//Downloads//results2_tanh-20230707T111436Z-001//results2_tanh//qvalue_centralized_for_plotting//qvalue.pkl"
filename3 ="C://Users//Windows dunya//Downloads//results3_tanh-20230707T142928Z-001//results3_tanh//qvalue_centralized_for_plotting//qvalue.pkl"

filename_decentralize0 = "C://Users//Windows dunya//Downloads//network_slicing-20230709T055434Z-001//network_slicing//results1_explor_decentralize//qvalue_decentralized_for_plotting//qvalue0.pkl"
filename2_decentralize0 = "C://Users//Windows dunya//Downloads//network_slicing-20230709T055434Z-001//network_slicing//results2_explor_decentralize//qvalue_decentralized_for_plotting//qvalue0.pkl"
filename3_decentralize0 = "C://Users//Windows dunya//Downloads//results3_explor_decentralize-20230708T172948Z-001//results3_explor_decentralize//qvalue_decentralized_for_plotting//qvalue0.pkl"


filename_decentralize1 = "C://Users//Windows dunya//Downloads//network_slicing-20230709T055434Z-001//network_slicing//results1_explor_decentralize//qvalue_decentralized_for_plotting//qvalue1.pkl"
filename2_decentralize1 = "C://Users//Windows dunya//Downloads//network_slicing-20230709T055434Z-001//network_slicing//results2_explor_decentralize//qvalue_decentralized_for_plotting//qvalue1.pkl"
filename3_decentralize1 = "C://Users//Windows dunya//Downloads//results3_explor_decentralize-20230708T172948Z-001//results3_explor_decentralize//qvalue_decentralized_for_plotting//qvalue1.pkl"


filename_decentralize2 = "C://Users//Windows dunya//Downloads//network_slicing-20230709T055434Z-001//network_slicing//results1_explor_decentralize//qvalue_decentralized_for_plotting//qvalue2.pkl"
filename2_decentralize2 = "C://Users//Windows dunya//Downloads//network_slicing-20230709T055434Z-001//network_slicing//results2_explor_decentralize//qvalue_decentralized_for_plotting//qvalue2.pkl"
filename3_decentralize2 = "C://Users//Windows dunya//Downloads//results3_explor_decentralize-20230708T172948Z-001//results3_explor_decentralize//qvalue_decentralized_for_plotting//qvalue2.pkl"


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
with open(filename3, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            deque.append(loaded_value)
    except EOFError:
        pass

with open(filename_decentralize2, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            deque_decentralize2.append(loaded_value)
    except EOFError:
        pass
with open(filename2_decentralize2, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            deque_decentralize2.append(loaded_value)
    except EOFError:
        pass

# with open(filename3_decentralize0, 'rb') as file:
#     try:
#         while True:
#             loaded_value = pickle.load(file)
#             deque_decentralize0.append(loaded_value)
#     except EOFError:
#         pass
# Copy the contents of the source folder to the destination folder
# shutil.copytree(source_folder, destination_folder)

for i in deque :
    print(i)
    print("\n")
print("Folder contents copied successfully.")

import matplotlib.pyplot as plt

# Create a deque with 35 values

# Plot the values
# plt.plot(deque)
#
# # Add labels and title
# plt.xlabel('Index')
# plt.ylabel('Value')
# plt.title('Plot of deque values')
# plt.savefig('plot.svg', format='svg')
# # Display the plot
# plt.show()


x = [i * 320 for i in range(len(deque))]
print(len(x))
# Generate y-axis values (every 320th value)
# y = [deque[i] for i in range(len(deque)) if i % 320 == 0]
# print(len(y))
# Plot the values
plt.plot(x, deque)

# Add labels and title
plt.xlabel('Time steps')
plt.ylabel('Q-value')
plt.title('Average Q-value each episode : { 320 Time step }')
plt.savefig('centralize.svg', format='svg')

# Display the plot
plt.show()



# plt.plot(deque)
#
# Add labels and title
# plt.xlabel('Index')
# plt.ylabel('Value')
# plt.title('Plot of deque values')
# plt.savefig('plot_cent.svg', format='svg')
# Display the plot
# plt.show()


import numpy as np
import matplotlib.pyplot as plt


def rolling_average(data, window_size):
    # Convert the data to a NumPy array with float type
    data_array = np.array(data, dtype=np.float64)

    # Pad the data with NaN values at the beginning to maintain the length of the output
    padded_data = np.pad(data_array, (window_size - 1, 0), mode='constant', constant_values=np.nan)

    # Calculate the rolling average using convolution with a window of ones
    weights = np.ones(window_size) / window_size
    rolling_avg = np.convolve(padded_data, weights, mode='valid')

    return rolling_avg


# Example usage:
data = [10, 5, 7, 9, 8, 12, 15, 20, 18, 16]
window_size = 3

result = rolling_average(data, window_size)
x_values = [i for i in range(len(result))]  # Adjust x-axis values
# x = [i * 320 for i in range(len(deque))]

# Plot the original data and the rolling average
plt.plot(np.arange(len(data)), data, label='Original Data', marker='o')
plt.plot(x_values, result, label=f'Rolling Average (window={window_size})', marker='o')
plt.xlabel('Data Points')
plt.ylabel('Values')
plt.legend()
plt.title('Rolling Average Plot')
plt.grid(True)
plt.show()