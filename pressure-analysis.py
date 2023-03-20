import numpy as np

positions = []
data = []
t_size = 0
f = open("pressure-data.txt", "r")
line = f.readline()
while line != "------\n":
    if line[0] == "t" or line[0] == "p":
        s = line.split("[")
        s = s[1][:-2]
        s = s.split(", ")

        q = list(map(float, s))
        data.append(q)

        if line[0] == "t":
            t_size = len(s)

    elif line[0] == "P":
        s = line.split(" - ")
        positions.append(int((s[1])[:-1]))

    line = f.readline()
#print(data)

for i in data:
    print(len(i))
