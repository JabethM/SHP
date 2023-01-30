from particles import Particles
import numpy as np


class run:

    def __init__(self, length, a_params, b_params, c_params):
        self.diagram = None
        Particles.length = length
        self.A = Particles(*a_params, name="A")
        self.B = Particles(*b_params, name="B")
        self.C = Particles(*c_params, name="C")
        self.system = [self.A, self.B, self.C]
        self.update_diagram()

    def t_t_collision(self, part1: Particles, part2: Particles):
        """
        Time Until Collision
        :param part1:
        :param part2:
        :return:
        """
        delta_vel = part1.velocity - part2.velocity
        delta_dist = (np.sign([delta_vel])[0] * (part2.position - part1.position)) % Particles.length - 2 * part1.radius
        # delta_dist calculates which distance to use based on the difference in velocity
        if delta_vel == 0:
            return float('inf')

        time = delta_dist / abs(delta_vel)
        return time

    def update_values(self, time, part1_idx, part2_idx):
        Particles.update_time(time)
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

        Particles.update_time(0.000005)
        for part in self.system:
            part.update_position(0.000005)
        return

    def update_diagram(self):
        self.diagram = ["."] * Particles.length
        self.diagram[round(self.A.position) % Particles.length] = "A"
        self.diagram[round(self.B.position) % Particles.length] = "B"
        self.diagram[round(self.C.position) % Particles.length] = "C"
        return

    def pos_sort(self, part: Particles):
        return part.position

    def collision_approach(self):
        events = []
        for t in range(1000):
            collisions = [(self.t_t_collision(self.system[i], self.system[j]), i, j) for i in range(len(self.system))
                          for j in range(i + 1, len(self.system))]
            times = [x[0] for x in collisions]
            next_coll = np.argmin(times)
            self.update_values(*collisions[next_coll])
            self.update_diagram()
            print("".join(self.diagram))
            """positions = [i for i in self.system]
            positions.sort(key=self.pos_sort)
            pos = [i.name for i in positions]
            # print(pos)

            x = "".join(pos)
            if x != "CBA" and x != "ACB" and x != "BAC":
                print("FAIL")
                break
            else:
                print("success")

            # """

            # print("Colliding: " + str(collisions[next_coll]))

            events.append(collisions[next_coll])

        """for e in range(1, len(events)):
            if (events[e][1], events[e][2]) == (events[e - 1][1], events[e - 1][2]):
                print("ERROR at: " + str(e))
                break
            else:
                print("SUCCESS")
"""
        return


def main():
    l = 100
    A = (12, 100, 10)
    B = (15, 50, 2)
    C = (-5, 25, 15)
    sim = run(l, A, B, C)
    sim.collision_approach()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
