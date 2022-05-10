import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr
from scipy.optimize import curve_fit

c1, c2, c3 = cmr.take_cmap_colors("cmr.bubblegum", 3, cmap_range=(0.3, 1), return_fmt="hex")
d1, d2, d3 = cmr.take_cmap_colors("cmr.toxic", 3, cmap_range=(0.6, 0.9), return_fmt="hex")

def linear(x, k, n):
    return k*x + n


x, y, yerr = np.column_stack(np.genfromtxt("data.dat"))


fitpar1, fitcov1 = curve_fit(linear, x, y)
fitpar2, fitcov2 =curve_fit(linear, x, y, sigma=yerr)
fit1 = linear(x, fitpar1[0], fitpar1[1])
fit2 = linear(x, fitpar2[0], fitpar2[1])

fig, ax = plt.subplots()
fittext1= "Linear fit: $y = kx + n$\n$k$ =  {} ± {}\n$n$ = {} ± {}"\
    .format(format(fitpar1[0], ".4e"), format(fitcov1[0][0]**0.5, ".4e"),
            format(fitpar1[1], ".4e"), format(fitcov1[1][1]**0.5, ".4e"))
plt.text(0.54, 0.85, fittext1, ha="left", va="center", size=10, transform=ax.transAxes,
         bbox=dict(facecolor=c3, alpha=0.5))
plt.plot(x, fit1, c=c3)

fittext2= "Linear fit w err: $y = kx + n$\n$k$ =  {} ± {}\n$n$ = {} ± {}"\
    .format(format(fitpar2[0], ".4e"), format(fitcov2[0][0]**0.5, ".4e"),
            format(fitpar2[1], ".4e"), format(fitcov2[1][1]**0.5, ".4e"))
plt.text(0.54, 0.65, fittext2, ha="left", va="center", size=10, transform=ax.transAxes,
         bbox=dict(facecolor=d3, alpha=0.5))
plt.plot(x, fit2, c=d3)

plt.errorbar(x, y, yerr=yerr, markersize=2, color="#5d89f0",
             linestyle='None', marker="o", capsize=2, alpha=1, label=r"$\psi_r$")

plt.title("Naive fit")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
