import matplotlib.pyplot as plt
import numpy as np

placements = []

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
            placements.append(p)
    line = f.readline()

x = np.arange(len(placements[0]))

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(x, placements[0], label='A')
ax.plot(x, placements[1], label='B')
ax.plot(x, placements[2], label='C')
ax.legend()
ax.set_xlabel('Position')
ax.set_ylabel('Distribution')
plt.show()