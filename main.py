from particles import Particles
import numpy as np


class run:

    def __init__(self, length, a_params, b_params, c_params):
        Particles.length = length
        self.A = Particles(*a_params)
        self.B = Particles(*b_params)
        self.C = Particles(*c_params)
        self.system = [self.A, self.B, self.C]

    def t_t_collision(self, part1: Particles, part2: Particles):
        """
        Time Until Collision
        :param part1:
        :param part2:
        :return:
        """
        delta_vel = part1.velocity - part2.velocity
        delta_dist = (np.sign([delta_vel])[0] * (part2.position - part1.position)) % Particles.length
        # delta_dist calculates which distance to use based on the difference in velocity
        if delta_vel == 0:
            return float('inf')

        time = delta_dist / delta_vel
        return time

    def update_values(self, time):
        Particles.update_time(time)

        # TODO: update new velocities based on the particles that collided and their new mom
        return

    def loop(self):
        for t in range(10):

            collisions = [self.t_t_collision(self.system[i], self.system[j]) for i in range(3) for j in range(i+1, 3)]

            next_coll = np.argmin(collisions)
            self.update_values(collisions[next_coll])

        return


def main():
    l = 1000
    A = (12, 100, 10)
    B = (15, 50, 2)
    C = (-5, 25, 15)
    run(l, A, B, C)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
