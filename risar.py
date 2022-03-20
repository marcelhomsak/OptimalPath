# coding=utf-8

# V tem rokohitrskem modulu so demonstrirane vse možne slabe programerske
# prakse in triki v Pythonu, zato ga raje ne glej. Hvala.

import time
from functools import wraps

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

app = QApplication([])

def setup():
    class QGraphicsViewWMouse(QGraphicsView):
        def __init__(self, *args, **kw):
            super(QGraphicsViewWMouse, self).__init__(*args, **kw)
            self.setMouseTracking(True)
            self.clicked = False
            self.pos = (0, 0)
            self.left = self.right = False

        def mouseMoveEvent(self, ev):
            self.pos = (ev.x(), ev.y())
            super(QGraphicsViewWMouse, self).mouseMoveEvent(ev)

        def mousePressEvent(self, ev):
            self.clicked = (ev.x(), ev.y())
            super(QGraphicsViewWMouse, self).mousePressEvent(ev)

        def get_click(self):
            value = self.clicked
            self.clicked = None
            return value

        def keyPressEvent(self, ev):
            super().keyPressEvent(ev)
            self.left = ev.key() == Qt.Key_Left
            self.right = ev.key() == Qt.Key_Right

        def keyReleaseEvent(self, ev):
            super().keyReleaseEvent(ev)
            self.left = self.right = False

    widget = QDialog()
    widget.setWindowTitle("Janezovo zasilno platno")
    widget.setLayout(QVBoxLayout())
    widget.layout().setContentsMargins(2, 2, 2, 2)
    widget.scene = QGraphicsScene(widget)
    widget.scene.setBackgroundBrush(Qt.black)
    widget.view = QGraphicsViewWMouse(widget.scene, widget)
    widget.view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    widget.view.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
    widget.view.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
    widget.layout().addWidget(widget.view)
    widget.resize(800, 500)
    widget.scene.setSceneRect(0, 0, widget.view.width(), widget.view.height())
    widget.view.setSceneRect(0, 0, widget.view.width(), widget.view.height())
    widget.show()
    widget.raise_()
    return widget


widget = setup()
maxx = maxX = widget.view.width()
maxy = maxY = widget.view.height()

globals().update(
    dict(bela=Qt.white, crna=Qt.black, rdeca=Qt.red, zelena=Qt.green,
         modra=Qt.blue, vijolicna=Qt.magenta, rumena=Qt.yellow, siva=Qt.gray,
         rjava=Qt.darkRed))

barva = QColor

obnavljaj = True

def nakljucna_barva():
    """Vrni naključno barvo."""
    from random import randint
    return barva(randint(0, 255), randint(0, 255), randint(0, 255))

def nakljucne_koordinate():
    """Vrni naključen kordinate."""
    from random import randint
    return randint(0, maxX), randint(0, maxY)

def obnovi():
    """
    Obnovi sliko na zaslonu.

    Funkcije ni potrebno klicati, če je 'obnavljaj' nastavljen na True. Prav
    tako funkcija 'cakaj' sama pokliče tudi 'obnovi'.
    """
    widget.scene.update()
    qApp.processEvents()

def pogojno_obnovi(f):
    @wraps(f)
    def g(*args, **kwargs):
        obj = f(*args, **kwargs)
        if obnavljaj:
            obnovi()
        return obj
    return g

def cakaj(t: int):
    """Počakaj t sekund."""
    obnovi()
    time.sleep(t)

@pogojno_obnovi
def barva_ozadja(barva):
    """Nastavi barvo ozadja."""
    widget.scene.setBackgroundBrush(barva)


@pogojno_obnovi
def crta(x0, y0, x1, y1, barva=bela, sirina=1):
    """Potegni črto med podanima točkama."""
    crta = widget.scene.addLine(0, 0, x1-x0, y1-y0, QPen(QBrush(barva), sirina))
    crta.setPos(x0, y0)
    return crta


@pogojno_obnovi
def tocka(x, y, barva=bela):
    """Nariše točko na podanih koordinatah."""
    return widget.scene.addLine(x, y, x, y, QPen(QBrush(barva), 1))


@pogojno_obnovi
def elipsa(x, y, rx, ry, barva=bela, sirina=1):
    """Nariše elipso s središčem v (x, y) in polmeroma rx in ry."""
    elipsa = widget.scene.addEllipse(-rx, -ry, 2*rx, 2*ry, QPen(QBrush(barva), sirina))
    elipsa.setPos(x, y)
    return elipsa

@pogojno_obnovi
def krog(x, y, r, barva=bela, sirina=1):
    """Nariše krog s polmerom r in središčem v (x, y)."""
    return elipsa(x, y, r, r, barva, sirina)


@pogojno_obnovi
def besedilo(x, y, txt, barva=bela, velikost=20, pisava="Arial"):
    """Izpiše besedilo txt; koordinati podajata zgornji levi vogal."""
    font = QFont(pisava)
    font.setPixelSize(velikost)
    txt = widget.scene.addText(txt, font)
    txt.setPos(x, y)
    txt.setDefaultTextColor(barva)
    return txt


def dimenzije(txt, velikost=20, pisava="Arial"):
    font = QFont(pisava)
    font.setPixelSize(velikost)
    br = QFontMetrics(font).boundingRect(txt)
    return br.width(), br.height()

@pogojno_obnovi
def slika(x, y, fname):
    """
    Naloži sliko iz datoteke fname in jo postavi na sliko tako, da je
    zgornji levi vogal na koordinatah (x, y)
    """
    pict = QPixmap(fname)
    pixmap = widget.scene.addPixmap(pict)
    pixmap.setPos(x, y)
    return pixmap


@pogojno_obnovi
def odstrani(stvar):
    widget.scene.removeItem(stvar)


def pobrisi():
    widget.scene.clear()
    obnovi()


def shrani(filename):
    import os
    scene = widget.scene
    source = scene.itemsBoundingRect().adjusted(-15, -15, 15, 15)
    size = source.size()
    buffer = QPixmap(int(size.width()), int(size.height()))

    painter = QPainter()
    painter.begin(buffer)
    try:
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(buffer.rect(), scene.backgroundBrush())
        target = QRectF(0, 0, source.width(), source.height())
        scene.render(painter, target, source)
        buffer.save(filename, os.path.splitext(filename)[1][1:])
    finally:
        painter.end()

def stoj():
    qApp.exec()


def klik():
    return widget.view.get_click()

def miska():
    return widget.view.pos

def levo():
    return widget.view.left

def desno():
    return widget.view.right
