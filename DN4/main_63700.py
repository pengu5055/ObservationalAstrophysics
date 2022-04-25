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
wavelengths = np.arange(1e-7, 1e-6, 1e-8)
plt.plot(x, y, c=c1)
spec_line(lines, label)
# plt.axvline(6871.6, ls="--", c=c2)
temp = 6000
# line2 = planck(wavelengths, temp)
# plt.plot(wavelengths, line2/np.max(line2), c=c3, label="Planck for {} K".format(temp))

plt.title("Some spectral lines of HD63700")
plt.xlabel(r"$\lambda$ [m]")
plt.ylabel("Relative Intensity")
plt.legend()
plt.subplots_adjust(bottom=0.17)
plt.show()
