import itertools
import numpy as np
import matplotlib.pyplot as plt


class RBFNetwork:
    """
    Esta clase implementa un controlador tipo red Neuronal RBF
    """
    def __init__(self, sampling_interval):
        """
        Constructor de la clase
        Inicializa los parametros de la red neuronal como se describe en
        la pagina 134 del libro de Kevin
        :param sampling_interval:
        """
        self.sampling_interval = sampling_interval
        n_partitions = 11
        self.sigma_e = 0.7 * (np.pi / n_partitions)
        self.sigma_c = 0.7 * (0.02 / n_partitions)
        self.last_error = 0
        # Computo de los centros
        self.centers = list(itertools.product(np.linspace(-np.pi / 2, np.pi / 2, n_partitions),
                                         np.linspace(-0.01, 0.01, n_partitions)))
        temp = np.linspace(-(n_partitions - 1) / 2, (n_partitions - 1) / 2, n_partitions)
        self.b = np.zeros((n_partitions, n_partitions))
        # Computo de los parametros b. Pagina 136
        for i in range(n_partitions):
            for j in range(n_partitions):
                self.b[i][j] = -((1 / 10) * (200 * (np.pi / 180)) * temp[i] +
                                 (1 / 10) * (200 * (np.pi / 180)) * temp[j])
                self.b[i][j] = np.maximum(-80 * (np.pi / 180), np.minimum(80 * (np.pi / 180), self.b[i][j]))
        self.b = self.b.T.flatten().reshape(-1, 1)

    def get_model_output(self, error, d_error):
        """
        Metodo para obtener la salida del controlador.
        Este metodo computa la salida como se explica en el libro de Kevin pagina 123
        :param error:
        :param d_error:
        :return:
        """
        activations = list()
        for (e_c, c_c) in self.centers:
            activations.append(np.exp(-(((error - e_c) ** 2) / self.sigma_e ** 2) -
                                      (((d_error - c_c) ** 2) / self.sigma_c ** 2)))
        activations = np.array(activations).reshape(-1, 1)
        return float(self.b.T.dot(activations))

    def predict(self, reference, angle):
        """
        Metodo para obtener la salida del controlador.
        Este metodo computa la salida como se explica en el libro de Kevin pagina 133
        :param reference: Referencia del controlador (\Psi_r en el libro)
        :param angle: Angulo actual del sistema (\Psi en el libro)
        :return: Salida del controlador
        """
        error = reference - angle
        d_error = (error - self.last_error)/self.sampling_interval
        self.last_error = error

        return self.get_model_output(error, d_error)

    def plot_in_out_map(self):
        """
        Este metodo grafica el mapeo entre entrada y salida del controlador
        Página 137 del libro de kevin.
        :return:
        """
        e, d_e = np.meshgrid(np.arange(-95*(np.pi/180), 95*(np.pi/180), 190*(np.pi/180)/50),
                             np.arange(-0.00999, 0.00999, 0.02/50))
        output = np.array([self.get_model_output(error, d_error) for (error, d_error) in zip(e.flatten(), d_e.flatten())])
        output = output.reshape(e.shape)

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_wireframe(e*(180/np.pi), d_e*(180/np.pi), output*(180 / np.pi), color="gray", linewidth=1)
        plt.xlabel(f"Heading error [deg]")
        plt.ylabel(f"Change in heading error [deg]")
        ax.set_zlabel(r'Controller output $\delta$ [deg]')
        plt.show()