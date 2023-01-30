import numpy


class Particles:
    """
    Units for particles:
    Time - s
    Position - m
    Velocity - m/s
    mass - kg
    momentum - kg * m/s
    """
    time = 0
    length = None

    def __init__(self, velocity, position, mass, length=None, name=None):
        self.velocity = velocity
        self.position = position % Particles.length  # cls.length might not be set yet
        self.mass = mass
        self.momentum = self.compute_mom()
        if Particles.length is None:
            Particles.length = length
        self.name = name
        self.radius = Particles.length / 200

    def compute_mom(self):
        mom = self.mass * self.velocity
        return mom

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity
        return

    def get_velocity(self):
        vel = self.velocity
        return vel

    def set_position(self, new_position):
        self.position = new_position % Particles.length
        return

    def get_position(self):
        pos = self.position
        return pos

    def get_mass(self):
        mass = self.mass
        return mass

    def get_momentum(self):
        mom = self.momentum
        return mom

    @staticmethod
    def update_time(time):
        Particles.time += time
        return

    def update_position(self, delta_time):
        self.set_position(round(self.velocity * delta_time + self.position, 7))
        return self.get_position()

    def calc_new_velocity(self, other: 'Particles'):
        new_vel = (self.velocity * (self.mass - other.mass) + 2 * other.mass * other.velocity) / (
                self.mass + other.mass)

        return new_vel

    def update_mom(self):
        self.momentum = self.compute_mom()
        return
