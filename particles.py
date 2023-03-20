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
        self.pos_distribution = np.zeros(int(Objects.length // self.increments))
        self.pressure_distribution = np.zeros(int(Objects.length // self.increments))

    def calc_new_velocity(self, other: 'Objects'):
        if isinstance(other, Walls):
            return self.velocity
        else:
            new_vel = super().calc_new_velocity(other)
        return new_vel

    def update_position(self, delta_time):
        p = super().update_position(delta_time)

        pos_shifted = np.roll(self.pos_distribution, 5 - int(p))
        pos_shifted[:11] += 1
        self.pos_distribution = np.roll(pos_shifted, int(p) - 5)

        pre_shifted = np.roll(self.pressure_distribution, 5 - int(p))
        pre_shifted[:11] += self.momentum
        self.pressure_distribution = np.roll(pre_shifted, int(p) - 5)
        """
        num_test = int(p)
        num = (int(p) + np.sign(self.velocity) * 5) % Objects.length
        self.pressure_distribution[int(num)] += self.momentum
        """


