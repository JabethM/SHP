import numpy as np


class Objects:
    time = 0
    dt = 0.1
    length = None

    def __init__(self, velocity, position, mass, length=None, name=None):
        self.velocity = velocity
        self.position = position % Objects.length  # cls.length might not be set yet
        self.mass = mass
        self.momentum = self.compute_mom()
        if Objects.length is None:
            Objects.length = length
        self.name = name
        self.radius = 0

    def set_dt(self, new_dt):
        self.dt = new_dt
        return

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity
        return

    def get_velocity(self):
        vel = self.velocity
        return vel

    def set_position(self, new_position):
        self.position = new_position % Objects.length
        return

    def get_position(self):
        pos = self.position
        return pos

    def compute_mom(self):
        mom = self.mass * self.velocity
        return mom

    def get_mass(self):
        mass = self.mass
        return mass

    def get_momentum(self):
        mom = self.momentum
        return mom

    def update_mom(self):
        self.momentum = self.compute_mom()
        return

    def calc_new_velocity(self, other: 'Objects'):
        new_vel = (self.velocity * (self.mass - other.mass) + 2 * other.mass * other.velocity) / (
                self.mass + other.mass)

        return new_vel

    @staticmethod
    def update_time(time):
        Objects.time += time
        return

    def update_position(self, delta_time):
        v = self.velocity * delta_time
        self.set_position(self.velocity * delta_time + self.position)
        return self.get_position()
