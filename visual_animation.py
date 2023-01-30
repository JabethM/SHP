import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib;

matplotlib.use("TkAgg")
import main

from particles import Particles

# The time step for the animation.
dt = 0.005
tMax = 1000

l = 100
A = (3, 100, 10)
B = (2, 50, 2)
C = (-1, 25, 15)
sim = main.run(l, A, B, C)


def get_pos(t=0):

    while t < tMax:
        t += dt
        system = sim.system_positions(t, dt)
        for i in system:
            print(i.position)
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
    balls[0].set_center((x1,0))
    balls[1].set_center((x2,0))
    balls[2].set_center((x3,0))
    return balls[0], balls[1], balls[2]


fig, ax = plt.subplots()
ax.set_aspect('equal')

# These are the objects we need to keep track of.
balls = [plt.Circle((sim.system[i].position, i), radius=sim.system[i].radius, color='r') for i in range(3)]

ax.add_patch(balls[0])
ax.add_patch(balls[1])
ax.add_patch(balls[2])

xdata, ydata = [], []

interval = 1000 * dt
ani = animation.FuncAnimation(fig, animate, get_pos, blit=True,
                              interval=interval, repeat=False, init_func=init)
plt.show()
