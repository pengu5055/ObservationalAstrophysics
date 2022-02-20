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
    :param A: Azimuth
    :param h: Elevation
    """
    alpha = hms_2_deg(alpha)  # Warning! Alpha is given in HMS
    delta = dms_2_dec(delta)
    H = get_LST(time, SUT0, lamb) - alpha
    h = np.arcsin(np.sin(phi)*np.sin(delta)+np.cos(phi)*np.cos(delta)*np.cos(H))
    A = np.arcsin(- (np.sin(H)*np.cos(delta))/np.cos(h))

    return A, h


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
    if time[2] == ":":
        s = time.split(":")
    elif time[2] == " ":
        s = time.split(" ")
    else:
        raise ValueError("Unknown input format")

    return ((float(s[0]) + (float(s[1]) / 60) + float(s[2]) / 3600) * 15) % 360


def get_LST(t, SUT0, lambd, t_0=15):
    """Get local star time"""
    t = hms_2_deg(t)
    return (SUT0 + lambd + (t - t_0) * (366.2422 / 365.2422)) % 360


# ----Observatory Data----
obstime = "18:50:05"
AGO_lambda = 14.5277
AGO_phi = 46.0439
ZeroTime = 149.912405


RA_sirius = "06 46 07.6"
DEC_sirius = "-16 45 57.5"
RA_rigel = "05 15 35.9"
DEC_rigel = "-08 20 44.8"

print(eq_to_hor(RA_rigel, DEC_rigel, obstime, ZeroTime, AGO_lambda, AGO_phi))