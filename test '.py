my_list = [[1, 2], [3, 4], [1, 2]] # a list of lists
my_set = set(map(frozenset, my_list)) # convert the list of lists to a set of frozensets
for fs in my_set:
    print(list(fs))