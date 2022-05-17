import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr
from scipy.optimize import curve_fit

c1, c2, c3 = cmr.take_cmap_colors("cmr.bubblegum", 3, cmap_range=(0.3, 1), return_fmt="hex")
d1, d2, d3 = cmr.take_cmap_colors("cmr.toxic", 3, cmap_range=(0.6, 0.9), return_fmt="hex")
color = cmr.take_cmap_colors("cmr.bubblegum", 8, cmap_range=(0.3, 1), return_fmt="hex")


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

import emcee
import corner


def lnlike(theta, x, y, yerr):
    a, b, f = theta
    model = a * x + b
    moderror = yerr + f * yerr
    return -0.5 * np.sum(np.array([np.log(2*np.pi*s**2) + ((p - m)/s)**2 for m, p, s in zip(model, y, moderror)]))


def lnprior(theta):
    a, b, f = theta
    if -10 < a < 10 and -10 < b < 10 and 0 < f < 10:
        return 0.0
    else:
        return -np.inf


def lnprob(theta, x, y, yerr):
    return lnprior(theta) + lnlike(theta, x, y, yerr)


def initcond(num_walkers, a_min, a_max, b_min, b_max):
    return np.array([[np.random.uniform(a_min, a_max), np.random.uniform(b_max, b_min), np.random.uniform(0, 10)] for i in range(num_walkers)])


theta = np.array([1, 4])
walkers = 8
init = initcond(8, -10, 10, -10, 10)

sampler = emcee.EnsembleSampler(walkers, 3, lnprob, args=(x, y, yerr))
sampler.run_mcmc(init, 5000)
samples = sampler.get_chain()


fig, (ax1, ax2) = plt.subplots(2, 1)
for i in range(walkers):
    ax1.plot(samples[:, i, 0], c=color[i])
    ax2.plot(samples[:, i, 1], c=color[i])
plt.show()

flat_samples = sampler.get_chain(discard=100, flat=True)
fig, ax = plt.subplots()
plt.scatter(flat_samples[:, 0], flat_samples[:, 1], cmap="cmr.bubblegum", s=2)
plt.show()
fig2 = corner.corner(flat_samples, labels=["a", "b", "f"], quantiles=[0.16, 0.5, 0.84], show_titles=True)
plt.show()


