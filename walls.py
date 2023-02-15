from objects import Objects


class Walls(Objects):

    def __init__(self, velocity, position, mass, length=None, name=None):
        super().__init__(velocity, position, mass, length, name)
        self.velocity = 0
        self.mass = 0
        self.pressure = 0
        self.p_time = Objects.time

    def calc_new_velocity(self, other):

        self.calc_pressure(other.momentum)
        return 0

    def calc_pressure(self, mom):
        if Objects.time >= self.p_time + 10 * Objects.dt:
            self.p_time = Objects.time
            self.pressure = 0
        self.pressure += mom
        return self.pressure

