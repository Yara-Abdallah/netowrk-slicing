import matplotlib.pyplot as plt

num_episodes = 5
num_steps = 256
accumulated_rewards = []  # List to store accumulated rewards

# Generate example accumulated rewards (replace with your actual accumulated reward values)
for episode in range(num_episodes):
    accumulated_reward = sum([episode * num_steps + step for step in range(num_steps)])
    accumulated_rewards.append(accumulated_reward)

# Calculate average reward across episodes
average_reward = sum(accumulated_rewards) / num_episodes

# Plotting the average reward across episodes
plt.plot(range(num_episodes), [average_reward] * num_episodes)
plt.xlabel('Episode')
plt.ylabel('Average Reward')
plt.title('Average Reward across Episodes')
plt.show()
