import matplotlib.pyplot as plt
import numpy as np

pos_placements = []
pre_placements = []
f = open("position_distribution.txt", "r")
line = f.readline()
while line != "------\n":
    if line == "######\n":
        for i in range(3):
            line = f.readline()
            distribution = line.split("[")[1]
            distribution = distribution.split(".]")[0]
            distribution = distribution.split(". ")

            p = list(map(int, distribution))
            pos_placements.append(p)
    elif line == "###########\n":
        for i in range(3):
            line = f.readline()
            distribution = line.split("[")[1]
            distribution = distribution.split("]")[0]
            distribution = distribution.split(" ")

            distribution = list(filter(lambda a: a != '', distribution))
            p = list(map(lambda q: abs(float(q)), distribution))
            pre_placements.append(p)

    line = f.readline()

x = np.arange(len(pos_placements[0]))

Pa = np.array(pos_placements[0])
Pb = np.array(pos_placements[1])
Pc = np.array(pos_placements[2])

ma = np.array(pre_placements[0])
mb = np.array(pre_placements[1])
mc = np.array(pre_placements[2])

fig = plt.figure()
ax = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

ax.plot(x, pos_placements[0], label='A')
ax.plot(x, pos_placements[1], label='B')
ax.plot(x, pos_placements[2], label='C')
ax.legend()
ax.set_xlabel('Position')
ax.set_ylabel('Distribution')

ax2.plot(x, (Pa + Pb + Pc))
ax2.set_xlabel('Position')
ax2.set_ylabel('Total Position Distribution')


ax3.plot(x, (ma + mb + mc))
ax3.set_xlabel('Position')
ax3.set_ylabel('Momentum Distribution')

plt.show()
