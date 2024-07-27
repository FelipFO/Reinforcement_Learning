from UI.edge import Edge
from PyQt5 import QtGui, QtCore
from utils import get_agent_colors
from PyQt5.QtWidgets import QGraphicsScene


class Scene(QGraphicsScene):

    edge_clicked_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.edge_13 = Edge(-80 + 15, -40 + 15, 0 + 15, -100 + 15, "13")
        self.addItem(self.edge_13)

        self.edge_23 = Edge(-80 + 15, -40 + 15, 80 + 15, -40 + 15, "23")
        self.addItem(self.edge_23)

        self.edge_35 = Edge(-80 + 15, -40 + 15, -50 + 15, 50 + 15, "35")
        self.addItem(self.edge_35)

        self.edge_34 = Edge(-80 + 15, -40 + 15, 50 + 15, 50 + 15, "34")
        self.addItem(self.edge_34)

        self.edge_12 = Edge(0 + 15, -100 + 15, 80 + 15, -40 + 15, "12")
        self.addItem(self.edge_12)

        self.edge_14 = Edge(0 + 15, -100 + 15, 50 + 15, 50 + 15, "14")
        self.addItem(self.edge_14)

        self.edge_15 = Edge(0 + 15, -100 + 15, -50 + 15, 50 + 15, "15")
        self.addItem(self.edge_15)

        self.edge_24 = Edge(80 + 15, -40 + 15, 50 + 15, 50 + 15, "24")
        self.addItem(self.edge_24)

        self.edge_25 = Edge(80 + 15, -40 + 15, -50 + 15, 50 + 15, "25")
        self.addItem(self.edge_25)

        self.edge_45 = Edge(50 + 15, 50 + 15, -50 + 15, 50 + 15, "45")
        self.addItem(self.edge_45)

        self.nodes = self.create_nodes()

    def create_nodes(self):
        nodes = list()
        agents_colors = get_agent_colors()
        positions = {0: {"x": 0, "y": -100},
                     1: {"x": 80, "y": -40},
                     2: {"x": -80, "y": -40},
                     3: {"x": 50, "y": 50},
                     4: {"x": -50, "y": 50}}
        for agent_id in range(5):
            node_graph_brush = QtGui.QBrush(agents_colors[agent_id])
            node_graph_pen = QtGui.QPen(agents_colors[agent_id])
            node = self.addEllipse(positions[agent_id]["x"], positions[agent_id]["y"], 30, 30,
                                   node_graph_pen, node_graph_brush)
            nodes.append(node)
        return nodes

