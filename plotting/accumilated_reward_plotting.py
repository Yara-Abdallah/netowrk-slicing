


filename1  = "C://Users//Windows dunya//Downloads//action_masking_occ_wasting_req_period3_phase1//reward_accumilated_decentralize//accu_reward0.pkl"
# filename2 = "C://Users//Windows dunya//Downloads//action_masking_occ_wasting_req_period3_phase2//reward_accumilated_decentralize//accu_reward0.pkl"
# filename3 = "C://Users//Windows dunya//Downloads//action_masking_occ_wasting_req_period3_phase3//reward_accumilated_decentralize//accu_reward0.pkl"
# filename4 = "C://Users//Windows dunya//Downloads//action_masking_occ_wasting_req_period3_phase4//reward_accumilated_decentralize//accu_reward0.pkl"


filesname=[filename1,filename2,filename3,filename4]
dequeu = plotting(filesname,dequeu)

# Example usage:
window_size = 1
result = rolling_average(deque, window_size)
x_values = [i for i in range(len(result))]  # Adjust x-axis values

plt.plot(x_values, result, label=f'wifi_acc_reward')
plt.xlabel('episode')
plt.ylabel('wifi_acc_reward')
plt.legend()
plt.title(f'Rolling Average Plot (window={window_size})')
plt.grid(True)
plt.savefig('wifi_acc_reward.svg', format='svg')

plt.show()
