from rehash_src_01 import *

# ---- Observatory Data ----
obstime_deg = 282.5
AGO_lambda = 14.5277
AGO_phi = 46.0439
ZeroTime = 148.926757

RA_procyon = 114.82549791
DEC_procyon = 05.22498756


times = np.linspace(270, 90 + 360, 20)
for time in times:
    az1, alt1 = eq2azalt(RA_procyon, DEC_procyon, time, ZeroTime, AGO_lambda, AGO_phi)
    print("Procyon Az: {} Alt: {} Time: {}".format(deg2dms(az1), deg2dms(alt1), time))
