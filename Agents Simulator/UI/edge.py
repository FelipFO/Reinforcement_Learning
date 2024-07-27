from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic, QtGui, QtCore


class Edge(QtWidgets.QGraphicsLineItem):

    clicked_signal = pyqtSignal()

    def __init__(self, x, y, x2, y2, name):
        super(Edge, self).__init__(x, y, x2, y2)
        self.edge_name = name
        self.is_active = True
        self.active_color = QtGui.QColor(127, 127, 127)
        self.inactive_color = QtGui.QColor(127, 127, 127, 50)
        self.update_pen()

    def update_pen(self):
        color = self.inactive_color
        if self.is_active:
            color = self.active_color
        line_pen = QtGui.QPen(color)
        line_pen.setWidth(4)
        self.setPen(line_pen)

    def mousePressEvent(self, event):
        self.is_active = not self.is_active
        self.update_pen()
        self.scene().edge_clicked_signal.emit(self.edge_name)
        
