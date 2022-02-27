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

# ---- Analemma 1 ----
GMST = np.genfromtxt("GMST_2022.tsv", usecols=(3,))
JD_init = 2459659.00000  # Julian date of first entry in GMST
# INFO: Table generated so, that index corresponds to days from spring equinox
timeangle = 165  # 11AM
data = sun_proper_analemma(GMST, timeangle, AGO_lambda, AGO_phi, JD_init)
data_2 = sun_analemma(GMST, timeangle, AGO_lambda, AGO_phi)

fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(data[0], data[1], c=c1, label="Eccentric orbit")
ax1.plot(data_2[0], data_2[1], c=c2, label="Circular orbit")
ax1.set_xlim(140, 170)
ax1.set_ylim(15, 65)
ax1.set_xlabel(r"Azimuth $[\degree]$")
ax1.set_ylabel(r"Elevation $[\degree]$")
ax1.grid(True)
ax1.legend()

datapoints = np.array([np.abs(data[0] - data_2[0]), np.abs(data[1] - data_2[1])]).T.reshape(-1, 1, 2)
segments = np.concatenate([datapoints[:-1], datapoints[1:]], axis=1)
norm = plt.Normalize(0, 366)
lc = LineCollection(segments, cmap="cmr.infinity_s", norm=norm)
lc.set_array(data[2])
line = ax2.add_collection(lc)
plt.colorbar(line, label=r"Days since vernal equinox", ax=ax2)
ax2.set_xlabel(r"Az. abs. err. $[\degree]$")
ax2.set_ylabel(r"El. abs. err. $[\degree]$")
ax2.set_xlim(0, 5)
ax2.set_ylim(-0.1, 2.9)
ax2.grid(True)

plt.suptitle("Comparison between circular and eccentric orbit")
plt.subplots_adjust(wspace=0.29)
plt.show()
