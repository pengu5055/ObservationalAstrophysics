import emcee
import numpy as np


def lnlike(theta, x, y, yerr):
    a, b = theta
    model = a * x + b
    return -0.5 * np.sum(np.array([np.log(2*np.pi*s**2) + ((p - m)/s)**2 for m, p, s in zip(model, y, yerr)]))

