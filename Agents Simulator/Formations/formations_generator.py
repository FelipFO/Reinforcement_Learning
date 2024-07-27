import numpy as np


class FormationsGenerator:
    """
    This class is used to get the leader agent reference position and its followers deltas matrices.
    This class handles only 5 agents, further work is needed.
    """
    def __init__(self, num_agents, leader_target_x=175, leader_target_y=120, dx=10, dy=10):
        """

        :param num_agents: Number of agents (in this moment this variable is not used)
        :param leader_target_x: Leader target x position
        :param leader_target_y: Leader target y position
        :param dx: scale factor for the follower deltas in the x axis
        :param dy: scale factor for the follower deltas in the y axis
        """
        self.num_agents = num_agents
        self.leader_target_x = leader_target_x
        self.leader_target_y = leader_target_y
        self.dx = dx
        self.dy = dy

    def set_leader_target_position(self, leader_x, leader_y):
        self.leader_target_x = leader_x
        self.leader_target_y = leader_y

    def scale_deltas(self, deltas):
        scaled_deltas = np.zeros_like(deltas)
        scaled_deltas[0, :] = self.dx*deltas[0, :]
        scaled_deltas[1, :] = self.dy*deltas[1, :]
        return scaled_deltas

    def get_vertical_line_formation(self):
        #self.leader_target_y = 140
        follower_deltas = np.array([[0, 0, 0, 0],
                                    [2, -2, 4, -4],
                                    [0, 0, 0, 0]])
        leader_reference = np.array([self.leader_target_x, self.leader_target_y, 0])
        return leader_reference, self.scale_deltas(follower_deltas)

    def get_triangle_formation(self):
        #self.leader_target_y = 120
        follower_deltas = np.array([[2, -2, 4, -4],
                                    [2, 2, 4, 4],
                                    [0, 0, 0, 0]])
        leader_reference = np.array([self.leader_target_x, self.leader_target_y, 0])
        return leader_reference, self.scale_deltas(follower_deltas)

    def get_pentagon_formation(self):
        #self.leader_target_y = 90
        follower_deltas = np.array([[4, -4, 2, -2],
                                    [2, 2, 5, 5],
                                    [0, 0, 0, 0]])
        leader_reference = np.array([self.leader_target_x, self.leader_target_y, 0])
        return leader_reference, self.scale_deltas(follower_deltas)

    def get_formation(self, formation_name):
        """

        :param formation_name: The name of the target formation
        :return: tuple(leader_reference, follower_deltas)
            leader_reference: numpy.array [target_x, target_y, target_theta]
            follower_deltas:  numpy.array with shape 3x(num_agents-1) where the ith 3x1 vector
                              contains [delta_x, delta_y, delta_theta] for the ith agent.
        """
        if formation_name == "vertical_line":
            return self.get_vertical_line_formation()
        elif formation_name == "triangle":
            return self.get_triangle_formation()
        elif formation_name == "pentagon":
            return self.get_pentagon_formation()
        return None
