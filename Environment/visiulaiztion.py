import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('agg')





def plotting_Utility_Requested_Ensured():
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(100, 52))
    fig.subplots_adjust(hspace=0.8)
    lines_out_utility = []
    lines_out_requested = []
    lines_out_ensured = []
    j = 0
    for i in range(1):
        row = 0
        line, line1, line2 = 0, 0, 0
        for index in range(3):
            if index == 0:
                color_str = 'b'
            elif index == 1:
                color_str = 'r'
            elif index == 2:
                color_str = 'g'
            line, = axs.flatten()[j].plot([], [], label=f"O{row + index + 1} utility", color=color_str)
            line1, = axs.flatten()[j + 1].plot([], [], label=f"O{row + index + 1} requested", color=color_str)
            line2, = axs.flatten()[j + 2].plot([], [], label=f"O{row + index + 1} ensured", color=color_str)
            lines_out_utility.append(line)
            lines_out_requested.append(line1)
            lines_out_ensured.append(line2)
        j += 3

    return fig,axs,lines_out_utility,lines_out_requested,lines_out_ensured


def plotting_reward_decentralize():
    fig_reward_decentralize, axs_reward_decentralize = plt.subplots(nrows=1, ncols=3, figsize=(100, 120))
    fig_reward_decentralize.subplots_adjust(hspace=0.8)
    lines_out_reward_decentralize = []
    for i, ax in enumerate(axs_reward_decentralize.flatten()):
        line, = ax.plot([], [], label=f"O{i + 1} reward", color='b')
        lines_out_reward_decentralize.append(line)
    return fig_reward_decentralize, axs_reward_decentralize ,lines_out_reward_decentralize
# def plotting_reward_centralize():
#     fig_reward_centralize, axs_reward_centralize = plt.subplots(nrows=1, ncols=1, figsize=(100, 52))
#     fig_reward_centralize.subplots_adjust(hspace=0.8)
#     lines_out_reward_centralize = []
#
#     for i, ax in enumerate(axs_reward_centralize.flatten()):
#         line, = ax.plot([], [], label=f"grid{i + 1} reward", color='b')
#         lines_out_reward_centralize.append(line)
#     return fig_reward_centralize, axs_reward_centralize , lines_out_reward_centralize


def plotting_reward_centralize():
    fig_reward_centralize, ax_reward_centralize = plt.subplots(figsize=(100, 52))

    line, = ax_reward_centralize.plot([], [], label="grid reward", color='b')

    return fig_reward_centralize, ax_reward_centralize, [line]



def update_lines_outlet_utility(lines_out_utility , steps ,outlets ):
    for j, line in enumerate(lines_out_utility):
        x_data, y_data = line.get_data()
        x_data = np.append(x_data, steps)
        y_data = np.append(y_data, outlets[j].utility)
        line.set_data(x_data, y_data)


def update_lines_outlet_requested(lines_out_requested, steps , outlets):
    for j, line1 in enumerate(lines_out_requested):
        x_data, y_data = line1.get_data()
        x_data = np.append(x_data, steps)
        y_data = np.append(y_data, sum(outlets[j].dqn.environment.state.services_requested))
        line1.set_data(x_data, y_data)

def update_lines_outlet_ensured(lines_out_ensured,steps,outlets):
    for j, line2 in enumerate(lines_out_ensured):
        x_data, y_data = line2.get_data()
        x_data = np.append(x_data, steps)
        y_data = np.append(y_data, sum(outlets[j].dqn.environment.state.services_ensured))
        line2.set_data(x_data, y_data)


def update_lines_reward_decentralized(lines_out_reward_decentralize,steps,outlets):
    for j, line3 in enumerate(lines_out_reward_decentralize):
        x_data, y_data = line3.get_data()
        x_data = np.append(x_data, steps)
        y_data = np.append(y_data, outlets[j].dqn.environment.reward.episode_reward_decentralize)
        # print(" reward value dec : ", outlets[j].dqn.environment.reward.reward_value )

        # print("xdata : ",x_data)
        # print("ydata : ", y_data)
        line3.set_data(x_data, y_data)


def update_lines_reward_centralized(lines_out_reward_centralize,steps,gridcells_dqn):
    # print(" outlets :  ", outlets)
    for j, line4 in enumerate(lines_out_reward_centralize):
        x_data, y_data = line4.get_data()
        x_data = np.append(x_data, steps)
        y_data = np.append(y_data, gridcells_dqn[j].environment.reward.gridcell_reward_episode)
        # print(" reward value ce  : ", gridcells_dqn[j].environment.reward.reward_value )
        line4.set_data(x_data, y_data)
