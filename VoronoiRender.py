#!/usr/bin/python3

from PyQt5.QtCore import QTimer
from OpenGL.GL import *  # NOQA
from OpenGL.GLU import *  # NOQA
from PyQt5.QtOpenGL import QGLWidget
import numpy
from itertools_recipe import pairwise_looped, pairwise

from ctypes import Structure, c_int


class CellColor(Structure):
    _fields_ = [("triagngleCount", c_int),
                ("state", c_int)]


class VoronoiRenderWidget(QGLWidget):
    __CELL_COLORS = [[0.0, 0.0, 0.0],
                     [0.8, 0.0, 0.0],
                     [0.3, 0.6, 0.6]]

    def __init__(self, voronoi_data, parent=None):
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

        self.__init_color_cells()

        self.__vertex_buffer = triangles + lines + points
        self.__triangles_count = len(triangles)
        self.__lines_count = len(lines)
        self.__points_count = len(points)

        self.__init_color_vbo()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.evalute)

    def __init_color_cells(self):
        CellsArray = CellColor * self.__points.count
        self.__color_sells = CellsArray()
        for i, point in enumerate(self.voronoi._points):
            self.__color_sells[i].trianglesCount = len(point.neighbors) - 2
            self.__color_sells[i].state = point.state

    def __reload_color_cells(self):
        for i, point in enumerate(self.voronoi._points):
            self.__color_sells[i].state = point.state

    def evalute(self):
        self.voronoi.update()
        self.update()

    def update(self):
        self.__reload_colors()
        glColorPointerf(self.__colors)
        QGLWidget.update(self)

    def __init_color_vbo(self):
        colors = [[0, 0, 0]] * (self.__triangles_count)
        self.__colors = numpy.array(colors, 'f')
        self.__reload_colors()

    def __reload_colors(self):
        triangle_id = 0
        for point in self.voronoi._points:
            triangles_count = len(point.polygone) - 2
            if triangles_count <= 0:
                continue
            else:
                color = self.__get_color(point.state)
                for i in range(triangles_count*3):
                    index = (triangle_id) * 3 + i
                    self.__colors[index] = color
                triangle_id += triangles_count

    def __get_color(self, state):
        return self.__CELL_COLORS[state]

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
        glDrawArrays(GL_POINTS, self.__triangles_count + self.__lines_count,
                     self.__points_count)
        glFlush()

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)
        glVertexPointerf(self.__vertex_buffer)
        glColorPointerf(self.__colors)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)

    def pause_toggle(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(16)

    def mousePressEvent(self, event):
        self.voronoi.change_closest(event.x(), self.height() - event.y())
        self.__reload_colors()
        self.update()
