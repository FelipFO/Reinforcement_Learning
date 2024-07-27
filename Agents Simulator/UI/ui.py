from canvas import Canvas
from UI.scene import Scene
from PyQt5 import uic, QtGui, QtCore
from Simulator.simulator import Simulator
from PyQt5.QtWidgets import QMainWindow, QPushButton, QRadioButton, QGraphicsView, QLabel


class UI(QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("Layouts/mainwindow.ui", self)
        self.setWindowTitle("Simulator")
        self.setMaximumSize(QtCore.QSize(800, 600))
        self.setWindowFlags(QtCore.Qt.WindowType.CustomizeWindowHint |
                            QtCore.Qt.WindowType.WindowCloseButtonHint |
                            QtCore.Qt.WindowType.WindowMinimizeButtonHint)
        self.simulator = Simulator()
        self.simulator.reset_simulation()

        self.canvas = self.findChild(Canvas, "canvas")

        self.radio_button_lineal = self.findChild(QRadioButton, "rdb_lineal")
        self.radio_button_triangular = self.findChild(QRadioButton, "rdb_trian")
        self.radio_button_pentagonal = self.findChild(QRadioButton, "rdb_penta")

        self.formations_dict = {"Lineal": "vertical_line", "Triangular": "triangle", "Pentogonal": "pentagon"}
        self.radio_button_lineal.toggled.connect(lambda: self.slot_radio_button_state(self.radio_button_lineal))
        self.radio_button_triangular.toggled.connect(lambda:
                                                     self.slot_radio_button_state(self.radio_button_triangular))
        self.radio_button_pentagonal.toggled.connect(lambda:
                                                     self.slot_radio_button_state(self.radio_button_pentagonal))
        self.formation_label_widget = self.findChild(QLabel, "formation_label")
        self.radio_button_lineal.setChecked(True)

        self.simulation_start_button = self.findChild(QPushButton, "start_simulation")
        self.simulation_start_button.clicked.connect(self.slot_start_simulation)
        self.simulation_restart_button = self.findChild(QPushButton, "restart_simulation")
        self.simulation_restart_button.clicked.connect(self.slot_restart_simulation)

        self.scene = Scene()
        self.graph_canvas_view = self.findChild(QGraphicsView, "graph_canvas")
        self.graph_canvas_view.setScene(self.scene)
        self.scene.edge_clicked_signal.connect(self.slot_edge_clicked)

        self.simulator.agent_positions_signal.connect(self.slot_update_agents_position)
        self.simulator.simulation_finished_signal.connect(self.slot_enable_start_button)
        self.simulator.publish_positions()

        self.simulation_running = False

        self.show()

    def slot_edge_clicked(self, edge_name):
        self.simulator.update_adjacency_matrix(edge_name)

    def slot_restart_simulation(self):
        print("Restarting simulation")
        self.simulator.reset_simulation()
        self.simulator.publish_positions()

    def slot_start_simulation(self):
        print("Starting simulation")
        self.canvas.draw_agents(self.simulator.agents.agents_positions)
        self.simulation_start_button.setEnabled(False)
        self.simulation_restart_button.setEnabled(False)
        self.simulation_start_button.setStyleSheet("background-color: gray")
        self.simulation_restart_button.setStyleSheet("background-color: gray")
        self.simulator.start()
        self.simulation_running = True

    def slot_enable_start_button(self):
        self.simulation_running = False
        self.simulation_start_button.setEnabled(True)
        self.simulation_start_button.setStyleSheet("background-color: white")
        self.simulation_restart_button.setEnabled(True)
        self.simulation_restart_button.setStyleSheet("background-color: white")

    def slot_update_agents_position(self, agents_position):
        self.canvas.draw_agents(agents_position)

    def slot_radio_button_state(self, button):
        if button.isChecked():
            target_simulation = button.text()
            target_simulation = self.formations_dict[target_simulation]
            image = QtGui.QPixmap(f"Images/{target_simulation}.png")
            self.formation_label_widget.setPixmap(image)
            self.simulator.formation_name = target_simulation
