import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib;
import random
import numpy as np

matplotlib.use("TkAgg")
import main

from particles import Particles

# The time step for the animation.
dt = 0.005
tMax = 1000


def get_pos(t=0):
    while t < tMax:
        t += dt
        system = sim.system_positions(t, dt)

        yield system[0].position, system[1].position, system[2].position


def init():
    ax.set_xlim(0, Particles.length)
    ax.set_ylim(-25 * sim.system[0].radius, 25 * sim.system[0].radius)
    ax.set_xlabel('$x$ /m')

    for i in range(len(balls)):
        balls[i].set_center((sim.system[i].position, 0))

    return balls[0], balls[1], balls[2]


def animate(pos: [Particles]):

    x1, x2, x3 = pos
    balls[0].set_center((x1, 0))
    balls[1].set_center((x2, 0))
    balls[2].set_center((x3, 0))
    #l = legend
    #legend.remove()

    for i in range(len(balls)):
        lab = "m = " + str(round(sim.system[i].mass)) + ", v = " + str(round(sim.system[i].velocity))
    #    legend.get_texts()[i].set_text(lab)
    #ax.legend()
    return balls[0], balls[1], balls[2]


####
# Set System Parameters
length = 1000  # Length
vel1 = np.random.random() * 400
vel2 = np.random.random() * -400
m1 = np.random.random() * 50
m2 = np.random.random() * 50
m3 = 10
vel3 = -(m1 * vel1 + m2 * vel2) / m3

A = (400, 100, 50)  # Velocity, Position and Mass
B = (-200, -100, 30)
C = (10, -500, 10)

W = (0, 0, 0)
sim = main.run(length, A, B, C, W)  # Create the system
####

fig, ax = plt.subplots()
ax.set_aspect('equal')

# These are the objects we need to keep track of.
balls = [plt.Circle((sim.system[i].position, i), radius=sim.system[i].radius)
         for i in range(3)]
balls[0].set_color('r')
balls[1].set_color('g')
balls[2].set_color('b')

for i in range(len(balls)):
    balls[i].set_label("m = " + str(round(sim.system[i].mass)) + ", initial v = " + str(round(sim.system[i].velocity)))
    ax.add_patch(balls[i])


interval = 1000 * dt
ani = animation.FuncAnimation(fig, animate, get_pos, blit=True,
                              interval=interval, repeat=False, init_func=init)
#legend = ax.legend(prop={'size': 6})
plt.show()
