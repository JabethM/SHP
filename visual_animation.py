import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib;
import random
import numpy as np

from objects import Objects

matplotlib.use("TkAgg")
import main

from particles import Particles

# The time step for the animation.
dt = 0.005
tMax = 100000
time_bool = False


def get_pos(t=0):
    sim.collection_point = 5
    while t < tMax:
        if time_bool:
            t += dt
            system = sim.system_positions(dt)
        else:
            system = sim.collision_approach(t)
            t = sim.system[0].time

        yield system[0].position, system[1].position, system[2].position


def init():
    ax.set_xlim(0, Particles.length)
    ax.set_ylim(-25 * 5, 25 * 5)  # sim.system[0].radius, 25 * sim.system[0].radius)
    ax.set_xlabel('$x$ /m')

    for i in range(len(balls)):
        balls[i].set_center((sim.system[i].position, 0))

    return balls


def animate(pos: [Particles]):
    x1, x2, x3 = pos
    balls[0].set_center((x1, 0))
    balls[1].set_center((x2, 0))
    balls[2].set_center((x3, 0))

    max_pressure = 1

    for i in range(len(lines)):
        lines[i].set_data(tracked_walls[i].time_list, tracked_walls[i].p_list)

        if tracked_walls[i].p_list[-1] > max_pressure:
            max_pressure = tracked_walls[i].p_list[-1]

    ax2.set_xlim(left=0, right=Objects.time + 0.05 * Objects.time)
    ax2.set_ylim(bottom=0, top=max_pressure + 0.05 * max_pressure)

    return balls, lines


####
# Set System Parameters
def rand_num():
    return np.random.random() * 100


def rand_set():
    return np.array([rand_num(), rand_num(), rand_num()])


length = 1000  # Length
m = rand_set() / 4
p = rand_set() * 10

v = 5
cap = v * 10
vel1 = (rand_num() * v) - cap / 2
vel2 = (rand_num() * v) - cap / 2
vel3 = -((m[0]) * vel1 + (m[1]) * vel2) / (m[2])
# vel3 = (rand_num() * v) - cap/2


A = (vel1, p[0], m[0])  # Velocity, Position and Mass
B = (vel2, p[1], (m[1]))
C = (vel3, p[2], (m[2]))

#A = (1812.6016608790178, 927.5484672569775, 18.35534448320567)
#B = (-1793.1840137378058, 252.5447347729187, 2.4032484234453784)
#C = (-1219.9488340806695, 862.5709287074595, 23.73989829182229)

A = (436.6755201473969, 942.037726682613, 0.023102833093793795)
B = (445.72750775754014, 251.88894735099854, 19.104199940935114)
C = (-802.187982013197, 354.98571547290226, 10.627628511259113)


total_mom = A[0] * A[2] + B[0] * B[2] + C[0] * C[2]

print("A = " + str(A))
print("B = " + str(B))
print("C = " + str(C))
print("Mom = " + str(total_mom))

W = range(0, 1000, 10)
sim = main.ring(length, A, B, C, W)  # Create the system
####

fig = plt.figure()
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax.set_aspect('equal')

# These are the objects we need to keep track of.
balls = [plt.Circle((sim.system[i].position, i), radius=5)  # sim.system[i].radius)
         for i in range(3)]
balls[0].set_color('r')
balls[1].set_color('g')
balls[2].set_color('b')

tracked_walls = []
for w in sim.W:
    if w.position % 100 == 0:
        tracked_walls.append(w)

lines = [ax2.plot(w.time_list, w.p_list, label="x = " + str(w.position))[0] for w in tracked_walls]

for i in range(len(balls)):
    balls[i].set_label("m = " + str(round(sim.system[i].mass)))
    ax.add_patch(balls[i])

interval = 1000 * dt
ani = animation.FuncAnimation(fig, animate, get_pos,
                              interval=interval, repeat=False, init_func=init)

legend1 = ax.legend(prop={'size': 6}, loc='center left', bbox_to_anchor=(1, 0.5))
legend2 = ax2.legend(prop={'size': 6}, loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
