import copy
import numpy as np


class Tanker:
    """
    Esta clase implementa el modelo dinamico del Tanker
    """
    def __init__(self, mode, initial_conditions=4000, integration_step=1):
        """
        Constructor de la clase
        :param mode: Modo del Tanker ("full", "ballast")
        :param initial_conditions: Condiciones iniciales del sistema
        :param integration_step: Paso de integracion requerido por el metodo runge kutta
        """
        assert mode in ["ballast", "full"], "Tanker mode should be 'ballast' or 'full'"
        self.mode = mode
        self.x = np.array(initial_conditions)
        self.step = integration_step
        self.a, self.b, self.c, self.d = self.init_parameters()
        self.sim_time = 0

    def init_parameters(self):
        """
        Metodo para inicializar los parametros del tanker basado en el modo de operacion
        indicado por el usuario.
        El computo de los parametros a, b, c y d se realiza de la manera descrita  en la pagina
        120 del libro de Kevin.
        :return: parametros a, b, c y d
        """
        ell, u = 350, 5
        if self.mode == "ballast":
            k_0 = 5.88
            tau_10 = -16.91
            tau_20 = 0.45
            tau_30 = 1.43
        else:
            k_0 = 0.83
            tau_10 = -2.88
            tau_20 = 0.38
            tau_30 = 1.07

        k = k_0 * (u / ell)
        tau_1 = tau_10 * (ell / u)
        tau_2 = tau_20 * (ell / u)
        tau_3 = tau_30 * (ell / u)

        a = ((1/tau_1)+(1/tau_2))
        b = (1/(tau_1*tau_2))
        c = (k*tau_3/(tau_1*tau_2))
        d = k/(tau_1*tau_2)
        return a, b, c, d

    def compute_runge_kutta_step(self, x, rudder_input):
        """
        Este metodo computa un paso un paso del metodo de runge kutta
        Utilizando las ecuaciones descritas en las paginas 119 y 121 del libro de Kevin.
        :param x: Estado actual del sistema
        :param rudder_input: Señal de control
        :return: nuevo estado del sistema.
        """
        ks = list()
        x_new = copy.deepcopy(x)
        for it in range(4):
            k = self.step*np.array([[x_new[1]],
                                    [x_new[2] + self.c*rudder_input],
                                    [-self.a*(x_new[2] + self.c*rudder_input) - self.b*(x_new[1]**3 + x_new[1]) +
                                     self.d*rudder_input]]).flatten()
            ks.append(k)
            if it < 2:
                x_new = x_new + k/2
            else:
                x_new = x_new + k
        return x + (1/6)*(ks[0]+2*ks[1]+2*ks[2]+ks[3])

    def reset(self):
        """
        Metodo para reiniciar el tiempo de simulacion.
        :return:
        """
        self.sim_time = 0

    def run_step(self, rudder_input):
        """
        Metodo usado por el simulador para obtener el nuevo estado del sistema de acuerdo
        a la accion de control rudder input
        :param rudder_input: Señal de control
        :return: Nuevo estado del sistema
        """
        if self.sim_time == 0:
            self.x[2] = -self.c*rudder_input
        self.x = self.compute_runge_kutta_step(self.x, rudder_input)
        self.sim_time += 1
        return self.x


