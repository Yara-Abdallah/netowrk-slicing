
import numpy as np
import matplotlib.pyplot as plt

# Create the plot
fig, ax = plt.subplots()
ax.set_xlabel('Time')
ax.set_ylabel('Utility')

# Create 15 lines and add them to the plot
lines = []
for i in range(15):
    line, = ax.plot([], [], label=f"Utility {i}")
    lines.append(line)

ax.legend()

# Set the time at which to save the snapshot
snapshot_time = 5
num_iterations = 200
time = 0
prev = 0

# Start the training loop
for i in range(num_iterations):
    # Perform one iteration of training
    utilities = np.random.randint(1, 100, 15)
    time = time + 1
    print("here")

    # Update the data for each line
    for j, line in enumerate(lines):
        x_data, y_data = line.get_data()
        x_data = np.append(x_data, time)
        y_data = np.append(y_data, utilities[j])
        line.set_data(x_data, y_data)

    # Update the plot
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()

    # Save a snapshot of the figure after a specific time
    if time - prev == snapshot_time:
        prev = time
        v = f'I://Documents//snapshot{time}'
        print(v)
        fig.savefig(v + '.png')
        plt.pause(0.001)

    # Update the plot every 5 time steps
    if time % 10 == 0:
        plt.pause(0.001)

plt.show()

# Close the plot
plt.close()
