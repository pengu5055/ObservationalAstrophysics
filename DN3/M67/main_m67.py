import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr


def absolute_mag(mag, dist):
    """
    Calculate absolute magnitude from distance and apparent magnitude
    :param mag: apparent magnitude
    :param dist: distance to cluster in pc
    :return: absolute magnitude
    """
    return mag + 5 - 5*np.log10(dist)


def process_tables(t1, t2, dist):
    BV = []
    V_mag = []
    for i in range(np.shape(t1)[1]):
        if t1[0, i] == t2[0, i]:
            BV.append(t1[3, i] - t2[3, i])
            V_mag.append(absolute_mag(t2[3, i], dist))

    return np.array(BV), np.array(V_mag)


c1, c2, c3 = cmr.take_cmap_colors("cmr.bubblegum", 3, return_fmt="hex")

# Data format: ID,XC,YC,MAG,MERR

b_data = np.column_stack(np.genfromtxt("b.dat"))
v_data = np.column_stack(np.genfromtxt("v.dat"))

M67_dist = 850

x, y = process_tables(b_data, v_data, M67_dist)

fig, ax = plt.subplots()
plt.scatter(x, y, s=1, c=c2)

plt.title("HR Diagram for M67")
plt.xlabel(r"$B - V$")
plt.ylabel(r"$M_V$")
ax.invert_yaxis()
plt.show()




