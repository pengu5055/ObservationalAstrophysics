import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

CALIBRATION_CORR = 2.35  # Angstrom
colors = cmr.take_cmap_colors("cmr.torch", 20, cmap_range=(0.1, 0.9), return_fmt="hex")

x, y = np.column_stack(np.genfromtxt("HD194839.dat"))

# Rough filtering of shit spike
x = x[300:len(x)-700]
y = y[300:len(y)-700]

fig, ax = plt.subplots()
plt.plot(x + CALIBRATION_CORR, y, c=colors[14])

plt.title("Sodium doublet in HD194839")
plt.xlabel(r"$\lambda$ [$\AA$]")
plt.ylabel("Relative intensity")
plt.xlim(5880, 5920)
ax.grid(True)
plt.show()
