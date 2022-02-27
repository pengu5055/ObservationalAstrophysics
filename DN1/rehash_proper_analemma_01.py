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

# Additional curves
data_8 = sun_proper_analemma(GMST, 120, AGO_lambda, AGO_phi, JD_init)
data_9 = sun_proper_analemma(GMST, 135, AGO_lambda, AGO_phi, JD_init)
data_10 = sun_proper_analemma(GMST, 150, AGO_lambda, AGO_phi, JD_init)
data_12 = sun_proper_analemma(GMST, 180, AGO_lambda, AGO_phi, JD_init)
data_13 = sun_proper_analemma(GMST, 195, AGO_lambda, AGO_phi, JD_init)
data_14 = sun_proper_analemma(GMST, 210, AGO_lambda, AGO_phi, JD_init)
data_15 = sun_proper_analemma(GMST, 225, AGO_lambda, AGO_phi, JD_init)
data_16 = sun_proper_analemma(GMST, 240, AGO_lambda, AGO_phi, JD_init)


datapoints = np.array([data[0], data[1]]).T.reshape(-1, 1, 2)
segments = np.concatenate([datapoints[:-1], datapoints[1:]], axis=1)
norm = plt.Normalize(0, 360)
lc = LineCollection(segments, cmap="cmr.infinity_s", norm=norm)
lc.set_array(data[2])

fig, ax = plt.subplots()
line = ax.add_collection(lc)

plt.plot(data_8[0], data_8[1], c="#c5cbd4", alpha=0.7)
plt.plot(data_9[0], data_9[1], c="#c5cbd4", alpha=0.7)
plt.plot(data_10[0], data_10[1], c="#c5cbd4", alpha=0.7)
plt.plot(data_12[0], data_12[1], c="#c5cbd4", alpha=0.7)
plt.plot(data_13[0], data_13[1], c="#c5cbd4", alpha=0.7)
plt.plot(data_14[0], data_14[1], c="#c5cbd4", alpha=0.7)
plt.plot(data_15[0], data_15[1], c="#c5cbd4", alpha=0.7)
plt.plot(data_16[0], data_16[1], c="#c5cbd4", alpha=0.7)

# Annotate analemmas
ax.annotate('8h',
            xy=(92.1, 35.6), xycoords='data',
            xytext=(0, 5), textcoords='offset points',
            horizontalalignment='right', verticalalignment='bottom', color="#6c6f73")
ax.annotate('9h',
            xy=(104, 46), xycoords='data',
            xytext=(0, 5), textcoords='offset points',
            horizontalalignment='right', verticalalignment='bottom', color="#6c6f73")
ax.annotate('10h',
            xy=(120, 55), xycoords='data',
            xytext=(0, 5), textcoords='offset points',
            horizontalalignment='right', verticalalignment='bottom', color="#6c6f73")
ax.annotate('11h',
            xy=(141, 63), xycoords='data',
            xytext=(0, 5), textcoords='offset points',
            horizontalalignment='right', verticalalignment='bottom', color="#000000")
ax.annotate('12h',
            xy=(174, 67), xycoords='data',
            xytext=(0, 5), textcoords='offset points',
            horizontalalignment='center', verticalalignment='bottom', color="#6c6f73")
ax.annotate('13h',
            xy=(208, 65), xycoords='data',
            xytext=(0, 5), textcoords='offset points',
            horizontalalignment='left', verticalalignment='bottom', color="#6c6f73")
ax.annotate('14h',
            xy=(233, 58), xycoords='data',
            xytext=(0, 5), textcoords='offset points',
            horizontalalignment='left', verticalalignment='bottom', color="#6c6f73")
ax.annotate('15h',
            xy=(250, 50), xycoords='data',
            xytext=(0, 5), textcoords='offset points',
            horizontalalignment='left', verticalalignment='bottom', color="#6c6f73")
ax.annotate('16h',
            xy=(260, 40), xycoords='data',
            xytext=(0, 5), textcoords='offset points',
            horizontalalignment='left', verticalalignment='bottom', color="#6c6f73")

plt.xlim(80, 275)
plt.ylim(-5, 75)
plt.colorbar(line, label=r"Days since vernal equinox")
plt.title("Corrected analemma on Earth in 2022/23")
plt.xlabel(r"Azimuth $[\degree]$")
plt.ylabel(r"Elevation $[\degree]$")
ax.grid(True)
plt.show()

