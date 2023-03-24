import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

total_mom = [[], [], []]
mom_over_time = [[], [], []]
times = [[], [], []]
x = np.arange(0, 1000, 1)
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
    if line == ">->->\n":
        line = f.readline()
        line = f.readline()
        while line != "<-<-<\n":
            pos = line.split(' = ')[1]
            pos = int(pos.split('\n')[0])

            line = f.readline()
            ts = process_text(line)

            line = f.readline()
            press = process_text(line)

            times[count].append(ts)
            mom_over_time[count].append(press)
            line = f.readline()

            total_mom[count].append(press[-1])
        count += 1
    line = f.readline()

fig = plt.figure()
ax = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

A = np.array(list(map(float, total_mom[0])))
B = np.array(list(map(float, total_mom[1])))
C = np.array(list(map(float, total_mom[2])))

ax.plot(x, (A + B + C), label='Total')
ax.plot(x, A, label='A', color='r')
ax.plot(x, B, label='B', color='g')
ax.plot(x, C, label='C', color='b')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
ax.set_xlabel('Position')
ax.set_ylabel('Total Momentum')

pressure = [[], [], []]
for p in range(len(mom_over_time)):

    for w in range(len(mom_over_time[p])):
        i = times[p][w]
        j = mom_over_time[p][w]
        if len(mom_over_time[p][w]) <= 5:
            i.insert(0, 0)
            j.insert(0, 0)
        slope, intercept, r_value, p_value, std_err = stats.linregress(i, j)
        pressure[p].append(slope)

pa = np.array(pressure[0])
pb = np.array(pressure[1])
pc = np.array(pressure[2])
pa[np.isnan(pa)] = 0
pb[np.isnan(pb)] = 0
pc[np.isnan(pc)] = 0

ptot = pa + pb + pc

ax2.plot(x, pa + pb + pc, label='Total')
ax2.plot(x, pressure[0], label='A', color='r')
ax2.plot(x, pressure[1], label='B', color='g')
ax2.plot(x, pressure[2], label='C', color='b')

ax2.set_xlabel('Position')
ax2.set_ylabel('Pressure')

ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()
