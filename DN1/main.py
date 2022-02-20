import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr


def eq_to_hor(alpha, delta, jd, SUT0, lamb, phi, t_0=1):
    """
    Convert equatorial coordinates to horizontal
    INPUTS:
    :param alpha: Right ascension in DMS
    :param delta: Declination in DMS
    :param SUT0: Greenwich mean sidereal time at 0h UT
    :param jd: Time of observation in jd
    :param lamb: Observer longitude
    :param phi: Observer latitude
    :param t_0: Daylight savings

    OUTPUTS:
    :param A: Azimuth
    :param h: Elevation
    """
    alpha = dms_2_dec(alpha)
    delta = dms_2_dec(delta)
    sec = (jd % 1) * 86400  # Get decimal points
    arc_sec = 15 * sec  # Time in arc sec
    t = arc_sec/3600  # Time in degrees
    S = SUT0 + lamb + (t-t_0)*(366.2422/365.2422)
    H = S - alpha
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
    return float(t[0]) + float(t[1])/60 + float(t[2])/3600


RA_sirius = "06 46 07.6"
DEC_sirius = "-16 45 57.5"
