from rehash_src_01 import *
import cmasher as cmr
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# ---- Observatory Data ----
obstime_deg = 282.5
AGO_lambda = 14.5277
AGO_phi = 46.0439
ZeroTime = 148.926757

# ---- Analemma 1 ----
GMST = np.genfromtxt("GMST_2022.tsv", usecols=(3,))
JD_init = 2459659.00000  # Julian date of first entry in GMST
# INFO: Table generated so, that index corresponds to days from spring equinox
timeangle = 165  # 11AM
data = sun_proper_analemma(GMST, timeangle, AGO_lambda, AGO_phi, JD_init)

datapoints = np.array([data[0], data[1]]).T.reshape(-1, 1, 2)
segments = np.concatenate([datapoints[:-1], datapoints[1:]], axis=1)
norm = plt.Normalize(0, 360)
lc = LineCollection(segments, cmap="cmr.infinity_s", norm=norm)
lc.set_array(data[2])

fig, ax = plt.subplots()
line = ax.add_collection(lc)

plt.xlim(0, 360)
plt.ylim(-90, 90)
plt.colorbar(line, label=r"Days since vernal equinox")
plt.title("Corrected analemma on Earth in 2022/23")
plt.xlabel(r"Azimuth $[\degree]$")
plt.ylabel(r"Elevation $[\degree]$")
ax.grid(True)
plt.show()

