import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

c1, c2, c3 = cmr.take_cmap_colors("cmr.gothic", 3, cmap_range=(0.2, 0.8), return_fmt="hex")


source_id, ra, dec, parallax, pmra, pmdec, phot_g_mean_mag = \
    np.column_stack(np.genfromtxt("SMC_tc_rangemag5.csv", delimiter=",", skip_header=1))


# ---- Proper motion filtering ----
def ellipse(u, v, x, y, a, b):
    """ Checks if (u, v) data point is in ellipse with center (x, y) and half axes a and b"""
    output = []
    n = len(u)
    for i in range(n):
        if ((u[i] - x) ** 2)/a**2 + ((v[i] - y) ** 2)/b**2 <= 1:
            output.append(i)

    return np.array(output)


x_coord = 0.77
y_coord = -1.26
filt = ellipse(pmra, pmdec, x_coord, y_coord, 0.5, 0.3)
ra_f = np.take(ra, filt)
dec_f = np.take(dec, filt)
pmra_f = np.take(pmra, filt)
pmdec_f = np.take(pmdec, filt)


# ---- Proper motion filter plot ----
plt.scatter(pmra, pmdec, s=2, c=c1, label="Noise")
plt.scatter(pmra_f, pmdec_f, s=1, c=c2, label="SMC stars")
plt.xlim(-0.25, 1.75)
plt.ylim(-2, -0.25)
plt.title("Filtering by proper motion")
plt.xlabel(r"$\Delta\alpha$ [mas/year]")
plt.ylabel(r"$\Delta\delta$ [mas/year]")
plt.legend()
plt.show()

# ---- Proper motion quiver plot ----
pmra_n = pmra_f - np.median(pmra_f)
pmdec_n = pmdec_f - np.median(pmdec_f)

C = np.hypot(pmra_n, pmdec_n)

plt.quiver(ra_f, dec_f, pmra_n, pmdec_n, C, width=0.004, scale=5, cmap="cmr.bubblegum", alpha=0.4)
plt.xlabel(r"$\alpha$ [$\degree$]")
plt.ylabel(r"$\delta$ [$\degree$]")
plt.title("Rotation of SMC")
plt.colorbar(label=r"$\Delta$ [mas/year]")
plt.show()
