import os
import sys


results_dir = os.path.join(sys.path[0], 'results3_exploit_decentralize')
path6 = os.path.join(results_dir, 'centralized_weights')
path7 = os.path.join(results_dir, 'decentralized_weights')
path_memory_centralize = os.path.join(results_dir,'centralize_memory')
path_memory_decentralize = os.path.join(results_dir,'decentralize_memory')
# prev_results_dir = "//content//drive//MyDrive//network_slicing//prev_results//"
utility_requested_ensured_path = os.path.join(results_dir, 'utility_requested_ensured')
reward_decentralized_path = os.path.join(results_dir, 'reward_decentralized')
reward_centralized_path = os.path.join(results_dir, 'reward_centralized')
qvalue_decentralized_path = os.path.join(results_dir, 'qvalue_decentralized')
qvalue_centralized_path = os.path.join(results_dir, 'qvalue_centralized')
# centralize_qvalue_path = os.path.join(prev_results_dir, 'qvalue_centralized_for_plotting')
# decentralize_qvalue_path = os.path.join(prev_results_dir, 'qvalue_decentralized_for_plotting')
prev_results_3tanh_dir = os.path.join(sys.path[0],"results3_tanh//results3_tanh//")
# results1_explor_decentralize = "//content//drive//MyDrive//network_slicing//results2_explor_decentralize//"

prev_centralize_weights_path = os.path.join(prev_results_3tanh_dir,"centralized_weights//")
# prev_decentralize_weights_path = os.path.join(results1_explor_decentralize,"decentralized_weights//")
# prev_centralize_memory_path = os.path.join(prev_results_4tanh_dir,"centralize_memory//")
# prev_decentralize_memory_path = os.path.join(results1_explor_decentralize,"decentralize_memory//")
centralize_qvalue_path = os.path.join(results_dir,"qvalue_centralized_for_plotting//")
decentralize_qvalue_path = os.path.join(results_dir,"qvalue_decentralized_for_plotting//")



os.makedirs(utility_requested_ensured_path, exist_ok=True)
os.makedirs(reward_decentralized_path, exist_ok=True)
os.makedirs(reward_centralized_path, exist_ok=True)
os.makedirs(qvalue_decentralized_path, exist_ok=True)
os.makedirs(qvalue_centralized_path, exist_ok=True)
os.makedirs(path6, exist_ok=True)
os.makedirs(path7, exist_ok=True)
os.makedirs(path_memory_centralize, exist_ok=True)
os.makedirs(path_memory_decentralize, exist_ok=True)
os.makedirs(centralize_qvalue_path, exist_ok=True)
os.makedirs(decentralize_qvalue_path, exist_ok=True)