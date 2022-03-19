import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

X = np.linspace(-5, 5, 100)
Y = np.linspace(-3, 3, 100)
deltaX = deltaY = np.array(100*[1])


# deltaX = np.linspace(0, 1, 100)
# deltaY = np.linspace(0, 1, 100)

xx, yy = np.meshgrid(X, Y)

plt.streamplot(xx, yy, xx + 10, yy)
plt.show()
