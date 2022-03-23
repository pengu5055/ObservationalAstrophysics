import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr
from scipy.interpolate import griddata

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


# ---- Proper motion filtering ----
def ellipse(u, v, x, y, a, b):
    """ Checks if (u, v) data point is in ellipse with center (x, y) and half axes a and b"""
    output = []
    n = len(u)
    for i in range(n):
        if ((u[i] - x) ** 2)/a**2 + ((v[i] - y) ** 2)/b**2 <= 1:
            output.append(i)

    return np.array(output)


x_coord = 1.86
y_coord = 0.33
filt = ellipse(pmra, pmdec, x_coord, y_coord, 0.7, 1)
ra_f = np.take(ra, filt)
dec_f = np.take(dec, filt)
pmra_f = np.take(pmra, filt)
pmdec_f = np.take(pmdec, filt)
pmra_n = pmra_f - np.median(pmra_f)
pmdec_n = pmdec_f - np.median(pmdec_f)  # Len is 41443
C = np.hypot(pmra_n, pmdec_n)

# ---- Proper motion filter plot ----
# plt.scatter(pmra, pmdec, s=2, c=c1, label="Noise")
# plt.scatter(pmra_f, pmdec_f, s=1, c="#ADF1D2", label="LMC stars")
# plt.xlim(-4, 7)
# plt.ylim(-7, 7)
# plt.title("Filtering by proper motion")
# plt.xlabel(r"$\Delta\alpha$ [mas/year]")
# plt.ylabel(r"$\Delta\delta$ [mas/year]")
# plt.legend()
# plt.show()

# ---- Proper motion quiver plot ----
# plt.quiver(ra_f, dec_f, pmra_n, pmdec_n, C, width=0.002, headwidth=3, headlength=5,
#            scale=10, cmap="cmr.bubblegum", alpha=0.6)
# plt.xlabel(r"$\alpha$ [$\degree$]")
# plt.ylabel(r"$\delta$ [$\degree$]")
# plt.title("Rotation of LMC")
# plt.colorbar(label=r"$\Delta$ [mas/year]")
# plt.show()


# ---- Stream plot (failed) ----
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

# ---- Stream plot code snippet from Ema ----
fig, ax = plt.subplots()
x = np.array(ra_f)
y = np.array(dec_f)
u = pmra_n
v = pmdec_n

# resample onto a 50x50 grid
nx, ny = 50, 50

# (N, 2) arrays of input x,y coords and u,v values
pts = np.vstack((x, y)).T
vals = np.vstack((u, v)).T

# the new x and y coordinates for the grid, which will correspond to the
# columns and rows of u and v respectively
xi = np.linspace(x.min(), x.max(), nx)
yi = np.linspace(y.min(), y.max(), ny)

# an (nx * ny, 2) array of x,y coordinates to interpolate at
ipts = np.vstack(a.ravel() for a in np.meshgrid(yi, xi)[::-1]).T

# an (nx * ny, 2) array of interpolated u, v values
ivals = griddata(pts, vals, ipts, method='nearest')

# reshape interpolated u,v values into (ny, nx) arrays
ui, vi = ivals.T
ui.shape = vi.shape = (ny, nx)
grid_C = np.hypot(ui, vi)

# plot
# fig, ax = plt.subplots(1, 1)
# ax.hold(True)
plt.streamplot(xi, yi, ui, vi, color=grid_C, cmap="cmr.bubblegum")
plt.title("Prikaz rotacije z tokovnicami za LMC")
plt.xlabel(r"$\alpha$ [$\degree$]")
plt.ylabel(r"$\delta$ [$\degree$]")
plt.colorbar(label=r"$\Delta$ [mas/year]")
plt.show()
