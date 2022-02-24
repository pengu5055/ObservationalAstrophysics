import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr
from matplotlib.collections import LineCollection


def eq_to_hor(alpha, delta, time, SUT0, lamb, phi):
    """
    Convert equatorial coordinates to horizontal
    INPUTS:
    :param alpha: Right ascension in DMS
    :param delta: Declination in DMS
    :param SUT0: Greenwich mean sidereal time at 0h UT
    :param time: Time of observation in HH:MM:SS
    :param lamb: Observer longitude
    :param phi: Observer latitude

    OUTPUTS:
    :return A: Azimuth
    :return h: Elevation
    """
    time = hms2deg(time)
    H = np.deg2rad((get_LST(time, SUT0, lamb) - hms2deg(alpha)) % 360)  # Warning! Alpha is given in HMS
    print(H)
    delta = np.deg2rad(dms2deg(delta))
    phi = np.deg2rad(phi)
    h = np.arcsin(np.sin(phi)*np.sin(delta) + np.cos(phi)*np.cos(delta)*np.cos(H))
    A = np.arccos((np.sin(delta)-np.sin(phi)*np.sin(h))/(np.cos(phi)*np.cos(h)))

    return np.rad2deg(A), np.rad2deg(h)


def dms2deg(t):
    """Convert DMS to decimals. Input format DD MM SS.SS"""
    t = t.split(" ")
    if np.sign(int(t[0])) == 1 or np.sign(int(t[0])) == 0:
        return (float(t[0]) + float(t[1])/60 + float(t[2])/3600) % 360
    elif np.sign(int(t[0])) == -1:
        return (float(t[0]) - float(t[1]) / 60 - float(t[2]) / 3600) % 360
    else:
        raise ValueError("Something's fucky..")


def deg2dms(time):
    tH = int(np.trunc(time))
    tM = int(np.trunc((time - tH) * 60))
    tS = (((time - tH) * 60) - tM) * 60

    return "{:0>2d}:{:0>2d}:{:05.2f}".format(int(tH), int(tM), (tS))


def hms2deg(time):
    """Converts HMS time to degree. Input format HH:MM:SS.SS or HH MM SS.SS"""
    time = str(time)
    if time[2] == ":":
        s = time.split(":")
    elif time[2] == " ":
        s = time.split(" ")
    else:
        # raise ValueError("Unknown input format")
        return float(time)

    return ((float(s[0]) + (float(s[1]) / 60) + float(s[2]) / 3600) * 15) #% 360


def deg2hms(time):
    """Converts degree time to HMS"""
    time = time/15
    tH = int(np.trunc(time))
    tM = int(np.trunc((time - tH)*60))
    tS = (((time - tH)*60)-tM)*60

    return "{:0>2d}:{:0>2d}:{:05.2f}".format(int(tH), int(tM), (tS))


def get_LST(t, SUT0, lambd, t_0=15):
    """Get local star time"""
    return (SUT0 + lambd + (t - t_0) * (366.2422 / 365.2422)) % 360


def track_azalt(alpha, delta, time_start, time_end, bins, SUT0, lamb, phi):
    """
    Track elevation and azimuth of desired star at discrete time points
    :param alpha: Right ascension of star
    :param delta: Declination of star
    :param time_start: Time of observation start in HMS
    :param time_end: Time of observation end in HMS
    :param bins: Discrete divisions of time interval (2 less than given because broken bins system in generator)
    :param SUT0: Greenwich sidereal time at 0h UT
    :param lamb: Observer longitude
    :param phi: Observer latitude
    :return: 2D array with Azimuth and elevation and 1D array of times
    """
    time_start = hms2deg(time_start)
    time_end = hms2deg(time_end)
    times = list(crange(time_start, time_end, 360, bins))
    print(times)
    output = []
    for time in times:
        time = deg2hms(time)  # Hacky fix the fact that eq_to_hor takes HMS time (and instantly converts it into deg)
        output.append(eq_to_hor(alpha, delta, time, SUT0, lamb, phi))

    return np.column_stack(np.array(output)), np.array(list(times))


def crange(start, end, modulo, bin):
    """Generator of circular range"""
    step = np.abs(start - end)/bin
    # end += bin   # Hacky fix to extend range to [start, end] and not [start, end)
    if start > end:
        while start < modulo:
            yield start
            start += step
        start = 0

    while start < end:
        yield start
        start += step


# ----Observatory Data----
obstime = "18:50:05"
AGO_lambda = 14.5277
AGO_phi = 46.0439
# ZeroTime = 149.912405
ZeroTime = 148.926757

# ----Test with Cartes du Ciel----
RA_sirius = "06 46 07.6"
DEC_sirius = "-16 45 57.5"
RA_rigel = "05 15 35.9"
DEC_rigel = "-08 10 44.8"

r1, r2 = eq_to_hor(RA_rigel, DEC_rigel, obstime, ZeroTime, AGO_lambda, AGO_phi)
# print(deg2dms(r1), deg2dms(r2))
# print(eq_to_hor(RA_sirius, DEC_sirius, obstime, ZeroTime, AGO_lambda, AGO_phi))

# ----Tracking two stars----
RA_procyon = "07 40 27.871"
DEC_procyon = "05 10 00.74 "
RA_betaUMi = "14 50 42.32580"
DEC_betaUMi = "74 09 19.8142"

t_start = "21:00:00"
t_end = "00:00:00"  # The next day but SUT0 by definition should stay the same


azalt, times, = track_azalt(RA_procyon, DEC_procyon, t_start, t_end, 100, ZeroTime, AGO_lambda, AGO_phi)
az = azalt[0]
alt = azalt[1]
print(times)
# Plot style 1
# datapoints = np.array([np.deg2rad(az), alt]).T.reshape(-1, 1, 2)
datapoints = np.array([(az), alt]).T.reshape(-1, 1, 2)

segments = np.concatenate([datapoints[:-1], datapoints[1:]], axis=1)
norm = plt.Normalize(0, 360)
lc = LineCollection(segments, cmap="cmr.infinity_s", norm=norm)
lc.set_array(times)

# WARNING: POLAR PLOT TAKES X DATA IN RADIANS
# fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
# line = ax.add_collection(lc)
# ax.set_rlim(bottom=90, top=0)
# ax.set_rmax(90)
# ax.set_rticks([0, 15, 30, 45, 60, 75, 90])
# # ax.set_rlabel_position(-22.5)
# ax.set_theta_zero_location("N")
# ax.set_theta_direction(-1)
# ax.grid(True)
# plt.colorbar(line, label=r"Time $[\degree]$", pad=0.075)
# plt.title(r"Azimuth and elevation of $\beta$ UMi")
# plt.show()

# Plot style 2
fig, ax = plt.subplots()
# line = ax.add_collection(lc)
for i in range(len(az)):
    plt.scatter(az[i], alt[i], label=i)

plt.xlim(0, 360)
plt.ylim(-90, 90)
# plt.colorbar(line, label=r"Time $[\degree]$")
plt.title("Azimuth and elevation of Procyon")
plt.xlabel(r"Azimuth $[\degree]$")
plt.ylabel(r"Elevation $[\degree]$")
plt.legend()

time = "21:55:00"
r1, r2 = eq_to_hor(RA_procyon, DEC_procyon, time, ZeroTime, AGO_lambda, AGO_phi)
print(deg2dms(r1), deg2dms(r2))

# plt.show()
