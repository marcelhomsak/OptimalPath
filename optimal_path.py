from collections import defaultdict
from random import choice
from time import time

from connections import connections

before = time()

s = defaultdict(set)
for k1, k2 in connections:
    s[k1].update({k2})
    s[k2].update({k1})

####################
from_point = "Piran"
to_point = "Gornja Radgona"
max_hop = 15
####################

def path(from_point, to_point, max_hop_var):
    path_list = [from_point]
    while from_point != to_point:
        if len(path_list) > max_hop_var:
            break
        rnd_next = choice(list(s[from_point]))
        while rnd_next in path_list and not choice(list(s[from_point])) in path_list:
            rnd_next = choice(list(s[from_point]))
        from_point = rnd_next
        path_list.append(from_point)
    return path_list

def most_optimal():
    for max_hop_var in range(max_hop + 1):
        for _ in range(1000):
            path_list = path(from_point, to_point, max_hop_var)
            if len(path_list) == max_hop_var:
                return f"From: {from_point}\nTo: {to_point}\nPath: {path_list}\nNumber of hops: {max_hop_var}"
print(most_optimal())

print(f"Running time: {time() - before :.2f} seconds")