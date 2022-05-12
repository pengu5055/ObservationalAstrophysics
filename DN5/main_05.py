import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr
from scipy.stats import cauchy
from scipy.signal import convolve


colors = cmr.take_cmap_colors("cmr.torch", 20, cmap_range=(0.1, 0.9), return_fmt="hex")


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def cauchy_pdf(x, mu, gamma):
    dist = cauchy(mu, gamma)
    return dist.pdf(x)


def voigt(x, mu, sig, gamma):
    """Returns normalized voigt profile"""
    dist = np.convolve(cauchy_pdf())

    return

x_space = np.linspace(-3, 3, 100)
x_space2 = np.linspace(-3, 3, 199)
dist1 = cauchy_pdf(x_space, 0, 1)
dist2 = gaussian(x_space, 0, 1)
dist3 = convolve(dist1, dist2)
dist3 = dist3 / np.max(dist3)
# dist3 = dist3[:len(dist3)//2 + 1]

plt.plot(x_space, dist1, color=colors[4], label="Cauchy")
plt.plot(x_space, dist2, color=colors[7], label="Gauss")
plt.plot(x_space2, dist3, color=colors[14], label="Voigt")

plt.title("Distributions")
plt.legend()
plt.show()
