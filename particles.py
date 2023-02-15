from multipledispatch import dispatch
import numpy as np

from Walls import Walls
from objects import Objects


def sigmoid(x):
    sig = 25 * (1 / (1 + np.exp(-0.1 * x))) + 2.5
    return sig


class Particles(Objects):
    """
    Units for particles:
    Time - s
    Position - m
    Velocity - m/s
    mass - kg
    momentum - kg * m/s
    """

    def __init__(self, velocity, position, mass, length=None, name=None):
        super().__init__(velocity, position, mass, length, name)
        # self.velocity = velocity
        # self.position = position % Particles.length  # cls.length might not be set yet

        # if Particles.length is None:
        #    Particles.length = length
        # self.name = name
        self.radius = (Objects.length / 200)  # * sigmoid(np.sqrt(self.mass))


