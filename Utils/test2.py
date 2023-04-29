
# buffer_data = np.random.randint(0, 100, (5, 3))
# fig, ax = plt.subplots()
# sns.heatmap(buffer_data, cmap="RdYlGn_r", ax=ax, vmin=0, vmax=100)
# ax.set_title("Buffer Occupancy")
#
# # Create the color bar
# cbar = ax.collections[0].colorbar
# sm = plt.cm.ScalarMappable(cmap="RdYlGn_r")
# sm.set_array([])
#
# outlet_occupancy = np.zeros([5, 3])
#
# # from Utils.FileLoggingInfo import Logger
#
#
# buffer_data_utility = np.random.randint(0, 10, (5, 3))
# fig2, ax2 = plt.subplots()
# sns.heatmap(buffer_data, cmap="RdYlGn_r", ax=ax2, vmin=0, vmax=10)
# ax2.set_title("Buffer utility")
#
# # Create the color bar
# cbar2 = ax2.collections[0].colorbar
# sm = plt.cm.ScalarMappable(cmap="RdYlGn_r")
# sm.set_array([])
#
# outlet_utility = np.zeros([5, 3])


# def buffer_data_occupancy_generator(self, outlet_occupancy):
#     while True:
#         for i in range(5):
#             for j in range(3):
#                 outlet_occupancy[i][j] = outlet_occupancy[i][j]
#         yield outlet_occupancy
#
# def update_outlet_occupancy(self, outlet_occupancy):
#     # Update the buffer occupancy data
#     buffer_data = next(self.buffer_data_occupancy_generator(outlet_occupancy))
#     # Update the heatmap
#     sns.heatmap(buffer_data, annot=True, cmap="RdYlGn_r", ax=ax, cbar=False)
#     ax.set_title(f"Buffer Occupancy )")
#
#     for t in ax.texts:
#         t.remove()
#     for i in range(buffer_data.shape[0]):
#         for j in range(buffer_data.shape[1]):
#             text = str(buffer_data[i][j])
#             ax.text(j + 0.5, i + 0.5, text, ha="center", va="center")
#     plt.draw()
#     plt.pause(1)
#
# def buffer_data_utility_generator(self, outlet_utility):
#     while True:
#         for i in range(5):
#             for j in range(3):
#                 outlet_utility[i][j] = outlet_utility[i][j]
#         yield outlet_utility
#
# def update_outlet_utility(self, outlet_utility):
#     # Update the buffer occupancy data
#     buffer_data_utility = next(self.buffer_data_utility_generator(outlet_utility))
#     # Update the heatmap
#     sns.heatmap(buffer_data_utility, annot=True, cmap="RdYlGn_r", ax=ax2, cbar=False)
#     ax2.set_title(f"Buffer utility ")
#
#     for t in ax2.texts:
#         t.remove()
#     for i in range(buffer_data_utility.shape[0]):
#         for j in range(buffer_data_utility.shape[1]):
#             text = str(buffer_data_utility[i][j])
#             ax2.text(j + 0.5, i + 0.5, text, ha="center", va="center")
#     plt.draw()
#     plt.pause(1)