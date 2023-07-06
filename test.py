import pickle
import shutil
source_folder = 'H://work_projects//network_slicing//ns//results'
destination_folder = 'H://work_projects//network_slicing//ns//prev_results'
deque = []
filename = "C://Users//Windows dunya//Downloads//results-20230705T110544Z-001//prev_results//qvalue_centralized_for_plotting//qvalue.pkl"
with open(filename, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            deque.append(loaded_value)
    except EOFError:
        pass

# Copy the contents of the source folder to the destination folder
# shutil.copytree(source_folder, destination_folder)
for i in deque :
    print(i)
    print("\n")
print("Folder contents copied successfully.")