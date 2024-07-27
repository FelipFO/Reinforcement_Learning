from utils import get_agent_colors
from PyQt5 import QtWidgets, QtGui, QtCore


class Canvas(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agents_positions = get_agent_colors()
        self.agent_colors = get_agent_colors()
        print("Canvas loaded ")

    def draw_agents(self, agents_positions):
        self.agents_positions = agents_positions
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush(QtCore.Qt.white)
        painter.setBrush(brush)
        painter.drawRect(event.rect())
        pen = QtGui.QPen()
        pen.setWidth(1)
        if self.agents_positions is not None:
            num_agents = self.agents_positions.shape[1]
            for agent_id in range(num_agents):
                x, y, theta = self.agents_positions[:, agent_id]
                brush = QtGui.QBrush(self.agent_colors[agent_id])
                painter.setBrush(brush)
                pen.setColor(self.agent_colors[agent_id])
                painter.setPen(pen)
                painter.drawEllipse(int(x), int(y), 8, 8)

