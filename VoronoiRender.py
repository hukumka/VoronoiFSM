import math

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtOpenGL import *


from VoronoiCWrap import Voronoi
from Vector import Vect2

from random import randint, uniform


class VoronoiRenderWidget(QGLWidget):
    def __init__(self, voronoi, parent=None):
        assert isinstance(voronoi, Voronoi)

        QGLWidget.__init__(self, parent)
        self.voronoi = voronoi

        # points will need to view points
        self.__points = []
        for p in voronoi._points:
            self.__points.append([p.x, p.y])

        # same for lines
        self.__lines = []
        for _, linelist in voronoi._lines.items():
            for p1, p2 in linelist:
                self.__lines.append([p1.x, p1.y])
                self.__lines.append([p2.x, p2.y])

        # triagles need to colorise it
        self.__triangles = []
        for _, points in voronoi._line_points.items():
            p1 = points[0]
            for i in range(1, len(points)-1):
                p2 = points[i]
                p3 = points[i+1]

                self.__triangles.append([p1.x, p1.y])
                self.__triangles.append([p2.x, p2.y])
                self.__triangles.append([p3.x, p3.y])

        self.__color_list = [[0.0, 0.0, 0] for _ in self.__triangles]

        self.__reload_colors();

        self.__vertex_buffer = self.__triangles + self.__lines + self.__points

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.evalute)

    def evalute(self):
        self.voronoi.update()
        self.update()

    def update(self):
        self.__reload_colors()
        glColorPointerf(self.__color_list)
        QGLWidget.update(self)


    def __reload_colors(self):

        triangle_id = 0
        for center_point, points in self.voronoi._line_points.items():
            red = uniform(0.0, 0.5)
            green = uniform(0.0, 0.5)
            blue = uniform(0.0, 0.5)
            triangles_count = len(points) - 2
            if triangles_count <= 0:
                continue
            else:
                for i in range(triangles_count):
                    for j in range(3):
                        index = (triangle_id + i) * 3 + j
                        self.__color_list[index] = self.voronoi.get_color(center_point)
                triangle_id += triangles_count


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glEnableClientState(GL_VERTEX_ARRAY)

        glEnableClientState(GL_COLOR_ARRAY)

        glDrawArrays(GL_TRIANGLES, 0, len(self.__triangles))
        glDisableClientState(GL_COLOR_ARRAY)

        glDrawArrays(GL_LINES, len(self.__triangles), len(self.__lines))

        glPointSize(2.0)
        glDrawArrays(GL_POINTS, len(self.__triangles) + len(self.__lines), len(self.__points))
        glFlush()

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)
        glVertexPointerf(self.__vertex_buffer)
        glColorPointerf(self.__color_list)
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
                self.timer.start(0.3)

    def mousePressEvent(self, event):
        self.voronoi.change_closest(event.x(), self.height() - event.y())
        self.__reload_colors()
        self.update()



if __name__ == '__main__':
    import sys
    from random import randint
    app = QApplication(sys.argv)


    points = [Vect2(randint(200, 1720), randint(200, 880)) for _ in range(500)]
    #points = [Vect2(100, 100), Vect2(400, 100), Vect2(100, 400)]

    voronoi = Voronoi(points)

    window = VoronoiRenderWidget(voronoi)
    window.showFullScreen()

    exit(app.exec_())
