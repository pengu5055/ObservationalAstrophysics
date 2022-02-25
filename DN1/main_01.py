import matplotlib.pyplot as plt
import cmasher as cmr
from matplotlib.collections import LineCollection
from src_01 import *

# ----Observatory Data----
obstime = "18:50:05"
obstime_deg = 282.500
AGO_lambda = 14.5277
AGO_phi = 46.0439
ZeroTime = 148.926757
jd_obs = 2459629.50000

# ----Test with Stellarium----
RA_sirius = 0
DEC_sirius = 0
RA_rigel = 78.63446707
DEC_rigel = -08.20163836

r1, r2 = eq2azalt(RA_rigel, DEC_rigel, obstime_deg, ZeroTime, AGO_lambda, AGO_phi)
print(deg2dms(r1), deg2dms(r2))
# print(eq_to_hor(RA_sirius, DEC_sirius, obstime, ZeroTime, AGO_lambda, AGO_phi))

# ----Tracking two stars----
RA_procyon = "07 40 27.871"
DEC_procyon = "05 10 00.74 "
RA_betaUMi = "14 50 42.32580"
DEC_betaUMi = "74 09 19.8142"

t_start = "18:00:00"
t_end = "06:00:00"  # The next day but SUT0 by definition should stay the same

time = "23:44:00"
r1, r2 = eq_to_hor(RA_procyon, DEC_procyon, time, ZeroTime, AGO_lambda, AGO_phi)
print(deg2dms(r1), deg2dms(r2), hms2deg(time))
plt.show()
