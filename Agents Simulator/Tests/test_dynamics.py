import numpy as np
from Agents.agents import Agents
from Controllers.dt_dsd import DTDSD
from Formations.formations_generator import FormationsGenerator


num_agents = 5
simulation_steps = 100
formation_name = "vertical_line"
adjacency_matrix = np.array([[0., 1., 0., 0., 0.],
                             [1., 0., 1., 0., 0.],
                             [0., 1., 0., 1., 0.],
                             [0., 0., 1., 0., 1.],
                             [0., 0., 0., 1., 0.]])

agents = Agents(num_agents)

# Create controller and add adjacency matrix
gammas = [agents.max_x, agents.max_y]
epsilons = [(1 - 1e-3)*1/(2*gammas[0]), (1 - 1e-3)*1/(2*gammas[1])]
controller = DTDSD(num_robots=num_agents, num_populations=2, epsilon=epsilons, gamma=gammas)
controller.set_adjacency_matrix(adjacency_matrix)

# Generate desired formation
formation_generator = FormationsGenerator(num_agents=num_agents, leader_target_x=60, leader_target_y=130)
leader_reference, followers_deltas = formation_generator.get_formation(formation_name)

# Set initial positions
# initial_positions = np.array([[40., 50., 60., 70., 30.],
#                               [40., 40., 40., 40., 40.],
#                               [0.,  0.,  0.,  0.,  0.]])
initial_positions = np.array([[60., 120., 180., 240., 300.],
                                   [130., 130., 130., 130., 130.],
                                   [0., 0., 0., 0., 0.]])
# initial reset
agents.reset(initial_positions=initial_positions)
x0 = agents.agents_positions[:2, :].copy()
x0[:, 0] = num_agents*np.array(gammas)
controller.reset(x0=x0.reshape(-1))

for sim_steps in range(simulation_steps):
    print(agents.agents_positions)
    leader_position = agents.agents_positions[:2, 0].reshape(2, 1)
    controller_input = np.hstack((-leader_position, followers_deltas[:2, :]))
    references = controller.step(controller_input).reshape(2, num_agents)
    # reset leader reference
    references[:, 0] = leader_reference[:2]
    # add angle zeros
    references = np.vstack((references, np.zeros((1, num_agents))))
    agents.step(references)
