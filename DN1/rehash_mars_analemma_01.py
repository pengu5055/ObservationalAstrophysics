from rehash_src_01 import *
import cmasher as cmr
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# ---- Generate cmasher colors ----
c1, c2, c3 = cmr.take_cmap_colors("cmr.infinity_r", 3, cmap_range=(0., 1), return_fmt="hex")

# ---- Observatory Data ----
obstime_deg = 282.5
AGO_lambda = 14.5277
AGO_phi = 46.0439
ZeroTime = 148.926757

# ---- Analemma Mars ----
GMST = np.genfromtxt("GMST_mars.tsv", usecols=(3,))
JD_init = 2457832.00000  # Julian date of first entry in GMST
# INFO: Table generated so, that index corresponds to days from spring equinox
timeangle = 165  # 11AM
M_0 = 19.3730
M_1 = 0.52402068
Pi = 71.0041
C = [10.6912, 0.6228, 0.0503, 0.0046, 0.0005, 0]

mars_data = planetary_analemma(GMST, timeangle, 687, AGO_lambda, AGO_phi, JD_init, M_0, M_1, Pi, C, 170, 270)

datapoints = np.array([mars_data[0], mars_data[1]]).T.reshape(-1, 1, 2)
segments = np.concatenate([datapoints[:-1], datapoints[1:]], axis=1)
norm = plt.Normalize(0, 366)
lc = LineCollection(segments, cmap="cmr.infinity_s", norm=norm)
lc.set_array(mars_data[2])

fig, ax = plt.subplots()
line = ax.add_collection(lc)

plt.xlim(0, 360)
plt.ylim(-90, 90)
plt.colorbar(line, label=r"Days since vernal equinox")
plt.title("Analemma on Earth in 2022/23")
plt.xlabel(r"Azimuth $[\degree]$")
plt.ylabel(r"Elevation $[\degree]$")
ax.grid(True)
plt.show()
