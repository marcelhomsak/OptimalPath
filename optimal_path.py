from random import choice
from math import e
from time import time

from PyQt5 import QtGui
from PIL import Image
import risar

from connections import cities_coords, countries_coords
from connections import cities, countries

#################### MODE: cities or countries
# s = cities OR s = countries
s = countries
# map = 'map_cities.png' OR map = 'map_countries.png'
map = 'map_countries.png'
# coords = cities_coords OR countries_coords
coords = countries_coords
from_point = "France"
to_point = "Greece"
####################
max_hop = 15
base = 3
power = 0.895
####################

img = Image.open(map)
width, height = img.size

risar.widget.setFixedHeight(height)
risar.widget.setFixedWidth(width)
risar.slika(0, 0, map)

risar.widget.setWindowTitle('Path Finder Algorithm Visualizer')
risar.widget.setWindowIcon(QtGui.QIcon('map-icon.png'))

before = time()

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
                return from_point, to_point, path_list, max_hop_var

def draw_path(coords):
    from_point, to_point, path_list, max_hop_var = most_optimal()
    print(f"From: {from_point}\nTo: {to_point}\nPath: {path_list}\nNumber of hops: {max_hop_var-1}")
    coords = [coords[place] for place in path_list]

    start_x, start_y = coords[0]
    end_x, end_y = coords[-1]
    risar.krog(start_x, start_y, 4, risar.barva(0, 176, 255), 4)
    risar.krog(end_x, end_y, 4, risar.barva(0, 176, 255), 4)
    for coord in zip(coords, coords[1:]):
        x1, y1 = coord[0]
        x2, y2 = coord[1]
        risar.crta(x1, y1, x2, y2, risar.barva(0, 176, 255), 7)


draw_path(coords)

print(f"Running time: {time() - before :.2f} seconds")

risar.stoj()