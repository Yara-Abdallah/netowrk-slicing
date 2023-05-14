# my_list = [[1, 2], [3, 4], [1, 2]] # a list of lists
# my_set = set(map(frozenset, my_list)) # convert the list of lists to a set of frozensets
# for fs in my_set:
#     print(list(fs))
import gc
import sys


my_object = [1, 2, 3]
object_id = id(my_object)
my_object = None
# do something with my_object...
gc.collect()
if object_id in (id(obj) for obj in gc.get_objects()):
    print("my_object still exists in memory")

else:
    print("my_object has been garbage collected")

