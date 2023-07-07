import pickle
import shutil
source_folder = 'H://work_projects//network_slicing//ns//results'
destination_folder = 'H://work_projects//network_slicing//ns//prev_results'
deque = []
deque_decentralize0=[]
deque_decentralize1=[]
deque_decentralize2=[]



filename = "C://Users//Windows dunya//Downloads//prev_results-20230706T103052Z-001//prev_results//qvalue_centralized_for_plotting//qvalue.pkl"
filename2= "C://Users//Windows dunya//Downloads//results2_tanh-20230707T111436Z-001//results2_tanh//qvalue_centralized_for_plotting//qvalue.pkl"

filename_decentralize0 = "C://Users//Windows dunya//Downloads//prev_results-20230706T103052Z-001//prev_results//qvalue_decentralized_for_plotting//qvalue0.pkl"
filename2_decentralize0= "C://Users//Windows dunya//Downloads//results2_tanh-20230707T111436Z-001//results2_tanh//qvalue_decentralized_for_plotting//qvalue0.pkl"

filename_decentralize1 = "C://Users//Windows dunya//Downloads//prev_results-20230706T103052Z-001//prev_results//qvalue_decentralized_for_plotting//qvalue1.pkl"
filename2_decentralize1= "C://Users//Windows dunya//Downloads//results2_tanh-20230707T111436Z-001//results2_tanh//qvalue_decentralized_for_plotting//qvalue1.pkl"

filename_decentralize2 = "C://Users//Windows dunya//Downloads//prev_results-20230706T103052Z-001//prev_results//qvalue_decentralized_for_plotting//qvalue2.pkl"
filename2_decentralize2= "C://Users//Windows dunya//Downloads//results2_tanh-20230707T111436Z-001//results2_tanh//qvalue_decentralized_for_plotting//qvalue2.pkl"


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


plt.plot(deque_decentralize2)

# Add labels and title
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Plot of deque values')
plt.savefig('plot_d2.svg', format='svg')
# Display the plot
plt.show()