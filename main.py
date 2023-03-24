from particles import Particles
import numpy as np
from objects import Objects
from walls import Walls
import math


class ring:

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
                w.idx = i
                self.system.append(w)
                self.W.append(w)

            for p in self.P:
                p.init_wall_pressure(len(self.W))
        self.last = None

        self.end = False
        self.noAnim = False
        self.CApproach = False
        self.collection_point = 10

    def update_data_distributions(self, v, x_old, x_new, m_old):
        dv = np.sign(v)
        for i in range(3):
            part = self.P[i]
            dist = self.dist_travelled(dv[i], x_old[i], x_new[i], 0, 0)
            t = [self.t_t_collision(v1=v[i], v2=0, p1=x_old[i], p2=t_idx, r1=part.radius, r2=0) + Objects.time
                 for t_idx in range(Objects.length)]

            if dv[i] > 0:
                start = math.ceil((x_old[i]) % Objects.length + part.radius)
                end = math.floor(x_old[i] + dist + part.radius) + 1  # Don't want to double count radius

                if start == end:
                    continue

                test = part.pos_distribution
                pos_shifted = np.roll(part.pos_distribution, -start)
                pos_shifted[:(end - start)] += 1
                self.P[i].pos_distribution = np.roll(pos_shifted, start)
                test = self.P[i].pos_distribution

                pres_shifted = np.roll(part.pressure_distribution, -start)
                pres_shifted[:(end - start)] += abs(m_old[i])
                self.P[i].pressure_distribution = np.roll(pres_shifted, start)

            else:
                start = (math.floor(x_old[i] - part.radius)) % Objects.length
                end = math.ceil(x_old[i] - dist - part.radius) - 1

                if start == end:
                    continue

                test = part.pos_distribution
                pos_shifted = np.roll(part.pos_distribution, -start)
                pos_shifted[(end - start):] += 1
                self.P[i].pos_distribution = np.roll(pos_shifted, start)

                pres_shifted = np.roll(part.pressure_distribution, -start)
                pres_shifted[(end - start):] += abs(m_old[i])
                self.P[i].pressure_distribution = np.roll(pres_shifted, start)
                test = self.P[i].pos_distribution
            inc = int(dv[i])

            for j in range(start, end, int(dv[i])):

                t_val = t[j % Objects.length]
                if not self.P[i].wall_pressure_efficient[j % Objects.length]:
                    self.P[i].wall_pressure_efficient[j % Objects.length].append((abs(m_old[i]), t[j % Objects.length]))
                else:
                    mom = abs(m_old[i]) + self.P[i].wall_pressure_efficient[(j % Objects.length)][-1][0]
                    self.P[i].wall_pressure_efficient[j % Objects.length].append((mom, t[j % Objects.length]))

            dummy = 2

    def dist_travelled(self, dv, pos1, pos2, r1, r2):
        a = np.sign([dv])[0]
        b = pos2 - pos1
        c = (a * b) % Objects.length
        d = (r1 + r2)
        delta_dist = c - d
        return delta_dist

    def t_t_collision(self, part1=None, part2=None, v1=0, v2=0, p1=0, p2=0, r1=0, r2=0):
        if part1 is not None and part2 is not None:
            v1 = part1.velocity
            p1 = part1.position
            r1 = part1.radius

            v2 = part2.velocity
            p2 = part2.position
            r2 = part2.radius

        delta_vel = v1 - v2
        delta_dist = self.dist_travelled(delta_vel, p1, p2, r1, r2)
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

        for part in self.P:
            part.update_position(nt)
        for w in self.W:
            w.update_position(Objects.time + nt)

        cE = sum([0.5 * i.mass * (i.velocity ** 2) for i in self.system])
        part1.set_velocity(part1_vel)
        part2.set_velocity(part2_vel)
        cE = sum([0.5 * i.mass * (i.velocity ** 2) for i in self.system])

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
        times = np.array(times)
        # next_coll = np.argmin(times)
        next_coll = int(np.where(times == np.min(times[np.nonzero(times)]))[0])

        if self.W is not None:
            wall_collisions = collisions[3:]

        return next_coll, ball_collisions, wall_collisions

    def collision_approach(self, t):
        Objects.CApproach = True
        events = []

        next_idx, p_collisions, w_collisions = self.detect_next_collision()
        next_ball = p_collisions[next_idx]

        if not self.noAnim:
            for w in w_collisions:
                if next_ball[0] >= w[0] >= 0:
                    # a = Objects.time + w[0]
                    # b = self.system[w[2]].time_list
                    self.system[w[2]].update_position(Objects.time + w[0])
                    other = self.system[w[1]]
                    # mom = other.momentum
                    self.system[w[2]].calc_pressure(other.momentum, other, w[0] + Objects.time)

        v_old = [p.velocity for p in self.P]
        x_old = [p.position for p in self.P]
        m_old = [p.momentum for p in self.P]
        self.update_values(*next_ball)

        x_new = [p.position for p in self.P]
        self.update_data_distributions(v_old, x_old, x_new, m_old)

        Objects.update_time(next_ball[0])
        print(Objects.time)
        if Objects.time >= self.collection_point and not self.write:
            self.export_pressure()
            self.export_pos_dist()
            self.write = True
            self.end = True

        return self.system

    def system_positions(self, dt):
        Objects.CApproach = False
        next_idx, p_collisions, w_collisions = self.detect_next_collision()
        next_coll = p_collisions[next_idx]
        nt = next_coll[0]
        collision_occurred = False

        last_collision_condition = (next_coll[0] == self.last or next_coll[1] == self.last)
        if Objects.time + dt >= Objects.time + nt and (not next_coll[-1] or nt > 0):
            self.update_values(*next_coll)
            collision_occurred = True
            dt = nt

        for i in range(len(w_collisions)):
            current = w_collisions[i]
            nt = current[0]
            if Objects.time + dt >= Objects.time + nt and nt > 0:
                self.system[current[2]].update_position(Objects.time)
                self.system[current[2]].calc_new_velocity(self.system[current[1]])

        if not collision_occurred:
            for part in self.P:
                part.update_position(dt)
            for w in self.W:
                w.update_position(Objects.time)

        self.update_diagram()
        print(Objects.time)
        t = Objects.update_time(dt)

        if Objects.time >= self.collection_point and not self.write:
            self.export_pressure()
            self.export_pos_dist()
            self.write = True
            self.end = True
        # o = 2 * (collision_info[1] + collision_info[2]) % 3
        # print(self.system[o].name)
        # print(sum([i.momentum for i in self.system]), sum([0.5 * i.mass * (i.velocity ** 2) for i in self.system]))
        return self.system

    def export_pressure(self):
        with open('pressure-data.txt', 'w') as f:
            f.write("#####\n")
            f.write("init conditions: \n")
            for p in self.P:
                f.write(p.name + ": (v=" + str(p.velocity) + ", p=" + str(p.position) + ", m=" + str(p.mass) + ")\n")
            f.write("########\n")

            for p in self.P:
                f.write(">->->\n")
                f.write("Wall pressure contributions of " + p.name + "\n")

                if self.noAnim:
                    wall_data = p.wall_pressure_efficient
                else:
                    wall_data = p.wall_pressure

                for i in range(len(wall_data)):
                    f.write("position = " + str(i) + "\n")

                    ts = [wp[1] for wp in wall_data[i]]
                    ms = [wp[0] for wp in wall_data[i]]
                    f.write("> Time: " + str(ts) + "\n")
                    f.write("> Pressure: " + str(ms) + "\n")
                f.write("<-<-<\n")
            f.write("------\n")
            f.close()
        return

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

    def run(self, dt, end, c_approach):
        t = 0
        self.collection_point = 500
        self.CApproach = c_approach
        while Objects.time <= end:
            if self.CApproach:
                system = self.collision_approach(t)
                t = self.system[0].time
            else:
                self.system_positions(dt)
                t += dt

            if self.noAnim and self.end:
                break
        return


def main():
    ####
    # Set System Parameters
    length = 1000  # Length
    v = 50
    cap = v * 100

    def rand_num():
        return np.random.random() * 100

    def rand_set():
        return np.array([rand_num(), rand_num(), rand_num()])

    m = rand_set() / 4
    p = rand_set() * 10

    vel1 = (rand_num() * v) - cap / 2
    vel2 = (rand_num() * v) - cap / 2
    vel3 = -((m[0]) * vel1 + (m[1]) * vel2) / (m[2])

    A = (vel1, p[0], m[0])  # Velocity, Position and Mass
    B = (vel2, p[1], (m[1]))
    C = (vel3, p[2], (m[2]))

    A = (436.6755201473969, 942.037726682613, 0.023102833093793795)
    B = (445.72750775754014, 251.88894735099854, 19.104199940935114)
    C = (-802.187982013197, 354.98571547290226, 10.627628511259113)

    W = range(0, 1000, 10)
    sim = ring(length, A, B, C, W)  # Create the system
    sim.noAnim = True
    ####
    # sim.collision_approach()
    sim.run(0.005, 10000, True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
