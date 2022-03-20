import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

X = np.linspace(-5, 5, 100)
Y = np.linspace(-3, 3, 100)
deltaX = deltaY = np.array(100*[1])


# deltaX = np.linspace(0, 1, 100)
# deltaY = np.linspace(0, 1, 100)

# xx, yy = np.meshgrid(X, Y)
# U = xx * yy
#
#
# plt.streamplot(xx, yy, U, yy)
# plt.show()
a = [1, 2, 3, 4]
data = [a]


def repeat(input, times):
    b = input
    for i in range(0, times - 1):
        b = np.concatenate((b, input))

    return b


print(repeat(data, 3))
