import utils
import numpy as np


class Agents:

    def __init__(self, num_agents):
        self.num_agents = num_agents
        # Set maximum lineal velocity [cm/s] and angular velocity [rad/s]
        self.max_v = 15
        self.max_w = 7
        # Set maximum x and y positions [cm]
        self.max_x = 351
        self.max_y = 241
        # Set agent diameter [cm]
        self.diameter = 12
        # Set simulation limits
        self.lim_x = self.max_x - 0.5 * self.diameter
        self.lim_y = self.max_y - 0.5 * self.diameter
        # Set simulation parameters
        self.dt_sys = 0.1  # s
        self.n_runs = 10
        self._dt_sim = self.dt_sys / self.n_runs
        # Auxiliar identity matrix
        self.identity = np.eye(self.num_agents)
        self.identity_comp = np.ones((self.num_agents, self.num_agents)) - self.identity

        # Set controller parameters
        self.kp_v = 2
        self.kp_w = 2
        self.distance_margin = 0.5

        # For rendering
        self._window = None
        self._render_landmarks = True
        # agent_positions and controller landmarks variables
        self.agents_positions = None
        self.landmarks = None
        self.reset()

    def set_poses(self, positions):
        positions = np.array(positions)
        assert positions.shape[0] == 3 and positions.shape[1] == self.num_agents, \
            "ERROR: Input poses must have shape (3, n)."
        self.agents_positions = positions

    def set_landmarks(self, landmarks):
        assert landmarks.shape[0] == 3 and landmarks.shape[1] == self.num_agents, \
            "ERROR: Input landmarks must have shape (3, n)."
        self.landmarks = landmarks

    def check_collisions(self):
        dx = (self.agents_positions[0, :].reshape(-1, 1) - self.agents_positions[0, :]).T
        dy = (self.agents_positions[1, :].reshape(-1, 1) - self.agents_positions[1, :]).T
        inter_robot_distances = np.sqrt(np.square(dx) + np.square(dy))
        inter_robot_angles = np.arctan2(dy, dx)
        overlaps = self.diameter - np.minimum(inter_robot_distances + self.diameter * self.identity, self.diameter)
        collisions = False if np.max(overlaps) == 0 else True
        return collisions, overlaps, inter_robot_distances, inter_robot_angles

    def resolve_collisions(self):
        collisions, overlaps, _, inter_robot_angles = self.check_collisions()
        if collisions:
            dx = np.sum(0.5 * overlaps * np.cos(inter_robot_angles), axis=1)
            dy = np.sum(0.5 * overlaps * np.sin(inter_robot_angles), axis=1)
            self.agents_positions[0, :] = np.clip(self.agents_positions[0, :] - dx, 0.5 * self.diameter, self.lim_x)
            self.agents_positions[1, :] = np.clip(self.agents_positions[1, :] - dy, 0.5 * self.diameter, self.lim_y)

    def reset(self, initial_positions=None, initial_landmarks=None):

        if initial_positions is None:
            self.agents_positions = np.zeros((3, self.num_agents))
            self.agents_positions[0, :] = np.random.random(self.num_agents) * \
                                          (self.lim_x - 0.5 * self.diameter) + 0.5 * self.diameter
            self.agents_positions[1, :] = np.random.random(self.num_agents) * \
                                          (self.lim_y - 0.5 * self.diameter) + 0.5 * self.diameter
            self.agents_positions[2, :] = np.random.random(self.num_agents) * 2 * np.pi
        else:
            self.set_poses(initial_positions)

        if initial_landmarks is None:
            self.landmarks = np.zeros_like(self.agents_positions)
            self.landmarks[0, :] = np.random.random(self.num_agents) * \
                                   (self.lim_x - 0.5 * self.diameter) + 0.5 * self.diameter
            self.landmarks[1, :] = np.random.random(self.num_agents) * (
                    self.lim_y - 0.5 * self.diameter) + 0.5 * self.diameter
            self.landmarks[2, :] = np.random.random(self.num_agents) * 2 * np.pi
        else:
            self.set_landmarks(initial_landmarks)

        self.resolve_collisions()
        return self.agents_positions, self.landmarks

    def compute_low_level_control(self):
        dxs = self.landmarks[0, :] - self.agents_positions[0, :]
        dys = self.landmarks[1, :] - self.agents_positions[1, :]
        distances = np.sqrt(np.square(dxs) + np.square(dys))
        angles = utils.demap_angles(np.arctan2(dys, dxs))
        mask = (distances >= self.distance_margin).astype(float)
        vs = self.kp_v*distances * mask
        ws = self.kp_w*utils.map_angles(angles - self.agents_positions[2, :]) * mask
        return vs, ws

    def dynamics(self, v, w):
        for i in range(self.n_runs):
            self.agents_positions[0, :] = np.clip(self.agents_positions[0, :] +
                                                  self._dt_sim * v * np.cos(self.agents_positions[2, :]),
                                                  0.5*self.diameter, self.lim_x)
            self.agents_positions[1, :] = np.clip(self.agents_positions[1, :] +
                                                  self._dt_sim * v * np.sin(self.agents_positions[2, :]),
                                                  0.5*self.diameter, self.lim_y)
            self.agents_positions[2, :] = (self.agents_positions[2, :] + self._dt_sim * w) % (2*np.pi)
            self.resolve_collisions()

    def step(self, references):
        self.set_landmarks(references)
        v, w = self.compute_low_level_control()
        v = np.clip(v, -self.max_v, self.max_v)
        w = np.clip(w, -self.max_w, self.max_w)
        self.dynamics(v, w)
        return self.agents_positions, self.landmarks
