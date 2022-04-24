import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

c1, c2, c3 = cmr.take_cmap_colors("cmr.freeze", 3, cmap_range=(0.2, 0.8), return_fmt="hex")


def spec_line(wave_table, label_table, label_height=10000, label_offset=100):
    n = len(wave_table)
    color = cmr.take_cmap_colors("cmr.flamingo", n, cmap_range=(0.3, 0.8), return_fmt="hex")
    for i in range(n):
        plt.axvline(float(wave_table[i]), ls="--", c=color[i])
        plt.text(float(wave_table[i]) - label_offset, label_height + np.random.randint(-10000, 10000, 1), label_table[i], rotation="vertical", c=color[i])


plt.figure(figsize=(12, 3))
x, y = np.column_stack(np.genfromtxt("HD63700.txt"))
lines = ["5266.2", "5892", "6139", "6497.4", "6563.4", "6871.6", "7605.5", "7630.9", "8500.1", "8544", "8665.2"]
label = ["Fe I", "Hg II", "Hg II", "Fe I", "H I", "V I", "V I", "V I", "V I", "V I", "Fe I"]

plt.plot(x, y, c=c1)
spec_line(lines, label)
# plt.axvline(6871.6, ls="--", c=c2)
plt.title("Some spectral lines of HD63700")
plt.xlabel(r"$\lambda$ [$\AA$]")
plt.ylabel("Relative Intensity")
plt.show()
