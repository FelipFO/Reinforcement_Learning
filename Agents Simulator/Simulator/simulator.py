import time
import copy
import numpy as np
from Agents.agents import Agents
from Controllers.dt_dsd import DTDSD
from PyQt5.QtCore import QThread, pyqtSignal
from Formations.formations_generator import FormationsGenerator


class Simulator(QThread):

    agent_positions_signal = pyqtSignal(np.ndarray)
    simulation_finished_signal = pyqtSignal()

    def __init__(self):
        super(Simulator, self).__init__()
        self.running = False
        self.num_agents = 5
        self.simulation_steps = 350
        self.formation_name = "vertical_line"

        self.adjacency_matrix = np.array([[0., 1., 1., 1., 1.],
                                          [1., 0., 1., 1., 1.],
                                          [1., 1., 0., 1., 1.],
                                          [1., 1., 1., 0., 1.],
                                          [1., 1., 1., 1., 0.]])

        self.initial_positions = np.array([[60., 120., 180., 240., 300.],
                                           [130., 130., 130., 130., 130.],
                                           [0., 0., 0., 0., 0.]])
        self.agents = Agents(self.num_agents)
        self.gammas = [self.agents.max_x, self.agents.max_y]
        epsilons = [(1 - 1e-3) * 1 / (2 * self.gammas[0]), (1 - 1e-3) * 1 / (2 * self.gammas[1])]
        self.controller = DTDSD(num_robots=self.num_agents, num_populations=2, epsilon=epsilons, gamma=self.gammas)
        self.controller.set_adjacency_matrix(self.adjacency_matrix)
        self.t = 0
        self.formation_generator = FormationsGenerator(self.num_agents)
        self.leader_reference, self.followers_deltas = None, None
        self.reset_simulation()

    def run(self):

        self.running = True
        self.leader_reference, self.followers_deltas = self.formation_generator.get_formation(self.formation_name)
        last_positions = copy.deepcopy(self.agents.agents_positions)
        while self.running:
            leader_position = self.agents.agents_positions[:2, 0].reshape(2, 1)
            controller_input = np.hstack((-leader_position, self.followers_deltas[:2, :]))
            references = self.controller.step(controller_input).reshape(2, self.num_agents)
            # reset leader reference
            references[:, 0] = self.leader_reference[:2]
            # add angle zeros
            references = np.vstack((references, np.zeros((1, self.num_agents))))
            self.agents.step(references)
            self.agent_positions_signal.emit(self.agents.agents_positions)
            self.t += 1
            if (self.t == self.simulation_steps) or (np.all(last_positions == self.agents.agents_positions)):
                self.t = 0
                self.stop()
                self.simulation_finished_signal.emit()
            last_positions = copy.deepcopy(self.agents.agents_positions)
            time.sleep(0.01)

    def stop(self):
        self.running = False

    def reset_simulation(self):
        self.agents.reset(initial_positions=self.initial_positions)
        x0 = self.agents.agents_positions[:2, :].copy()
        x0[:, 0] = self.num_agents*np.array(self.gammas)
        self.controller.reset(x0=x0.reshape(-1))

    def publish_positions(self):
        self.agent_positions_signal.emit(self.agents.agents_positions)

    def update_adjacency_matrix(self, edge_name):
        i, j = [int(dig)-1 for dig in list(edge_name)]
        self.adjacency_matrix[i][j] = 1 - self.adjacency_matrix[i][j]
        self.adjacency_matrix[j][i] = 1 - self.adjacency_matrix[j][i]
        self.controller.set_adjacency_matrix(self.adjacency_matrix)
        print("Adjacency Matrix updated to: ")
        print(self.adjacency_matrix)