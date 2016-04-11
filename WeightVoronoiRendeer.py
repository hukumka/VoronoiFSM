#!/usr/bin/python3

from PyQt5.QtWidgets import QApplication
from OpenGL.GL import *  # NOQA
from OpenGL.GLU import *  # NOQA
from PyQt5.QtOpenGL import QGLWidget
from itertools_recipe import pairwise_looped, pairwise

from WeightVoronoi import Voronoi, WeightPoint
from random import randint
from random import uniform
from Vector import Vect2 as Vect


class VoronoiRenderWidget(QGLWidget):
    def __init__(self, voronoi_data, parent=None):
        QGLWidget.__init__(self, parent)
        self.voronoi = voronoi_data

        # points will need to view points
        points = []
        lines = []
        triangles = []

        for p in self.voronoi.points:
            # points
            points.append([p.x, p.y])

            # lines
            for border in p.borders:
                for p1, p2 in border.lines():
                    lines.append([p1.x, p1.y])
                    lines.append([p2.x, p2.y])

        self.__vertex_buffer = lines + points
        self.__lines_count = len(lines)
        self.__points_count = len(points)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnableClientState(GL_VERTEX_ARRAY)
        glDrawArrays(GL_LINES, 0, self.__lines_count)

        glPointSize(2.0)
        glDrawArrays(GL_POINTS, self.__lines_count, self.__points_count)
        glFlush()

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)
        glVertexPointerf(self.__vertex_buffer)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)


def point_on_screen():
    WIDTH = 1920
    HEIGHT = 1080
    PADDING = 10

    x = randint(PADDING, WIDTH - PADDING)
    y = randint(PADDING, HEIGHT - PADDING)
    return WeightPoint(x, y, uniform(1, 3))


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    points = [point_on_screen() for _ in range(100)]
    voronoi = Voronoi(points)
    window = VoronoiRenderWidget(voronoi)
    window.showFullScreen()

    code = app.exec_()
    exit(code)
