from particles import Particles
import numpy as np
from objects import Objects
from walls import Walls


class run:

    def __init__(self, length, a_params, b_params, c_params, w_positions=None):
        self.write = False
        self.diagram = None
        Objects.length = length
        self.A = Particles(*a_params, name="A")
        self.B = Particles(*b_params, name="B")
        self.C = Particles(*c_params, name="C")
        self.system = [self.A, self.B, self.C]
        self.consMom = sum([i.momentum for i in self.system])
        self.consE = sum([0.5 * i.mass * (i.velocity ** 2) for i in self.system])
        self.update_diagram()

        self.debug_count = 0
        self.P = self.system[:3]
        self.W = None
        if w_positions is not None:
            self.W = []
            for i in range(len(w_positions)):
                w = Walls(0, w_positions[i], 0, name="W" + str(i))
                self.system.append(w)
                self.W.append(w)

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

    def update_values(self, nt, part1_idx, part2_idx, is_wall):

        part1 = self.system[part1_idx]
        part2 = self.system[part2_idx]

        part1_vel = part1.calc_new_velocity(part2)
        part2_vel = part2.calc_new_velocity(part1)

        for part in self.system:
            part.update_position(nt)

        part1.set_velocity(part1_vel)
        part2.set_velocity(part2_vel)

        part1.update_mom()
        part2.update_mom()

        return

    def update_diagram(self):
        self.diagram = ["."] * Objects.length
        self.diagram[round(self.A.position) % Particles.length] = "A"
        self.diagram[round(self.B.position) % Particles.length] = "B"
        self.diagram[round(self.C.position) % Particles.length] = "C"
        return

    def detect_next_collision(self, dt=0):
        arbitrary_num = len(self.P)

        collisions = [(self.t_t_collision(self.system[i], self.system[j]), i, j, (isinstance(self.system[i], Walls)
                                                                                  or isinstance(self.system[j], Walls)))
                      for i in range(len(self.system))
                      for j in range(i + 1, len(self.system))]

        collisions = sorted(collisions, key=(lambda x: x[1] + x[2] * arbitrary_num if x[-1] else x[1] + x[2]))
        ball_collisions = sorted(collisions[:3], key=(lambda x: x[0]))
        wall_collisions = []

        times = [x[0] for x in ball_collisions]
        next_coll = np.argmin(times)

        if self.W is not None:
            wall_collisions = collisions[3:]

        return next_coll, ball_collisions, wall_collisions

    def collision_approach(self):
        events = []
        for t in range(1000):
            collision_info = self.detect_next_collision()

            self.update_values(*collision_info)
            self.update_diagram()

            events.append(collision_info)
        return

    def system_positions(self, dt):

        next_idx, p_collisions, w_collisions = self.detect_next_collision()
        next_coll = p_collisions[next_idx]
        nt = next_coll[0]
        collision_occurred = False

        if Objects.time + dt >= Objects.time + nt and (not next_coll[-1] or nt > 0):
            self.update_values(*next_coll)
            collision_occurred = True
            dt = nt

        for i in range(len(w_collisions)):
            current = w_collisions[i]
            nt = current[0]
            if Objects.time + dt >= Objects.time + nt and nt > 0:
                self.system[current[2]].update_position(nt)
                self.system[current[2]].calc_new_velocity(self.system[current[1]])

        if not collision_occurred:
            for part in self.system:
                part.update_position(dt)

        self.update_diagram()
        # print(self.consMom, self.consE)
        t = Objects.update_time(dt)

        if Objects.time >= 50 and not self.write:
            self.export_pressure()
            self.export_pos_dist()
            self.write = True
        # o = 2 * (collision_info[1] + collision_info[2]) % 3
        # print(self.system[o].name)

        return self.system

    def export_pressure(self):
        with open('pressure-data.txt', 'w') as f:

            f.write("#######\n")
            f.write("init conditions: \n")
            for p in self.P:
                f.write(p.name + ": (v=" + str(p.velocity) + ", p=" + str(p.position) + ", m=" + str(p.mass) + ")\n")
            f.write("#######\n")
            f.write("Time:\n")
            f.write("t = " + str(self.W[0].time_list) + "\n")
            for w in self.W:
                f.write("Position - " + str(w.position) + "\n")
                f.write("p = " + str(w.p_list))
                f.write('\n')
            f.write("------\n")
            f.close()

    def export_pos_dist(self):
        with open('position_distribution.txt', 'w') as f:
            f.write("#######\n")
            f.write("Length = " + str(Objects.length) + "\n")
            f.write("Distribution Increments = " + str(self.A.increments) + "\n")

            f.write("Init conditions: \n")
            for p in self.P:
                f.write(p.name + ": (v=" + str(p.velocity) + ", p=" + str(p.position) + ", m=" + str(p.mass) + ")\n")

            f.write("######\n")
            for p in self.P:
                f.write(
                    "" + str(p.name) + " pos_dist = " + np.array_str(p.pos_distribution, max_line_width=1000000) + "\n")

            f.write("###########\n")
            for p in self.P:
                f.write("" + str(p.name) + " pressure_dist = " + np.array_str(p.pressure_distribution,
                                                                              max_line_width=1000000) + "\n")

            f.write("------\n")
            f.close()

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
