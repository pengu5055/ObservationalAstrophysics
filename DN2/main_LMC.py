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


def movement(coord, delta, intervals):
    """
    Calculates coord changes
    :param coord: Input coord
    :param delta: Delta in some time interval
    :param intervals: Times of that interval
    :return: Changed coord
    """
    return coord + intervals * (delta / 3600000)


def repeat(input, times):
    b = input
    for i in range(0, times - 1):
        b = np.concatenate((b, input))

    return b


c1, c2, c3 = cmr.take_cmap_colors("cmr.gothic", 3, cmap_range=(0.2, 0.8), return_fmt="hex")
source_id, ra, dec, parallax, pmra, pmdec, phot_g_mean_mag = \
    np.column_stack(np.genfromtxt("LMC_tc_rangemag5.csv", delimiter=",", skip_header=1))

# ---- Proper motion quiver plot ----
pmra_median = np.median(pmra)
pmdec_median = np.median(pmdec)
pmra_sub = pmra - pmra_median
pmdec_sub = pmdec - pmdec_median

C = np.hypot(pmra_sub, pmdec_sub)
# plt.scatter(pmra, pmdec, s=0.25, c=c2)

plt.quiver(ra, dec, pmra_sub, pmdec_sub, C, scale=25, cmap="cmr.bubblegum", alpha=0.4)
plt.xlabel(r"$\alpha$ [$\degree$]")
plt.ylabel(r"$\delta$ [$\degree$]")
plt.title("Proper motions of LMC stars")
plt.show()

# ---- Stream plot ----

# data = np.sort(np.array([pmra, pmdec]), axis=1)
# s_pmra = data[0]
# s_pmdec = data[1]
#
# # Y, X = np.mgrid[min(sample_pmra):max(sample_pmra):1000j, min(sample_pmdec):max(sample_pmdec):1000j]
# w = 42352
# s_size = 1000
# sim_years = 100000  # Years tp simulate movment
# sample_ra = ra[:s_size]
# sample_dec = dec[:s_size]
# sample_pmra = pmra[:s_size]
# sample_pmdec = pmdec[:s_size]
# C = repeat(np.sqrt(sample_pmra**2 + sample_pmdec**2), s_size)
#
# movement_ra = repeat([movement(sample_ra, sample_pmra, sim_years)], s_size)
# movement_dec = repeat([movement(sample_dec, sample_pmdec, sim_years)], s_size)
# X = np.linspace(min(sample_ra), max(sample_ra), s_size)
# Y = np.linspace(min(sample_dec), max(sample_dec), s_size)
#
# plt.streamplot(X, Y, movement_ra, movement_dec, color=C, cmap="cmr.bubblegum")
# plt.show()
