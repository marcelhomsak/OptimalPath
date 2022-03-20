from random import choice
from math import e
from time import time

from connections import cities, countries

before = time()

####################
s = countries
####################
from_point = "Norway"
to_point = "Netherlands"
max_hop = 15
base = 4
power = 0.75
####################

def path(from_point, to_point, max_hop_var):
    path_list = [from_point]
    while from_point != to_point:
        if len(path_list) > max_hop_var:
            break
        rnd_next = choice(list(s[from_point]))
        was_not_there = s[from_point].difference(set(path_list))
        if rnd_next in path_list and was_not_there != set():
            rnd_next = choice(list(was_not_there))
        from_point = rnd_next
        path_list.append(from_point)
    return path_list

def most_optimal():
    for max_hop_var in range(max_hop + 1):
        for _ in range(int(base*e**(power*max_hop_var))):
            path_list = path(from_point, to_point, max_hop_var)
            if len(path_list) == max_hop_var:
                return f"From: {from_point}\nTo: {to_point}\nPath: {path_list}\nNumber of hops: {max_hop_var}"
print(most_optimal())

print(f"Running time: {time() - before :.2f} seconds")