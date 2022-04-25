import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

c1, c2, c3 = cmr.take_cmap_colors("cmr.freeze", 3, cmap_range=(0.2, 0.8), return_fmt="hex")
h = 6.62e-34
k = 1.38e-23
c = 3.e+8


def planck(lamb, T):
    a = 2*h*c**2/lamb**5
    b = h*c/(lamb*k*T)
    return a/(np.exp(b) - 1)


plt.figure(figsize=(12, 3))

x, y = np.column_stack(np.genfromtxt("HD104731.txt"))
x = x * 1e-10
wavelengths = np.arange(1e-7, 1e-6, 1e-8)
plt.plot(x, y/np.max(y), c=c1)
temp = 4400
line2 = planck(wavelengths, temp)
plt.plot(wavelengths, line2/np.max(line2), c=c3, label="Planck for {} K".format(temp))

plt.title("Planck fitted to HD104731")
plt.xlabel(r"$\lambda$ [m]")
plt.ylabel("Normalized Intensity")
plt.legend()
plt.subplots_adjust(bottom=0.17)
plt.show()
