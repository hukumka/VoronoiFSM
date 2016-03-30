#!/usr/bin/python3

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

from random import uniform
from Vector import Vect2 as Vect

from VoronoiData import VoronoiData
from VoronoiCWrap import Voronoi
from VoronoiRender import VoronoiRenderWidget

from Hunt import rule, generator
from Hunt import precalculation1, precalculation2


class Window(QWidget):
    WIDTH = 1920
    HEIGHT = 1080
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.voronoi_widget = self.init_voronoi_render()
        self.voronoi_widget.resize(self.WIDTH, self.HEIGHT)
        self.showFullScreen()

    def init_voronoi_render(self):
        def point_on_screen():
            PADDING = 10
 
            x = uniform(PADDING, self.WIDTH - PADDING)
            y = uniform(PADDING, self.HEIGHT - PADDING)
            return Vect(x, y)
 
        points = [point_on_screen() for _ in range(10000)]

        print("Begin constructing voronoi diagram")
        voronoi = Voronoi(points)
        print("Transfrom into graph view")
        voronoi_data = VoronoiData(voronoi)
        voronoi_data.generate_state(generator)
 
        voronoi_data.bind_rule(rule)
        voronoi_data.bind_precalculations([precalculation1, precalculation2])
 
        print("Load data into video buffer")
        render = VoronoiRenderWidget(voronoi_data, self)
        print("done")
        return render

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self.voronoi_widget.pause_toggle()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    code = app.exec_()
    exit(code)
