import math

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtOpenGL import *
import numpy


from VoronoiCWrap import Voronoi
from VoronoiData import VoronoiData
from Vector import Vect2

from random import randint, uniform


from itertools_recipe import pairwise_looped, pairwise

from Hunt import rule, generator
from Hunt import precalculation1, precalculation2


class VoronoiRenderWidget(QGLWidget):
    def __init__(self, voronoi_data, parent=None):
        assert isinstance(voronoi, Voronoi)

        QGLWidget.__init__(self, parent)
        self.voronoi = voronoi_data

        # points will need to view points
        points = []
        lines = []
        triangles = []

        for p in self.voronoi._points:
            # points
            points.append([p.x, p.y])

            # lines
            for p1, p2 in pairwise_looped(p.polygone):
                lines.append([p1.x, p1.y])
                lines.append([p2.x, p2.y])

            # triagles (for colorise)
            poly = iter(p.polygone)
            p1 = next(poly, None)
            if p1 is not None:
                for p2, p3 in pairwise(poly):
                    triangles.append([p1.x, p1.y])
                    triangles.append([p2.x, p2.y])
                    triangles.append([p3.x, p3.y])


        self.__vertex_buffer = triangles + lines + points
        self.__triangles_count = len(triangles)
        self.__lines_count = len(lines)
        self.__points_count = len(points)

        self.__init_color_vbo();

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.evalute)

    def evalute(self):
        self.voronoi.update(rule, [precalculation1, precalculation2])
        self.update()

    def update(self):
        self.__reload_colors()
        #glColorPointer(3, GL_FLOAT, 0, self.__colors)
        glColorPointerf(self.__colors)
        QGLWidget.update(self)


    def __init_color_vbo(self):
        self.__colors = numpy.array([[.0, .5, .0]]*(self.__triangles_count), 'f')
        self.__reload_colors()


    def __reload_colors(self):
        triangle_id = 0
        for point in self.voronoi._points:
            red = uniform(0.0, 0.5)
            green = uniform(0.0, 0.5)
            blue = uniform(0.0, 0.5)
            triangles_count = len(point.polygone) - 2
            if triangles_count <= 0:
                continue
            else:
                for i in range(triangles_count):
                    for j in range(3):
                        index = (triangle_id + i) * 3 + j
                        color = self.__get_color(point.state)
                        self.__colors[index] = color
                triangle_id += triangles_count

    def __get_color(self, state):
        colors = [[0, 0, 0],
                  [0.4, 0, 0],
                  [0.8, 0, 0],
                  [0.6, 0, 0],
                  [0.8, 0, 0],
                  [1, 0, 0],
                  [0.2, 0.5, 0.5]]
        return colors[state]


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnableClientState(GL_VERTEX_ARRAY)

        glEnableClientState(GL_COLOR_ARRAY)

        glDrawArrays(GL_TRIANGLES, 0, self.__triangles_count)
        glDisableClientState(GL_COLOR_ARRAY)

        glDrawArrays(GL_LINES, self.__triangles_count, self.__lines_count)

        glPointSize(2.0)
        glDrawArrays(GL_POINTS, self.__triangles_count + self.__lines_count, self.__points_count)
        glFlush()

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)
        glVertexPointerf(self.__vertex_buffer)
        glColorPointerf(self.__colors)
        #glMatrixMode(GL_PROJECTION)
        #glLoadIdentity()
        #glOrtho(0, 1, 1, 0, 0, 1)


    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        ratio = width / height
        #gluPerspective(40, width/2, height/2, 30)
        glOrtho(0, width, 0, height, -1, 1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.timer.isActive():
                self.timer.stop()
            else:
                self.timer.start(0.04)

    def mousePressEvent(self, event):
        self.voronoi.change_closest(event.x(), self.height() - event.y())
        self.__reload_colors()
        self.update()



if __name__ == '__main__':
    import sys
    from random import randint
    app = QApplication(sys.argv)


    points = [Vect2(randint(10, 1910), randint(10, 1070)) for _ in range(500)]
    #points = [Vect2(100, 100), Vect2(400, 100), Vect2(100, 400)]

    voronoi = Voronoi(points)
    voronoi_data = VoronoiData(voronoi)
    voronoi_data.generate_state(generator)

    window = VoronoiRenderWidget(voronoi_data)
    window.showFullScreen()

    exit(app.exec_())
