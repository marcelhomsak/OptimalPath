import risar
from PIL import Image

im = Image.open('map_countries.png')
width, height = im.size

risar.widget.setFixedHeight(height)
risar.widget.setFixedWidth(width)
risar.slika(0, 0, 'map_countries.png')

risar.widget.setWindowTitle('Risar grafov')

places = {'Slovenia', 'Croatia', 'Italy', 'Austria', 'France', 'Serbia', 'Bosnia and Herzegovina', 'Germany', 'Netherlands', 'Belgium', 'Spain', 'Hungary', 'Holy See', 'San Marino', 'Switzerland', 'Czech Republic', 'Slovakia', 'Poland', 'Luxembourg', 'Andorra', 'Portugal', 'Lithuania', 'Ukraine', 'Denmark', 'Romania', 'Latvia', 'Estonia', 'Russia', 'Belarus', 'Moldova', 'Bulgaria', 'Kosovo', 'Montenegro', 'Macedonia', 'Greece', 'Turkey', 'Albania', 'Finland', 'Norway', 'Sweden'}
places_coords = {x: tuple() for x in places}
print(places_coords)
list_of_places = []
places_l = list(places)
i = 0
while True:
    click = risar.klik()
    if click is not None and click != False:
        places_coords[places_l[i]] = click
        i += 1
        print(places_coords)
    risar.cakaj(0.01)
