
from plotting.plotting import *

deque = []
deque = read_data(paths_reading_from(outlet_number=0),deque)
print(len(deque))

window_size = 200
result = rolling_average(deque, window_size)
x_values = [i for i in range(len(result))]  # Adjust x-axis values
plotting(x_values,result,window_size,'wifi',occupancy,"occupancy")
