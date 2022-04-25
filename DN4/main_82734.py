import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr

c1, c2, c3 = cmr.take_cmap_colors("cmr.freeze", 3, cmap_range=(0.2, 0.8), return_fmt="hex")
h = 6.62e-34
k = 1.38e-23
c = 3.e+8


def planck(wav, T):
    # wav = wav * 10e-10
    a = 2.0*h*c**2
    b = h*c/(wav*k*T)
    intensity = a/ ( (wav**5) * (np.exp(b) - 1.0) )
    return intensity


def spec_line(wave_table, label_table, label_height=10000, label_offset=100):
    n = len(wave_table)
    color = cmr.take_cmap_colors("cmr.flamingo", n, cmap_range=(0.3, 0.8), return_fmt="hex")
    for i in range(n):
        plt.axvline(float(wave_table[i]), ls="--", c=color[i])
        plt.text(float(wave_table[i]) - label_offset, label_height + np.random.randint(-10000, 10000, 1),
                 label_table[i], rotation="vertical", c=color[i])


plt.figure(figsize=(12, 3))
x, y = np.column_stack(np.genfromtxt("HD82734.txt"))
lines = ["4861", "5168", "5266", "5890",  "5896", "6497", "6564", "6871", "7605", "7629.6"]
label = ["H I", "Fe I", "Fe I", "Na I", "Na I", "Fe I", "H I", "V I", "V I", "V I"]

wavelengths = np.arange(1000e-10, 15000e-10, 1e-10)
plt.plot(x, y, c=c1)
spec_line(lines, label)
# plt.axvline(6871.6, ls="--", c=c2)
temp = 4000
# line2 = planck(wavelengths, temp)
# plt.plot(wavelengths * 10e9, line2/np.max(line2), c=c3, label=temp)
plt.title("Some spectral lines of HD82734")
plt.xlabel(r"$\lambda$ [$\AA$]")
plt.ylabel("Relative Intensity")
plt.subplots_adjust(bottom=0.17)
plt.show()
