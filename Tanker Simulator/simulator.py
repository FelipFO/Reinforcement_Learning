import utils
import numpy as np
from tanker.tanker import Tanker
from controllers.rbf_network import RBFNetwork
from controllers.neural_network import NeuralNetwork


# Se declaran los parametros de la simulación
mode = "ballast"  # full ballast
ctrl_name = "nn"  # "rbf" or "nn"
simulation_steps = 4000
sampling_interval = 10
initial_conditions = [0, 0, 0]

# Se valida que el controlador seleccionado por el usuario sea un controlador valido
assert ctrl_name in ["rbf", "nn"], "Controller name must be rbf or nn"
# Se instancia el controlador correspondiente y se grafica su mapeo de entradas y salidas
if ctrl_name == "nn":
    controller = NeuralNetwork()
else:
    controller = RBFNetwork(sampling_interval)
controller.plot_in_out_map()

# Se instancia el objeto del tanker
tanker = Tanker(mode, initial_conditions)

# Se definen los valores iniciales para la referencia, entrada al sistema (rudder input)
# y para el sistema
reference, rudder_input = 45 * (np.pi / 180), 0
x_0 = initial_conditions[0]

psi, refs, rudder_hist = list(), list(), list()

# Se inicia la simulacion por la cantidad de pasos indicada por el usuario.
# Cada vez que se cumpla un periodo de muestreo (i % sampling_interval == 0)
# se utiliza el controlador para obtener la nueva entrada del sistema (rudder_input).
# Al llegar al paso de simulation 2000 cambiamos la referencia del controlador.
# En cada instante de simulacion actualizamos el estado del sistema usando el objeto tanker.
# Finalmente, guardamos las variables utilizadas para graficarlas mas adelante.
for i in range(simulation_steps):

    if i % sampling_interval == 0:
        rudder_input = controller.predict(reference, x_0)
    if i == 2000:
        reference = 0
    x_0 = tanker.run_step(rudder_input)[0]

    psi.append(x_0*180/np.pi)
    refs.append(reference * 180 / np.pi)
    rudder_hist.append(rudder_input*(180/np.pi))

utils.plot_hist(psi, refs, rudder_hist)
