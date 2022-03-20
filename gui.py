from PyQt5 import QtGui

import risar
from PIL import Image
from optimal_path import most_optimal
from connections import places_coords

img = Image.open('map.png')
width, height = img.size

risar.widget.setFixedHeight(height)
risar.widget.setFixedWidth(width)
risar.slika(0, 0, 'map.png')

risar.widget.setWindowTitle('Path finder algorithm visualizer')
risar.widget.setWindowIcon(QtGui.QIcon('map-icon.png'))


def draw_path():
    places, path = most_optimal()
    print(places)
    coords = [places_coords[place] for place in path]

    start_x, start_y = coords[0]
    end_x, end_y = coords[-1]
    risar.krog(start_x, start_y, 4, risar.barva(0, 176, 255), 4)
    risar.krog(end_x, end_y, 4, risar.barva(0, 176, 255), 4)
    for coord in zip(coords, coords[1:]):
        x1, y1 = coord[0]
        x2, y2 = coord[1]
        risar.crta(x1, y1, x2, y2, risar.barva(0, 176, 255), 7)


draw_path()

risar.stoj()
