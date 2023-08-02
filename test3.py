import pickle

import pandas as pd

reward ="C://Users//Windows dunya//Downloads//result_occ_with_derivation//reward_decentralized//reward1.pkl"
action ="C://Users//Windows dunya//Downloads//result_occ_with_derivation//action_decentralized//action1.pkl"
utility ="C://Users//Windows dunya//Downloads//result_occ_with_derivation//utility_decentralized//utility1.pkl"
requested = "C://Users//Windows dunya//Downloads//result_occ_with_derivation//requested_decentralized//requested1.pkl"
ensured = "C://Users//Windows dunya//Downloads//result_occ_with_derivation//ensured_decentralized//ensured1.pkl"
supported = "C://Users//Windows dunya//Downloads//result_occ_with_derivation//supported_service_decentralized//supported_services1.pkl"
occu = "C://Users//Windows dunya//Downloads//result_occ_with_derivation//ratio_of_occupancy_decentralized//ratio_of_occupancy1.pkl"
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

df.to_csv('3G_testing_derivation4.csv', index=False, header=False)