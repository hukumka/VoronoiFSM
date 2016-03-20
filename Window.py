#!/usr/bin/python3

from Vector import Vect2 as Vect
from random import randint

from VoronoiData import VoronoiData
from VoronoiCWrap import Voronoi
from VoronoiRender import VoronoiRenderWidget

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

from Hunt import rule, generator
from Hunt import precalculation1, precalculation2


class Window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        voronoi_data = self.init_voronoi()
        self.voronoi_widget = VoronoiRenderWidget(voronoi_data, self)
        self.voronoi_widget.resize(1920, 1080)

    def init_voronoi(self):
        def point_on_screen():
            WIDTH = 1920
            HEIGHT = 1080
            PADDING = 10

            x = randint(PADDING, WIDTH - PADDING)
            y = randint(PADDING, HEIGHT - PADDING)
            return Vect(x, y)

        points = [point_on_screen() for _ in range(8000)]
        voronoi = Voronoi(points)
        voronoi_data = VoronoiData(voronoi)
        voronoi_data.generate_state(generator)

        voronoi_data.bind_rule(rule)
        voronoi_data.bind_precalculations([precalculation1, precalculation2])

        return voronoi_data

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.voronoi_widget.pause_toggle()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    window = Window()
    window.showFullScreen()

    code = app.exec_()
    exit(code)
