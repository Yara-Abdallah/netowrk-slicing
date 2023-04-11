import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create the buffer occupancy data
buffer_data = np.random.randint(0, 10, (5, 4))

# Initialize the plot
fig, ax = plt.subplots()
sns.heatmap(buffer_data, cmap="RdYlGn_r", ax=ax, vmin=0, vmax=10)
ax.set_title("Buffer Occupancy")

# Create the color bar
cbar = ax.collections[0].colorbar
sm = plt.cm.ScalarMappable(cmap="RdYlGn_r")
sm.set_array([])
arr = [["val"] * 4] * 5
for i in range(buffer_data.shape[0]):
    for j in range(buffer_data.shape[1]):
        text = str(arr[i][j])
        ax.text(j + 0.5, i + 0.5, text, ha="center", va="center")

# Define the update function
def update(step):
    # Update the buffer occupancy data
    buffer_data = np.random.randint(0, 10, (5, 4))

    # Update the heatmap
    sns.heatmap(buffer_data, cmap="RdYlGn_r", ax=ax, cbar=False)
    ax.set_title(f"Buffer Occupancy (Step: {step})")

    for t in ax.texts:
        t.remove()
    for i in range(buffer_data.shape[0]):
        for j in range(buffer_data.shape[1]):
            text = str(buffer_data[i][j])
            ax.text(j + 0.5, i + 0.5, text, ha="center", va="center")

    return [ax]


# Animate the plot
ani = FuncAnimation(fig, update, frames=200, interval=0)

plt.show()
