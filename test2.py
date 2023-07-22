import pickle
from collections import deque
filename  = "C://Users//Windows dunya//Downloads//dec_ac_ma//results//action_decentralized//available_capacity0.pkl"
deque = []
with open(filename, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            deque.append(loaded_value)
    except EOFError:
        pass

for i in deque:
    print(i)
    print("\n")
print("Folder contents copied successfully.")
