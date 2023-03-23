import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

total_mom = [[], [], []]
mom_over_time = [[], [], []]
times = [[], [], []]
walls = np.arange(0, 1000, 10)
t_size = 0
f = open("pressure-data.txt", "r")
line = f.readline()
count = 0


def process_text(current_line):
    data = current_line.split('[')[1]
    data = data.split(']')[0]
    data = data.split(', ')

    if data == ['']:
        data = ['0']
    data = list(map(float, data))
    return data


while line != "------\n":
    if line[0] == 'P':
        for i in range(3):
            line = f.readline()
            mom = line.split(' : ')[1]
            mom = mom.split('\n')[0]
            total_mom[i].append(mom)
    if line == ">->->\n":
        line = f.readline()
        line = f.readline()
        while line != "<-<-<\n":
            pos = int(line.split('\n')[0]) // 10

            line = f.readline()
            ts = process_text(line)

            line = f.readline()
            press = process_text(line)

            times[count].append(ts)
            mom_over_time[count].append(press)
            line = f.readline()
        count += 1
    line = f.readline()

fig = plt.figure()
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

A = np.array(list(map(float, total_mom[0])))
B = np.array(list(map(float, total_mom[1])))
C = np.array(list(map(float, total_mom[2])))
ax.plot(walls, (A + B + C), label='Total')
ax.plot(walls, A, label='A', color='r')
ax.plot(walls, B, label='B', color='g')
ax.plot(walls, C, label='C', color='b')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.set_xlabel('Position')
ax.set_ylabel('Total Momentum')

pressure = [[], [], []]
for p in range(len(mom_over_time)):

    for w in range(len(mom_over_time[p])):
        x = times[p][w]
        y = mom_over_time[p][w]
        if len(mom_over_time[p][w]) <= 5:
            x.insert(0, 0)
            y.insert(0, 0)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        pressure[p].append(slope)

pa = np.array(pressure[0])
pb = np.array(pressure[1])
pc = np.array(pressure[2])
pa[np.isnan(pa)] = 0
pb[np.isnan(pb)] = 0
pc[np.isnan(pc)] = 0

ptot = pa + pb + pc

ax2.plot(walls, pa + pb + pc, label='Total')
ax2.plot(walls, pressure[0], label='A', color='r')
ax2.plot(walls, pressure[1], label='B', color='g')
ax2.plot(walls, pressure[2], label='C', color='b')

ax2.set_xlabel('Position')
ax2.set_ylabel('Pressure')

ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()
