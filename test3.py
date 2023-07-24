import pickle

import pandas as pd

available_cap = "H://work_projects//network_slicing//ns//dec_action_masking_phase_replace_towers//available_capacity_decentralized//available_capacity2.pkl"
reward ="H://work_projects//network_slicing//ns//dec_action_masking_phase_replace_towers//reward_decentralized//reward2.pkl"
action ="H://work_projects//network_slicing//ns//dec_action_masking_phase_replace_towers//action_decentralized//action2.pkl"
utility ="H://work_projects//network_slicing//ns//dec_action_masking_phase_replace_towers//utility_decentralized//utility2.pkl"
requested = "H://work_projects//network_slicing//ns//dec_action_masking_phase_replace_towers//requested_decentralized//requested2.pkl"
ensured = "H://work_projects//network_slicing//ns//dec_action_masking_phase_replace_towers//ensured_decentralized//ensured2.pkl"
supported = "H://work_projects//network_slicing//ns//dec_action_masking_phase_replace_towers//supported_service_decentralized//supported_services2.pkl"
power = "H://work_projects//network_slicing//ns//dec_action_masking_phase_replace_towers//sum_power_allocation//sum_power_allocation2.pkl"
av_cap = []
rew =[]
act=[]
uti =[]
req =[]
ens=[]
sup = []
pow_=[]
# with open(filename, 'rb') as file:
#     try:
#         while True:
#             loaded_value = pickle.load(file)
#             deque.append(loaded_value)
#     except EOFError:
#         pass

with open(available_cap, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            av_cap.append(loaded_value)
    except EOFError:
        pass

with open(reward, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            rew.append(loaded_value)
    except EOFError:
        pass

with open(action, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            act.append(loaded_value)
    except EOFError:
        pass
with open(utility, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            uti.append(loaded_value)
    except EOFError:
        pass

with open(requested, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            req.append(loaded_value)
    except EOFError:
        pass
with open(ensured, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            ens.append(loaded_value)
    except EOFError:
        pass
with open(supported, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            sup.append(loaded_value)
    except EOFError:
        pass

with open(power, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            pow_.append(loaded_value)
    except EOFError:
        pass
# import csv
# newfilePath = "H://work_projects//network_slicing//ns//dec_action_masking_phase_replace_towers//results2.csv"
#
# rows = zip(av_cap, uti, action, rew)
# df = pd.DataFrame(list(zip(*[av_cap, uti, action,rew]))).add_prefix('Col')
#
# df.to_csv(newfilePath, index=False)
#
# print(df)

# import csv
# dic = {av_cap, uti, action,rew} #dictionary
# csv = open('result.csv', "w")
# for key in dic.keys():
#     row ="\n"+ str(key) + "," + str(dic[key])
#     csv.write(row)
#
import pandas as pd
columns = {}

columns['available_cap'] = av_cap
columns['utility'] = uti
columns['action'] = act
columns['reward'] = rew
columns['requested'] = req
columns['ensured'] = ens
columns['supported'] = sup
columns['power'] = pow_
data = list(zip(columns['available_cap'],columns['utility'],columns['action'],columns['reward'],columns['requested'],columns['ensured'],columns['supported'],columns['power']))

df = pd.DataFrame(data = data)

df.to_csv('4G.csv', index=False, header=False)