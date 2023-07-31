import pickle

import pandas as pd

reward ="C://Users//Windows dunya//Downloads//TEST5//reward_decentralized//reward0.pkl"
action ="C://Users//Windows dunya//Downloads//TEST5//action_decentralized//action0.pkl"
utility ="C://Users//Windows dunya//Downloads//TEST5//utility_decentralized//utility0.pkl"
requested = "C://Users//Windows dunya//Downloads//TEST5//requested_decentralized//requested0.pkl"
ensured = "C://Users//Windows dunya//Downloads//TEST5//ensured_decentralized//ensured0.pkl"
supported = "C://Users//Windows dunya//Downloads//TEST5//supported_service_decentralized//supported_services0.pkl"
occu = "C://Users//Windows dunya//Downloads//TEST5//ratio_of_occupancy_decentralized//ratio_of_occupancy0.pkl"
av_cap = []
rew =[]
act=[]
uti =[]
req =[]
ens=[]
sup = []
pow_=[]
occu_= []
# with open(filename, 'rb') as file:
#     try:
#         while True:
#             loaded_value = pickle.load(file)
#             deque.append(loaded_value)
#     except EOFError:
#         pass

# with open(available_cap, 'rb') as file:
#     try:
#         while True:
#             loaded_value = pickle.load(file)
#             av_cap.append(loaded_value)
#     except EOFError:
#         pass

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

with open(occu, 'rb') as file:
    try:
        while True:
            loaded_value = pickle.load(file)
            occu_.append(loaded_value)
    except EOFError:
        pass

# with open(power, 'rb') as file:
#     try:
#         while True:
#             loaded_value = pickle.load(file)
#             pow_.append(loaded_value)
#     except EOFError:
#         pass
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

print(len(rew))
import pandas as pd
columns = {}

# columns['available_cap'] = av_cap
columns['utility'] = uti
columns['action'] = act
columns['reward'] = rew
columns['requested'] = req
columns['ensured'] = ens
columns['supported'] = sup
columns['occu'] = occu_
# columns['power'] = pow_
data = list(zip(columns['occu'],columns['utility'],columns['action'],columns['reward'],columns['requested'],columns['ensured'],columns['supported']))

df = pd.DataFrame(data = data)

df.to_csv('wifi_TEST.csv', index=False, header=False)