from objects import Objects
import numpy as np


class Walls(Objects):

    def __init__(self, velocity, position, mass, length=None, name=None):
        super().__init__(velocity, position, mass, length, name)
        self.velocity = 0
        self.mass = 0
        self.pressure = 0
        self.time_list = [0]
        self.p_list = [0]
        self.other = None
        self.part_mom = np.zeros(3)
        self.idx = 0

    def calc_new_velocity(self, other):
        self.calc_pressure(other.momentum, other)
        return 0

    def calc_pressure(self, mom, other):
        self.pressure += abs(mom)

        self.p_list.append(self.pressure)
        self.time_list.append(self.time)

        if other.name == 'A':
            self.part_mom[0] += self.pressure
        elif other.name == 'B':
            self.part_mom[1] += self.pressure
        elif other.name == 'C':
            self.part_mom[2] += self.pressure
        else:
            print("ERROR")

        other.wall_pressure[self.idx].append((self.pressure, Objects.time))

        return self.pressure

    def update_position(self, delta_time):
        self.time_list.append(self.time)
        self.p_list.append(self.pressure)
        return self.get_position()
