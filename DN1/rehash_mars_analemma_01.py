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

