from plotting.plotting import *


deque = []
deque = read_data(paths_reading_from(outlet_number=0),deque)
window_size = 10
result = rolling_average(deque, window_size)
print(len(deque))
x_values = [i for i in range(len(result))]  # Adjust x-axis values
plotting(x_values,result,window_size,'wifi',qvalue,"qvalue")
