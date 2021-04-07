DELTA_GRAV = []
DELTA_GRAV_GRAPH = []
graph_x = []
# Earth Rad = 6371.009
# Earth Grav acc at sea level = 9.80665 m/s²

hl = int(input('Enter lowest number in range of heights to calculate: '))
hh = int(input('Enter highest number in range of heights to calculate: '))
hr = range(hl, hh)

DELTA_GRAV.extend(hr)

r = float(input('Enter radius of body: '))
g = float(input('Enter gravitational acceleration at sea level: '))

for i in range(hl, hh):
    #DELTA_GRAV_GRAPH.append(float(g * ((r / r + i) ** 2)))
    bottom = r + i
    ins_per = r / bottom
    part_2 = ins_per ** 2
    grav = g * part_2
    DELTA_GRAV_GRAPH.append(grav)
    graph_x.append(i)

import matplotlib.pyplot as plt

plt.plot(graph_x, DELTA_GRAV_GRAPH)
plt.savefig("Gravity Graph", dpi=400)