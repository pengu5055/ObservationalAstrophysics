import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr


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
    time = hms_2_deg(time)
    H = np.deg2rad((get_LST(time, SUT0, lamb) - hms_2_deg(alpha)) % 360)  # Warning! Alpha is given in HMS
    delta = np.deg2rad(dms_2_dec(delta))
    phi = np.deg2rad(phi)
    h = np.arcsin(np.sin(phi)*np.sin(delta) + np.cos(phi)*np.cos(delta)*np.cos(H))
    A = np.arccos((np.sin(delta)-np.sin(phi)*np.sin(h))/(np.cos(phi)*np.cos(h)))

    return np.rad2deg(A), np.rad2deg(h)


def GMST(jd):
    """
    Calculate Greenwich Mean Sidereal Time
    Input is in julian date
    """
    T = (jd - 2451545.0)/36525
    return 24110.54841 + 8640184.812866*T + 0.093104 * T**2 - 0.0000062 * T**3


def dms_2_dec(t):
    """Convert DMS to decimals. Input format DD MM SS.SS"""
    t = t.split(" ")
    if np.sign(int(t[0])) == 1 or np.sign(int(t[0])) == 0:
        return (float(t[0]) + float(t[1])/60 + float(t[2])/3600) % 360
    elif np.sign(int(t[0])) == -1:
        return (float(t[0]) - float(t[1]) / 60 - float(t[2]) / 3600) % 360
    else:
        raise ValueError("Something's fucky..")


def hms_2_deg(time):
    """Converts HMS time to degree. Input format HH:MM:SS.SS or HH MM SS.SS"""
    time = str(time)
    if time[2] == ":":
        s = time.split(":")
    elif time[2] == " ":
        s = time.split(" ")
    else:
        # raise ValueError("Unknown input format")
        return float(time)

    return ((float(s[0]) + (float(s[1]) / 60) + float(s[2]) / 3600) * 15) % 360


def get_LST(t, SUT0, lambd, t_0=15):
    """Get local star time"""
    #if not t.isnumeric():
    #   t = hms_2_deg(t)
    return (SUT0 + lambd + (t - t_0) * (366.2422 / 365.2422)) % 360


def track_azalt(alpha, delta, time_start, time_end, bins, SUT0, lamb, phi):
    """
    Track elevation and azimuth of desired star at discrete time points
    :param alpha: Right ascension of star
    :param delta: Declination of star
    :param time_start: Time of observation start in HMS
    :param time_end: Time of observation end in HMS
    :param bins: Discrete divisions of time interval
    :param SUT0: Greenwich sidereal time at 0h UT
    :param lamb: Observer longitude
    :param phi: Observer latitude
    :return: 2D array with Azimuth and elevation and 1D array of times
    """
    time_start = hms_2_deg(time_start)
    time_end = hms_2_deg(time_end)
    times = np.linspace(time_start, time_end, bins)
    output = []
    for time in times:
        output.append(eq_to_hor(alpha, delta, time, SUT0, lamb, phi))

    return np.column_stack(np.array(output)), times


# ----Observatory Data----
obstime = "18:50:05"
AGO_lambda = 14.5277
AGO_phi = 46.0439
ZeroTime = 149.912405

# ----Test with Cartes du Ciel----
RA_sirius = "06 46 07.6"
DEC_sirius = "-16 45 57.5"
RA_rigel = "05 15 35.9"
DEC_rigel = "-08 20 44.8"

# print(eq_to_hor(RA_rigel, DEC_rigel, obstime, ZeroTime, AGO_lambda, AGO_phi))
# print(eq_to_hor(RA_sirius, DEC_sirius, obstime, ZeroTime, AGO_lambda, AGO_phi))

# ----Tracking two stars----
RA_procyon = "07 39 18.11950"
DEC_procyon = "05 13 29.9552"
RA_betaUMi = ""
DEC_betaUMi = ""

t_start = "18:00:00"
t_end = "05:00:00"  # The next day but SUT0 by definition should stay the same

azalt, times, = track_azalt(RA_procyon, DEC_procyon, t_start, t_end, 200, ZeroTime, AGO_lambda, AGO_phi)
az = azalt[0]
alt = azalt[1]


fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(times, az)
ax1.set_xlabel(r"Time $[\degree]$")
ax1.set_ylabel(r"Azimuth $[\degree]$")

ax2.plot(times, alt)
ax2.set_xlabel(r"Time $[\degree]$")
ax2.set_ylabel(r"Elevation $[\degree]$")

plt.suptitle("Azimuth and Elevation of Procyon")
plt.subplots_adjust(hspace=0.34)
plt.show()
