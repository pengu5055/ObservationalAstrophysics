import numpy as np
import matplotlib.pyplot as plt

data_star = np.column_stack(np.genfromtxt("14.dat"))
data_com = np.column_stack(np.genfromtxt("23.dat"))
mag_star = data_star[1]
jd = data_star[0]
mag_com = data_com[1]

plt.scatter(jd, mag_star - mag_com, s=3, c="#AA33B4")
plt.gca().invert_yaxis()
plt.title("Light curve for Cy Aqr")
plt.xlabel("jd")
plt.ylabel("Mag. dif.")
plt.show()
