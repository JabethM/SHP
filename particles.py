from multipledispatch import dispatch
import numpy as np

from walls import Walls
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
        self.increments = 1
        self.pos_distribution = np.zeros(int(Objects.length // self.increments) - 1)

    def calc_new_velocity(self, other: 'Objects'):
        if isinstance(other, Walls):
            return self.velocity
        else:
            new_vel = super().calc_new_velocity(other)
        return new_vel

    def update_position(self, delta_time):
        p = super().update_position(delta_time)

        p_shifted = np.roll(self.pos_distribution, 5 - int(p))
        p_shifted[:11] += 1
        self.pos_distribution = np.roll(p_shifted, int(p) - 5)

