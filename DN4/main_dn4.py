import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

x, y = np.column_stack(np.genfromtxt("HD63700.txt"))

plt.plot(x, y)
plt.show()
