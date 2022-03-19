import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

c1, c2, c3 = cmr.take_cmap_colors("cmr.gothic", 3, cmap_range=(0.2, 0.8), return_fmt="hex")


source_id, ra, dec, parallax, pmra, pmdec, phot_g_mean_mag = np.column_stack(np.genfromtxt("SMC_tc_rangemag5.csv", delimiter=",", skip_header=1))

# ---- Proper motion quiver plot ----
C = np.hypot(pmra, pmdec)
plt.title("Proper motions of SMC stars")
# plt.scatter(pmra, pmdec, s=0.25, c=c2)

plt.quiver(ra, dec, pmra, pmdec, C, scale=50, cmap="cmr.bubblegum", alpha=0.4)
plt.xlabel(r"$\alpha$ [$\degree$]")
plt.ylabel(r"$\delta$ [$\degree$]")
plt.show()
