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
SUT0_vec = np.genfromtxt("GMST_2022.tsv", usecols=(3,))
# INFO: Table generated so, that index corresponds to days from spring equinox
timeangle = 165  # 11AM

