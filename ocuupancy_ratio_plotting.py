
from plotting.plotting import *

deque = []
deque = read_data(paths_reading_from(outlet_number=1),deque)
print(len(deque))
for i in deque:
    print(i)
window_size = 1
result = rolling_average(deque, window_size)
x_values = [i for i in range(len(result))]  # Adjust x-axis values
plotting(x_values,result,window_size,'3G',occupancy,"occupancy")
