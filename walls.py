from objects import Objects


class Walls(Objects):

    def __init__(self, velocity, position, mass, length=None, name=None):
        super().__init__(velocity, position, mass, length, name)
        self.velocity = 0
        self.mass = 0
        self.pressure = 0
        self.p_time = Objects.time
        self.other = None

    def calc_new_velocity(self, other):

        self.calc_pressure(other.momentum, other)
        return 0

    def calc_pressure(self, mom, other):

        self.pressure += abs(mom)
        print(self.pressure)
        self.other = other

        return self.pressure

