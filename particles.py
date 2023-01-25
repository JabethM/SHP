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

    def __init__(self, velocity, position, mass, length=None):
        self.velocity = velocity
        self.position = position % Particles.length  # cls.length might not be set yet
        self.mass = mass
        self.momentum = self.compute_mom()

        if Particles.length is None:
            Particles.length = length

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
        self.set_position(self.velocity * delta_time)
        return self.get_position()

