from particles import Particles
import numpy as np
from objects import Objects
from walls import Walls


class run:

    def __init__(self, length, a_params, b_params, c_params, w_params=None):
        self.diagram = None
        Objects.length = length
        self.A = Particles(*a_params, name="A")
        self.B = Particles(*b_params, name="B")
        self.C = Particles(*c_params, name="C")
        self.system = [self.A, self.B, self.C]
        self.consMom = sum([i.momentum for i in self.system])
        self.consE = sum([0.5 * i.mass * (i.velocity ** 2) for i in self.system])
        self.update_diagram()

        self.W = None
        if w_params is not None:
            self.W = Walls(*w_params, name="W")
            self.system.append(self.W)

    def t_t_collision(self, part1: Objects, part2: Objects):
        """
        Time Until Collision
        :param part1:
        :param part2:
        :return:
        """

        delta_vel = part1.velocity - part2.velocity
        a = np.sign([delta_vel])[0]
        b = (part2.position - part1.position)
        c = (a * b) % Objects.length
        d = (part1.radius + part2.radius)
        delta_dist = c - d
        # delta_dist calculates which distance to use based on the difference in velocity
        if delta_vel == 0:
            return float('inf')

        time = delta_dist / abs(delta_vel)
        return time

    def update_values(self, time, part1_idx, part2_idx):

        part1 = self.system[part1_idx]
        part2 = self.system[part2_idx]

        for part in self.system:
            part.update_position(time)

        part1_vel = part1.calc_new_velocity(part2)
        part2_vel = part2.calc_new_velocity(part1)

        part1.set_velocity(part1_vel)
        part2.set_velocity(part2_vel)

        part1.update_mom()
        part2.update_mom()

        # Objects.update_time(0.000005)
        # for part in self.system:
        #    part.update_position(0.000005)
        return

    def update_diagram(self):
        self.diagram = ["."] * Objects.length
        self.diagram[round(self.A.position) % Particles.length] = "A"
        self.diagram[round(self.B.position) % Particles.length] = "B"
        self.diagram[round(self.C.position) % Particles.length] = "C"
        return

    def pos_sort(self, part: Particles):
        return part.position

    def detect_next_collision(self):
        collisions = [(self.t_t_collision(self.system[i], self.system[j]), i, j, (isinstance(self.system[i], Walls)
                                                                                  or isinstance(self.system[j], Walls)))
                      for i in range(len(self.system))
                      for j in range(i + 1, len(self.system))]
        times = [x[0] for x in collisions]
        next_coll = np.argmin(times)

        return collisions[next_coll]

    def collision_approach(self):
        events = []
        for t in range(1000):
            collision_info = self.detect_next_collision()

            self.update_values(*collision_info)
            self.update_diagram()
            # print("".join(self.diagram))

            events.append(collision_info)

        return

    def system_positions(self, t, dt):
        Objects.update_time(dt)
        collision_info = self.detect_next_collision()
        next_coll_time = collision_info[0]

        if t + dt >= t + next_coll_time or (next_coll_time < 0):
            c = collision_info[1:]
            self.update_values(dt, *collision_info[1:-1])
        else:
            for part in self.system:
                # Objects.update_time(idx)
                part.update_position(dt)

        self.update_diagram()
        # print(self.consMom, self.consE)
        o = 2 * (collision_info[1] + collision_info[2]) % 3
        # print(self.system[o].name)

        return self.system

    def time_approach(self, dt, end):
        t = 0
        while Objects.time <= end:
            self.system_positions(t, dt)
            t += dt
            Objects.time = t

        return


def main():
    ####
    # Set System Parameters
    length = 1000  # Length
    A = (0, 100, 150)  # Velocity, Position and Mass
    B = (-1, -700, 1)
    C = (-2, -100, 150)
    W = (0, 0, 0)
    sim = run(length, A, B, C)  # Create the system
    ####
    # sim.collision_approach()
    sim.time_approach(0.1, 10000)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
