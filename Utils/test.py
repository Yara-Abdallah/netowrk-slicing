import pickle

# create the dictionary of dictionaries
dict_of_dicts = {
    'dict1': {'value1': 10},
    'dict2': {'value1': 20, 'value2': 30},
    'dict3': {'value1': 40, 'value2': 50, 'value3': 60}
}

with open('H://data//data.pkl', 'wb') as f:
    pickle.dump(dict_of_dicts, f)
# load the dictionary from the pickle file
with open('H://data//data.pkl', 'rb') as f:
    dict_of_dicts = pickle.load(f)


print(f'Time step: {len(dict_of_dicts)}')
for i, d in enumerate(dict_of_dicts):
    print(f'Dictionary {i}: {d}')

#
# # set the time step count to 0
# time_step = 0
#
# # list to hold dictionaries for every 20 time steps
# dict_list = []
#
# # main loop
# while True:
#     # increment the time step count
#     time_step += 1
#
#     # add new values to the inner dictionaries of dict_of_dicts
#     for inner_dict in dict_of_dicts.values():
#         print("1")
#         inner_dict[f'value{time_step}'] = time_step
#
#     # every 20 time steps, clear the inner dictionaries of dict_of_dicts,
#     # append a new dictionary to dict_list with the updated values of the
#     # inner dictionaries, and write the list to the pickle file
#     if time_step % 20 == 0:
#         old_values = {}
#         new_dict = {}
#         for key, inner_dict in dict_of_dicts.items():
#             print("2")
#             old_values[key] = inner_dict.copy()
#             new_dict[key] = inner_dict
#             inner_dict.clear()
#         dict_list.append(new_dict)
#         with open('H://data//data.pkl', 'wb') as f:
#             pickle.dump(dict_list, f)
#
#     if  time_step == 200:
#         break
#
#     # do other things here...
#
#
# # Open the pickle file for reading
# with open('H://data//data.pkl', 'rb') as f:
#     dict_list = pickle.load(f)
#
# # Print the values in dict_list
# print(f'Time step: {len(dict_list)}')
# for i, d in enumerate(dict_list):
#     print(f'Dictionary {i}: {d}')