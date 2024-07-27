import numpy as np
from PyQt5 import QtGui

def map_angles(angles):
    """
    Maps from [0, 2pi] to [-pi, pi]
    :param angles:
    :return: mapped angles
    """

    return ((angles + np.pi) % (2 * np.pi)) - np.pi


def demap_angles(angles):
    """
    Maps from [-pi, pi] to [0, 2pi]
    :param angles:
    :return: mapped angles
    """

    return (2 * np.pi + angles) * (angles < 0) + angles * (angles >= 0)


def get_agent_colors():
    agents_colors = {0: QtGui.QColor(255, 186, 1), # Amarillo
                     1: QtGui.QColor(253, 86, 2),  # Naranja
                     2: QtGui.QColor(182, 75, 120),# Morado
                     3: QtGui.QColor(53, 214, 237),# Azul
                     4: QtGui.QColor(166, 214, 9)} # Verde
    return agents_colors
