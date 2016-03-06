import sys


from PyQt5.QtWidgets import QWidget, QApplication


class Window(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)



app = QApplication(sys.argv)
window = Window()
window.show()

exit(app.exec_())
