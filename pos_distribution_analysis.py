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
            distribution = distribution.split("]")[0]
            distribution = distribution.split(" ")
            distribution = list(filter(lambda a: a != '', distribution))

            p = list(map(float, distribution))
            p = list(map(int, p))
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
Pa = Pa / np.sum(Pa)

Pb = np.array(pos_placements[1])
Pb = Pb / np.sum(Pb)

Pc = np.array(pos_placements[2])
Pc = Pc / np.sum(Pc)

####

ma = np.array(pre_placements[0])
ma = ma / np.sum(ma)

mb = np.array(pre_placements[1])
mb = mb / np.sum(mb)

mc = np.array(pre_placements[2])
mc = mc / np.sum(mc)
fig = plt.figure()
ax = fig.add_subplot(311)
ax2 = fig.add_subplot(313)


ax.plot(x, Pa, label='A', color='r')
ax.plot(x, Pb, label='B', color='g')
ax.plot(x, Pc, label='C', color='b')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.set_xlabel('Position')
ax.set_ylabel('Distribution')

ax2.plot(x, ma, label='A', color='r')
ax2.plot(x, mb, label='B', color='g')
ax2.plot(x, mc, label='C', color='b')
ax2.plot(x, (ma + mb + mc), label='total')
ax2.set_xlabel('Position')
ax2.set_ylabel('Momentum Distribution')

plt.show()
