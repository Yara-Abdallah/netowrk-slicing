import numpy as np

THREE_G = {
    "NUM_ANTENNAS": [1, 2],
    "CHANNEL_BANDWIDTH": np.arange(1.25, 5, 0.25),
    "CODING_RATE": [1 / 2, 1 / 3],
    "MODULATION_ORDER": [4],
    "AVERAGE_SYMBOLS_PER_SLOT": np.arange(184, 368, 1),
    "NUM_SLOTS_PER_FRAME": [15],
    "NUM_FRAMES_PER_SECOND": [10],
}

FOUR_G = {
    "NUM_ANTENNAS": [3, 4],
    "CHANNEL_BANDWIDTH": np.arange(1.5, 20, 0.5),
    "CODING_RATE": [1 / 2, 2 / 3, 3 / 4],
    "MODULATION_ORDER": [4, 6, 8],
    "AVERAGE_SYMBOLS_PER_SLOT": [12, 13, 14],
    "NUM_SLOTS_PER_FRAME": [10],
    "NUM_FRAMES_PER_SECOND": [20],
}

FIVE_G = {
    "NUM_ANTENNAS": [3, 4],
    "CHANNEL_BANDWIDTH": np.arange(5, 400, 5),
    "CODING_RATE": [1 / 2, 2 / 3, 3 / 4, 4 / 5, 5 / 6],
    "MODULATION_ORDER": [4, 6, 8, 10],
    "AVERAGE_SYMBOLS_PER_SLOT": [12, 13, 14],
    "NUM_SLOTS_PER_FRAME": [10],
    "NUM_FRAMES_PER_SECOND": [60, 120],
}
outlet = {}
for k in THREE_G:
    outlet[k] = np.random.choice(THREE_G[k])

print(*outlet)


def calculate_max_power(
        num_antennas,
        channel_bandwidth,
        coding_rate,
        modulation_order,
        average_symbol_per_slot,
        num_slots_per_frame,
        num_frames_per_second,
):
    spectral_efficiency = modulation_order * coding_rate  # bits/symbol

    capacity_per_antenna = (
                                   channel_bandwidth
                                   * 1e6
                                   * spectral_efficiency
                                   * average_symbol_per_slot
                                   * num_slots_per_frame
                                   * num_frames_per_second
                           ) / 1e6  # Mbps
    total_capacity = capacity_per_antenna * num_antennas
    print(f"capacity is: {total_capacity} Mbps")


calculate_max_power(
    outlet["NUM_ANTENNAS"],
    outlet["CHANNEL_BANDWIDTH"],
    outlet["CODING_RATE"],
    outlet["MODULATION_ORDER"],
    outlet["AVERAGE_SYMBOLS_PER_SLOT"],
    outlet["NUM_SLOTS_PER_FRAME"],
    outlet["NUM_FRAMES_PER_SECOND"]
)
