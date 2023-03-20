from objects import Objects


class Walls(Objects):

    def __init__(self, velocity, position, mass, length=None, name=None):
        super().__init__(velocity, position, mass, length, name)
        self.velocity = 0
        self.mass = 0
        self.pressure = 0
        self.time_list = [0]
        self.p_list = [0]
        self.other = None
        self.a = 0
        self.b = 0
        self.c = 0

    def calc_new_velocity(self, other):
        self.calc_pressure(other.momentum, other)
        return 0

    def calc_pressure(self, mom, other):
        self.pressure += abs(mom)

        self.p_list.append(self.pressure)
        self.time_list.append(self.time)
        if other.name == 'A':
            self.a += self.pressure
        elif other.name == 'B':
            self.b += self.pressure
        elif other.name == 'C':
            self.c += self.pressure
        else:
            print("ERROR")
            
        return self.pressure

    def update_position(self, delta_time):
        self.time_list.append(self.time)
        self.p_list.append(self.pressure)
        return self.get_position()
