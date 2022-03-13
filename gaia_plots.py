import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

c1, c2, c3 = cmr.take_cmap_colors("cmr.bubblegum", 3, cmap_range=(0.2, 0.8), return_fmt="hex")

data = np.column_stack(np.genfromtxt("data_NGC.csv", skip_header=1, delimiter=","))
# FORMAT: source_id ra dec parallax pmra pmdec phot_gmean_mag

plt.scatter(data[4], data[5], c=c3, s=3)
plt.title("Proper motion of RA vs DEC")
plt.xlabel(r"pmRA [mas/year]")
plt.ylabel(r"pmDEC [mas/year]")
plt.show()

# Histogram
plt.hist(data[3], bins=200, color=c1)
plt.title("Histogram of parallaxes")
plt.ylabel("Counts")
plt.xlabel("Parallax [mas]")
plt.show()
