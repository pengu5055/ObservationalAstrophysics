import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr


# Check ascending order
def order(input):
    prev = input[0]
    for element in input:
        if element >= prev:
            prev = element
        else:
            raise ArithmeticError("Not ascending order..")
    return True



c1, c2, c3 = cmr.take_cmap_colors("cmr.gothic", 3, cmap_range=(0.2, 0.8), return_fmt="hex")
source_id, ra, dec, parallax, pmra, pmdec, phot_g_mean_mag = \
    np.column_stack(np.genfromtxt("LMC_tc_rangemag5.csv", delimiter=",", skip_header=1))

# ---- Proper motion quiver plot ----
# C = np.hypot(pmra, pmdec)
# plt.title("Proper motions of LMC stars")
# # plt.scatter(pmra, pmdec, s=0.25, c=c2)
#
# plt.quiver(ra, dec, pmra, pmdec, C, scale=50, cmap="cmr.bubblegum", alpha=0.4)
# plt.xlabel(r"$\alpha$ [$\degree$]")
# plt.ylabel(r"$\delta$ [$\degree$]")
# plt.show()

# ---- Stream plot ----
w = 3
l = 42352  # Size of arrays

# TODO: Define what an arrow is
# TODO: Make meshrid from sorted ra and dec

data = np.sort(np.array([pmra, pmdec]), axis=1)
s_pmra = data[0]
s_pmdec = data[1]

w = 42352
s_size = 1000
sample_ra = s_pmra[:s_size]
sample_dec = s_pmdec[:s_size]
Y, X = np.mgrid[min(sample_ra):max(sample_ra):100j, min(sample_dec):max(sample_dec):100j]
plt.streamplot(X, Y, X, Y, cmap="cmr.bubblegum")
plt.show()
