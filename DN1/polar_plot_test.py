from matplotlib import pyplot as plt
import numpy as np

theta = 35
r = 0.8
fig, ax1 = plt.subplots(subplot_kw={"projection": "polar"})
ax1.scatter(np.deg2rad(theta), r, c="k")
ax1.set_ylim(0, 1)
plt.show()
