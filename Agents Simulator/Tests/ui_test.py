from Simulator.simulator import Simulator
from PyQt5 import QtWidgets, QtGui, QtCore


class Canvas(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agents_positions = None

    def draw_agents(self, agents_positions):
        self.agents_positions = agents_positions
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush(QtCore.Qt.white)
        painter.setBrush(brush)
        painter.drawRect(event.rect())

        pen = QtGui.QPen()
        pen.setWidth(3)
        if self.agents_positions is not None:
            num_agents = self.agents_positions.shape[1]
            for agent_id in range(num_agents):
                x, y, theta = self.agents_positions[:, agent_id]
                painter.drawEllipse(int(x), int(y), 8, 8)


class MyWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.simulator = Simulator()
        self.simulator.agent_positions_signal.connect(self.slot_update_agents_position)
        self.simulator.reset_simulation()
        self.canvas = Canvas(self)
        self.simulation_start_button = QtWidgets.QPushButton('Start Simulation')
        self.simulation_start_button.clicked.connect(self.start_simulation)

        self.cb = QtWidgets.QComboBox()
        self.cb.addItems(["Linea", "Triangulo", "Pentagono"])
        self.cb.currentIndexChanged.connect(self.formation_changed)
        self.formations_dict = {"Linea": "vertical_line", "Triangulo": "triangle", "Pentagono": "pentagon"}

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.simulation_start_button)
        self.layout.addWidget(self.cb)
        self.resize(500, 500)
        self.canvas.draw_agents(self.simulator.agents.agents_positions)

    def start_simulation(self):
        self.canvas.draw_agents(self.simulator.agents.agents_positions)
        self.simulator.start()

    def formation_changed(self):
        target_simulation = self.cb.currentText()
        target_simulation = self.formations_dict[target_simulation]
        self.simulator.formation_name = target_simulation

    def slot_update_agents_position(self, agents_position):
        self.canvas.draw_agents(agents_position)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec()