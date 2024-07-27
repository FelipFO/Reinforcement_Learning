# Code for the discrete-time distributed Smith dynamics (with saturation)
# Code by: Juan Martinez-Piazuelo

import numpy as np


# Discrete-time Distributed Smith Dynamics (with saturation)
class DTDSD:

    def __init__(self, num_robots=2, num_populations=1, epsilon=[0.1], gamma=[140]):
        self._nr = np.maximum(num_robots, 2)
        self._np = np.maximum(num_populations, 1)
        self._n = self._nr*self._np

        # ERROR CHECKING
        epsilon, gamma = self.error_checker(epsilon, gamma)

        # Step-size matrix and gamma matrix
        diagonal = []
        gamma_matrix = np.zeros((self._n, self._n))
        for i in range(self._np):
            diagonal += [epsilon[i]] # Set this entry to 0 in order to use mass-varying dynamics (not used in IFAC paper)
            diagonal += [epsilon[i]]*(self._nr - 1)
            gamma_matrix[i*self._nr:(i+1)*self._nr, i*self._nr:(i+1)*self._nr] = gamma[i]

        self._epsilon_matrix = np.diag(diagonal).astype(float)
        self._gamma_matrix = gamma_matrix.astype(float)

        # Useful pre-computations
        self._normalizer_matrix = np.kron(np.eye(self._np), np.ones(self._nr))
        self._h_matrix = -np.eye(self._n)
        self._h_matrix[np.arange(self._np)*self._nr, np.arange(self._np)*self._nr] = 0.0

        self.set_adjacency_matrix()
        self.reset(silent=True)

    def observe(self):
        return self._x.copy()

    def reset(self, x0=None, scales=None, silent=False):
        if x0 is None:
            if scales is None:
                self._x = np.random.random(self._n)
            else:
                scaler = (np.ones(self._np) * (np.array(scales).reshape(self._np, 1))).reshape(self._n)
                self._x = np.random.random(self._n) * scaler
        else:
            assert x0.shape[0] == self._n, "ERROR: the x0 array must be of shape (num_robots*num_pops,)."
            self._x = x0.copy()

        if not silent:
            return self.observe()

    def step(self, external_signals): # external_signals must be a matrix with shape (num_pops, num_robots).
        self.set_fitness_vector(external_signals)   # Must be called before set_laplacian_matrix() (for smith dynamics)
        self.set_laplacian_matrix()                                        # Must be called after set_fitness_vector()
        self._x = self._x + np.dot(self._epsilon_matrix, np.dot(self._laplacian_matrix, self._fitness_vector))
        return self.observe()

    def set_fitness_vector(self, external_signals):
        _, self._fitness_vector = self.compute_potential_and_fitness_functions(self._x, external_signals)

    def set_laplacian_matrix(self):
        delta_fitness = self._fitness_vector.reshape(-1, 1) - self._fitness_vector
        idxs = np.where(abs(delta_fitness) > self._gamma_matrix)
        phi_matrix = np.ones((self._n, self._n))
        phi_matrix[idxs] = self._gamma_matrix[idxs]/abs(delta_fitness[idxs])
        sign_delta_fitness = np.sign(delta_fitness)
        positive_terms = np.maximum(sign_delta_fitness, 0) * self._x
        negative_terms = np.minimum(sign_delta_fitness, 0) * (self._x.reshape(-1, 1))
        modulated_adjacency = np.clip(positive_terms - negative_terms, -self._gamma_matrix, self._gamma_matrix)*self._adjacency_matrix*phi_matrix
        modulated_degree = np.diag(np.sum(modulated_adjacency, 1))
        self._laplacian_matrix = modulated_degree - modulated_adjacency

    def set_adjacency_matrix(self, adjacency_matrix=None):
        if adjacency_matrix is None:
            adj_matrix = np.ones((self._nr, self._nr)) - np.eye(self._nr) # By default use complete graph (full information)
        else:
            adj_matrix = adjacency_matrix.reshape(self._nr, self._nr)

        adj_matrix = np.clip(adj_matrix - np.eye(self._nr), 0, 1)      # Ensure diagonal is not included
        self._adjacency_matrix = np.kron(np.eye(self._np), adj_matrix) # Extended adjacency for multi-population cases

    def compute_potential_and_fitness_functions(self, x, external_signals):
        # Must return an array of shape (num_robots*num_pops,)
        x_in = np.reshape(x, (-1, 1))   # Force x to be a column vector
        fitness = np.dot(self._h_matrix, x_in) + external_signals.reshape(self._n, 1)
        return None, fitness.reshape(self._n)

    def error_checker(self, epsilon, gamma):
        if (not isinstance(epsilon, list) and not isinstance(epsilon, np.ndarray)):
            epsilon = [epsilon]
        if (not isinstance(gamma, list) and not isinstance(gamma, np.ndarray)):
            gamma = [gamma]

        assert np.array(epsilon).shape[0] <= self._np, "ERROR: the number of epsilon parameters provided is greater than num_populations."
        assert np.array(gamma).shape[0] <= self._np, "ERROR: the number of gamma parameters provided is greater than num_populations."

        if (np.array(epsilon).shape[0] < self._np):
            print('Using same epsilon for all populations. Provide a list of epsilons if you want a different epsilon for each population.')
            epsilon = [epsilon[0]]*self._np
        if (np.array(gamma).shape[0] < self._np):
            print('Using same gamma for all populations. Provide a list of gammas if you want a different gamma for each population.')
            gamma = [gamma[0]]*self._np

        return epsilon, gamma

    def close(self):
        pass
