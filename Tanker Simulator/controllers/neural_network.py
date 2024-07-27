import numpy as np
import matplotlib.pyplot as plt


class NeuralNetwork:
    """
    Esta clase implementa un controlador tipo Red Neuronal
    """
    def __init__(self):
        """
        Constructor de la clase
        Inicializa los parametros de la red neuronal como se describe en
        la pagina 124 del libro de Kevin
        """
        self.w112 = self.w122 = 10
        self.b12 = -200 * np.pi / 180
        self.b22 = +200 * np.pi / 180

        self.w113 = -80 * np.pi / 180
        self.w223 = -80 * np.pi / 180
        self.b13 = 0
        self.b23 = 80 * np.pi / 180

    def predict(self, reference, angle):
        """
        Metodo para obtener la salida del controlador.
        Este metodo computa la salida como se explica en el libro de Kevin pagina 123
        :param reference: Referencia del controlador (\Psi_r en el libro)
        :param angle: Angulo actual del sistema (\Psi en el libro)
        :return: Salida del controlador.
        """
        error = reference - angle
        x_bar_1 = self.b12 + self.w112 * error
        x_bar_2 = self.b22 + self.w122 * error
        x11 = 1 / (1 + np.exp(-x_bar_1))
        x21 = 1 / (1 + np.exp(-x_bar_2))
        return self.b13 + self.w113 * x11 + self.b23 + self.w223 * x21

    def plot_in_out_map(self):
        """
        Este metodo grafica el mapeo entre entrada y salida del controlador
        Página 126 del libro de kevin.
        :return:
        """
        x, y = np.meshgrid(np.arange(-100, 100, 0.2), np.arange(-100, 100, 0.2))
        output = self.predict(x.flatten()*np.pi/180, y.flatten()*np.pi/180).reshape(x.shape)
        output *= (180/np.pi)

        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_wireframe(x, y, output, color="gray", linewidth=1)
        plt.xlabel(f"Reference input $\Psi_r$ deg.")
        plt.ylabel(f"Heading angle $\Psi$ deg.")
        ax.set_zlabel(r'Controller output $\delta$ deg.')
        plt.show()
