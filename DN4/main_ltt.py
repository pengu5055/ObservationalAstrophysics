import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

c1, c2, c3 = cmr.take_cmap_colors("cmr.freeze", 3, cmap_range=(0.2, 0.8), return_fmt="hex")


def spec_line(wave_table, label_table, label_height=10000, label_offset=100):
    n = len(wave_table)
    color = cmr.take_cmap_colors("cmr.flamingo", n, cmap_range=(0.3, 0.8), return_fmt="hex")
    for i in range(n):
        plt.axvline(float(wave_table[i]), ls="--", c=color[i])
        plt.text(float(wave_table[i]) - label_offset, label_height + np.random.randint(-5000, 5000, 1),
                 label_table[i], rotation="vertical", c=color[i])


plt.figure(figsize=(12, 3))
x, y = np.column_stack(np.genfromtxt("LTT6248.txt"))
lines = ["3887", "3967", "4100", "4340", "4860", "5892", "6279", "6562", "6871", "7188", "7605", "7629.6"]
label = ["Fe I", "Cu I", "H I", "H I", "H I", "He I", "Al II", "H I", "V I", "Mg II", "V I", "V I"]

plt.plot(x, y, c=c1)
spec_line(lines, label)
plt.title("Some spectral lines of LTT6248")
plt.xlabel(r"$\lambda$ [$\AA$]")
plt.ylabel("Relative Intensity")
plt.show()
