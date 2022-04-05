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


def apparent_mag(mag, dist):
    return 5*np.log10(dist) + 5 + mag


def process_tables(t1, t2, dist):
    BV = []
    V_mag = []
    index = []
    c = 0
    for i in range(np.shape(t1)[1] - 1):
        if t1[0, i] == t2[0, i]:
            index.append(int(c))
            BV.append(t1[3, i] - t2[3, i])
            V_mag.append(absolute_mag(t2[3, i], dist))
        c += 1

    return np.array(BV), np.array(V_mag), np.array(index)


def ellipse(u, v, x, y, a, b):
    """ Checks if (u, v) data point is in ellipse with center (x, y) and half axes a and b"""
    output = []
    n = len(u)
    for i in range(n):
        if ((u[i] - x) ** 2)/a**2 + ((v[i] - y) ** 2)/b**2 <= 1:
            output.append(i)

    return np.array(output)


c1, c2, c3 = cmr.take_cmap_colors("cmr.guppy", 3, cmap_range=(0.1, 0.9), return_fmt="hex")

# Data format: ID,XC,YC,MAG,MERR
M67_dist = 850
b_data = np.column_stack(np.genfromtxt("b.dat"))
v_data = np.column_stack(np.genfromtxt("v.dat"))

b_iso, v_iso = np.column_stack(np.genfromtxt("iso-1e10.txt", usecols=(29, 30)))
iso_b_app = apparent_mag(b_iso, M67_dist)
iso_v_app = apparent_mag(v_iso, M67_dist)

b_iso1, v_iso1 = np.column_stack(np.genfromtxt("iso-4e9.txt", usecols=(29, 30)))
iso_b_app1 = apparent_mag(b_iso1, M67_dist)
iso_v_app1 = apparent_mag(v_iso1, M67_dist)

x, y, ind = process_tables(b_data, v_data, M67_dist)
ind = ind - 1  # Ind starts at 1 not at 0
b_x1 = np.take(b_data[1], ind)
b_y1 = np.take(b_data[2], ind)
b_mag1 = np.take(b_data[3], ind)
b_merr1 = np.take(b_data[4], ind)
v_x1 = np.take(v_data[1], ind)
v_y1 = np.take(v_data[2], ind)
v_mag1 = np.take(v_data[3], ind)
v_merr1 = np.take(v_data[4], ind)

filt = ellipse(b_x1, b_y1, 1050, 1050, 1000, 600)
b_x = np.take(b_x1, filt)
b_y = np.take(b_y1, filt)
b_mag = np.take(b_mag1, filt)
b_merr = np.take(b_merr1, filt)
v_mag = np.take(v_mag1, filt)
v_merr = np.take(v_merr1, filt)
x_filt = np.take(x, filt)
y_filt = np.take(y, filt)

# Image coordinates plot to do rough filtering
# plt.scatter(b_x1, b_y1, s=5, c=c1)
# plt.scatter(b_x, b_y, s=5, c=c2, label="Selected")
# plt.title("M67 star rough filtering")
# plt.xlabel(".FITS X")
# plt.ylabel(".FITS Y")
# plt.legend()
# plt.show()


fig, ax = plt.subplots()
plt.scatter(x_filt, y_filt, s=5, c=c2)
plt.plot(iso_b_app-iso_v_app + 0.7, v_iso + 2.3, c="#fa4172")  # 1e10
plt.plot(iso_b_app1-iso_v_app1 + 0.84, v_iso1 + 3.1, c="#34d2e0")

plt.title("HR Diagram for M67")
plt.xlabel(r"$B - V$")
plt.ylabel(r"$M_V$")
ax.invert_yaxis()
plt.show()




