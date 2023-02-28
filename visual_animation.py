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
tMax = 1000


def get_pos(t=0):
    while t < tMax:
        t += dt
        system = sim.system_positions(dt)

        yield system[0].position, system[1].position, system[2].position


def init():
    ax.set_xlim(0, Particles.length)
    ax.set_ylim(-25 * sim.system[0].radius, 25 * sim.system[0].radius)
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
        lines[i].set_data(sim.W[i].time_list, sim.W[i].p_list)

        if sim.W[i].p_list[-1] > max_pressure:
            max_pressure = sim.W[i].p_list[-1]

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

v = 25
cap = v * 100
vel1 = (rand_num() * v) - cap / 2
vel2 = (rand_num() * v) - cap / 2
vel3 = -(m[0] * vel1 + m[1] * vel2) / m[2]
# vel3 = (rand_num() * v) - cap/2


# A = (vel1, p[0], m[0])  # Velocity, Position and Mass
# B = (vel2, p[1], m[1])
# C = (vel3, p[2], m[2])

A = (500, 10, 200)
B = (10, 300, 1)
C = (-500,-300, 200)


W = [0, 333, 666]
sim = main.run(length, A, B, C, W)  # Create the system
####

fig = plt.figure()
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax.set_aspect('equal')

# These are the objects we need to keep track of.
balls = [plt.Circle((sim.system[i].position, i), radius=sim.system[i].radius)
         for i in range(3)]
balls[0].set_color('r')
balls[1].set_color('g')
balls[2].set_color('b')

lines = [ax2.plot(w.time_list, w.p_list, label="x = " + str(w.position))[0] for w in sim.W]

for i in range(len(balls)):
    balls[i].set_label("m = " + str(round(sim.system[i].mass)))
    ax.add_patch(balls[i])

interval = 1000 * dt
ani = animation.FuncAnimation(fig, animate, get_pos,
                              interval=interval, repeat=False, init_func=init)

legend1 = ax.legend(prop={'size': 6}, loc='center left', bbox_to_anchor=(1, 0.5))
legend2 = ax2.legend(prop={'size': 6}, loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()
