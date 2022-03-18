import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

c1, c2, c3 = cmr.take_cmap_colors("cmr.gothic", 3, cmap_range=(0.2, 0.8), return_fmt="hex")
# source_id, ra, dec, parallax, pmra, phot_g_mean_mag =
# np.column_stack(np.genfromtxt("LMC1-result.csv", delimiter=",", skip_header=1))
source_id, ra, dec, parallax, pmra, pmdec, phot_g_mean_mag = np.column_stack(np.genfromtxt("SMC_tc_nomag.csv", delimiter=",", skip_header=1))
source_id2, ra2, dec2, parallax2, pmra2, pmdec2, phot_g_mean_mag2 = np.column_stack(np.genfromtxt("SMC_tc_rangemag5.csv", delimiter=",", skip_header=1))

plt.title("SMC in the field")
plt.scatter(ra, dec, s=0.25, c=c1)
plt.scatter(ra2, dec2, s=0.25, c=c3)
plt.xlabel(r"$\alpha$ [$\degree$]")
plt.ylabel(r"$\delta$ [$\degree$]")
plt.show()
