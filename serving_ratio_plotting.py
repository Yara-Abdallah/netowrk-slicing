from plotting.plotting import *

deque =[ ]
deque = read_data(paths_reading_from(outlet_number=2),deque)
# Example usage:
window_size = 200
result = rolling_average(deque, window_size)
print(len(deque))
x_values = [i for i in range(len(result))]  # Adjust x-axis values
plotting(x_values,result,window_size,'4G',serving_ratio,"serving_ratio")

