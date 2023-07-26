import matplotlib.pyplot as plt
import numpy as np
epsilon=0.30
epsilon_decay=0.00015
min_epsilon = 0.001
e = []
for i in range(8000):
    if epsilon >= min_epsilon:
        epsilon -= epsilon*  epsilon_decay
    e.append(epsilon)
print(epsilon)
x = [ i for i in range(8000)]

# Plot the original data and the rolling average
# plt.plot(x_values, result, label=f'3G_utility (window={window_size})')
plt.plot(range(8000), e)
plt.xlabel('steps')
plt.ylabel('epsilon')
plt.title('epsilon decay policy')

plt.savefig('75-100.svg', format='svg')
plt.show()