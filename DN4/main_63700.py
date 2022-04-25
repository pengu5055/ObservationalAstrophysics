import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr
from radis import sPlanck

c1, c2, c3 = cmr.take_cmap_colors("cmr.freeze", 3, cmap_range=(0.2, 0.8), return_fmt="hex")
h = 6.62e-34
k = 1.38e-23
c = 3.e+8
#
#
def blackbody_lam(lam, T):
    """ Blackbody as a function of wavelength (um) and temperature (K).

    returns units of erg/s/cm^2/cm/Steradian
    """
    from scipy.constants import h,k,c
    lam = 1e-10 * lam  # convert to metres
    return 2*h*c**2 / (lam**5 * (np.exp(h*c / (lam*k*T)) - 1))


def planck(wav, T):
    # wav = wav * 10e-10
    a = 2.0*h*c**2
    b = h*c/(wav*k*T)
    intensity = a/ ( (wav**5) * (np.exp(b) - 1.0) )
    return intensity


def spec_line(wave_table, label_table, label_height=10000, label_offset=100):
    n = len(wave_table)
    color = cmr.take_cmap_colors("cmr.flamingo", n, cmap_range=(0.3, 0.8), return_fmt="hex")
    for i in range(n):
        plt.axvline(float(wave_table[i]), ls="--", c=color[i])
        plt.text(float(wave_table[i]) - label_offset, label_height + np.random.randint(-10000, 10000, 1), label_table[i], rotation="vertical", c=color[i])


plt.figure(figsize=(12, 3))
x, y = np.column_stack(np.genfromtxt("HD63700.txt"))
lines = ["5266.2", "5892", "6139", "6497.4", "6563.4", "6871.6", "7605.5", "7630.9", "8500.1", "8544", "8665.2"]
label = ["Fe I", "Na I", "Cs III", "Fe I", "H I", "V I", "V I", "V I", "V I", "V I", "Fe I"]
wavelengths = np.arange(1000e-10, 15000e-10, 1e-10)
plt.plot(x, y/np.max(y), c=c1)
# spec_line(lines, label)
# plt.axvline(6871.6, ls="--", c=c2)
temp = 4000
line2 = planck(wavelengths, temp)
plt.plot(wavelengths * 10e9, line2/np.max(line2), c=c3, label=temp)

plt.title("Planck fitted to HD63700")
plt.xlabel(r"$\lambda$ [$\AA$]")
plt.ylabel("Normalized Intensity")
plt.legend()
plt.show()
