import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr
from scipy.stats import cauchy
from scipy.special import voigt_profile

# colors = cmr.take_cmap_colors("cmr.torch", 20, cmap_range=(0.1, 0.9), return_fmt="hex")
colors = cmr.take_cmap_colors("cmr.torch", 100, cmap_range=(0.1, 0.9), return_fmt="hex")

def gauss_pdf(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def lorentz_pdf(x, mu, gamma):
    dist = cauchy(mu, gamma)
    return dist.pdf(x)


def lorentz_voigt(x, A, xc, wL):
    return (2*A / np.pi) * (wL / ((4*(x.astype(float) - xc)**2) + wL**2))


def gauss_voigt(x, wG):
    return np.sqrt((4*np.log(2)) / np.pi) * ((np.exp(-(((4*np.log(2)) / (wG**2))*(x.astype(float))**2))) / (wG))


def voigt(x, xc, A, wG, wL):
    """
    y0 = offset, xc = center, A =area, wG = Gaussian FWHM, wL = Lorentzian FWHM
    FWHM = 0.5346 * wL + sqrt(0.2166 * wL * wL + wG * wG)
    Source: https://www.originlab.com/doc/Origin-Help/Voigt-FitFunc
    """
    dist = np.convolve(lorentz_voigt(x, A, xc, wL), gauss_voigt(x, wG), 'full')
    return dist


x_space = np.linspace(-3, 3, 1000)
x_space2 = np.linspace(-3, 3, 1999)
dist1 = gauss_pdf(x_space, 0, 1)
dist2 = lorentz_pdf(x_space, 0, 1)
dist3 = voigt(x_space, 0, 1, 1, 1)
dist4 = voigt_profile(x_space, 1, 1)

# plt.plot(x_space, dist1, c=colors[4], label="Gauss")
# plt.plot(x_space, dist2, c=colors[7], label="Lorentz")
plt.plot(x_space2, dist3, c=colors[10], label="Voigt")
plt.plot(x_space, dist4, c=colors[15], label="Voigt 2")
plt.title("Distributions")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.show()


C = 100  # Constant factor
line = voigt(x_space, 0, 1, 0.001, 0.001)
satur_line = np.exp(-C * line)
plt.plot(x_space2, satur_line, c=colors[4])
plt.plot(x_space2, -line, c=colors[14])
plt.show()