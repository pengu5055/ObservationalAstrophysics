from rehash_src_01 import *
import cmasher as cmr
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# ---- Observatory Data ----
obstime_deg = 282.5
AGO_lambda = 14.5277
AGO_phi = 46.0439
ZeroTime = 148.926757

# ---- Track 2 stars ----
RA_procyon = 114.82549791
DEC_procyon = 05.22498756
RA_kochab = 222.67635750
DEC_kochab = 74.15550394

data, times = startrack(RA_procyon, DEC_procyon, 270, 90, 20000, ZeroTime, AGO_lambda, AGO_phi)
for i in range(len(times)):
    print("Procyon Az: {} Alt: {} Time: {}".format(deg2dms(data[0, i]), deg2dms(data[1, i]), times[i]))

# ==== Plot style 1 ====
# WARNING: POLAR PLOT TAKES X DATA IN RADIANS
datapoints = np.array([np.deg2rad(data[0]), data[1]]).T.reshape(-1, 1, 2)
segments = np.concatenate([datapoints[:-1], datapoints[1:]], axis=1)
norm = plt.Normalize(0, 360)
lc = LineCollection(segments, cmap="cmr.infinity_s", norm=norm)
lc.set_array(times % 360)

fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
line = ax.add_collection(lc)
ax.set_rlim(bottom=90, top=0)
ax.set_rmax(90)
ax.set_rticks([0, 15, 30, 45, 60, 75, 90])
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.grid(True)
plt.colorbar(line, label=r"Time $[\degree]$", pad=0.075)
# plt.title(r"Azimuth and elevation of $\beta$ UMi")
plt.title("Azimuth and elevation of Procyon")
plt.show()

# ==== Plot style 2 ====
datapoints = np.array([data[0], data[1]]).T.reshape(-1, 1, 2)
segments = np.concatenate([datapoints[:-1], datapoints[1:]], axis=1)
norm = plt.Normalize(0, 360)
lc = LineCollection(segments, cmap="cmr.infinity_s", norm=norm)
lc.set_array(times % 360)

fig, ax = plt.subplots()
line = ax.add_collection(lc)
plt.xlim(0, 360)
plt.ylim(-90, 90)
plt.colorbar(line, label=r"Time $[\degree]$")
# plt.title(r"Azimuth and elevation of $\beta$ UMi")
plt.title("Azimuth and elevation of Procyon")
plt.xlabel(r"Azimuth $[\degree]$")
plt.ylabel(r"Elevation $[\degree]$")
ax.grid(True)
plt.show()
