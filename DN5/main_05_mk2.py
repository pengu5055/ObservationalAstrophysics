import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr
import scipy.integrate as integrate
from scipy.special import wofz
from sklearn.metrics import auc

colors = cmr.take_cmap_colors("cmr.torch", 10, cmap_range=(0.1, 0.9), return_fmt="hex")


def V(x, alpha, gamma):
    """
    Return the Voigt line shape at x with Lorentzian component HWHM gamma
    and Gaussian component HWHM alpha.

    """
    sigma = alpha / np.sqrt(2 * np.log(2))

    return np.real(wofz((x + 1j*gamma)/sigma/np.sqrt(2))) / sigma/np.sqrt(2*np.pi)


def gauss(x, sigma):
    return np.exp(-x**2/(2*sigma**2))/(np.sqrt(2*np.pi) * sigma)


def lorentz(x, gamma):
    return gamma/(np.pi*(x**2 + gamma**2))


def integrand(x_p, x, sigma, gamma):
    return gauss(x_p, sigma) * lorentz(x - x_p, gamma)


def voigt(x, sigma, gamma):
    output = []
    for element in x:
        output.append(integrate.quad(lambda x_p: integrand(x_p, element, sigma, gamma), -np.inf, np.inf)[0])

    return np.array(output)


def saturated_line(x, sigma, gamma, C):
    return np.exp(-C*voigt(x, sigma, gamma))


def e_w(x, I):
    # return integrate.simpson(1-I, x)
    # return auc(x, 1-I)
    return np.trapz(1-I, x)


def line(f, N, phi):
    """Return I/I_0     phi must be array of profile values"""
    return np.exp(-constant*f*N*phi)


constant = 8.431 * 10**-7
# constant = 10**-10

# x_s = np.linspace(-10e7, 10e7, 100000)
x_s = np.linspace(-100, 100, 100000)
# ---- 1. task ----
# sigma = 1
# gamma = 1
# dist1 = gauss(x_s, sigma)
# dist2 = lorentz(x_s, gamma)
# dist4 = voigt(x_s, sigma, gamma)
#
# plt.plot(x_s, dist1, label="Gauss")
# plt.plot(x_s, dist2, label="Lorentz")
# plt.plot(x_s, dist4, label="Voigt")
#
# plt.legend()
# plt.show()

# ---- 2. task ----
# sigma = 10
# gamma = 1
# c = 0
# konst = [1, 10, 50, 100, 500, 1000]
# for k in konst:
#     plt.plot(x_s, saturated_line(x_s, sigma, gamma, k), c=colors[c], label="k:{}".format(k))
#     c += 1
#
# plt.title("Spectral line saturation")
# plt.axhline(1, ls="--", color="gray")
# plt.xlabel("Center of line offset")
# plt.ylabel("Normalized flux")
# plt.legend()
# plt.show()

# ---- 3. task ----


N_space = np.logspace(3, 29, 1000)
phi = V(x_s, 10, 1)
# phi = gauss(x_s, 10)
f = 1
widths = []
for N in N_space:
    l = line(f, N, phi)
    widths.append(e_w(x_s, l))
widths = np.array(widths)

plt.plot(N_space, widths, c=colors[7])

plt.title("Curve of growth")
plt.xscale("log")
plt.yscale("log")
plt.xlabel(r"$\log{Nf_{mu}}$")
plt.ylabel(r"$\log{EW}$")
plt.show()
