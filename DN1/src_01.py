import numpy as np


def eq_to_hor(alpha, delta, time, SUT0, lamb, phi):
    """
    Convert equatorial coordinates to horizontal
    INPUTS:
    :param alpha: Right ascension in HMS
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
    delta = np.deg2rad(dms2deg(delta))
    phi = np.deg2rad(phi)
    h = np.arcsin(np.sin(phi)*np.sin(delta) + np.cos(phi)*np.cos(delta)*np.cos(H))
    # A = np.arccos((np.sin(delta)-np.sin(phi)*np.sin(h))/(np.cos(phi)*np.cos(h)))
    A = (np.arcsin(-np.sin(H)*np.sin(delta)/np.cos(h)))

    return np.rad2deg(A), np.rad2deg(h)


def eq2azalt(alpha, delta, time, SUT0, lamb, phi):
    """
    Convert equatorial coordinates to horizontal
    INPUTS:
    :param alpha: Right ascension in deg
    :param delta: Declination in deg
    :param SUT0: Greenwich mean sidereal time at 0h UT in deg
    :param time: Time of observation in HH:MM:SS
    :param lamb: Observer longitude in deg
    :param phi: Observer latitude in deg

    OUTPUTS:
    :return A: Azimuth
    :return h: Elevation
    """
    H = np.deg2rad((get_LST(time, SUT0, lamb) - alpha) % 360)
    delta = np.deg2rad(delta)
    phi = np.deg2rad(phi)
    h = np.arcsin(np.sin(phi)*np.sin(delta) + np.cos(phi)*np.cos(delta)*np.cos(H))
    A = np.arccos((np.sin(delta)-np.sin(phi)*np.sin(h))/(np.cos(phi)*np.cos(h)))
    # A = (np.arcsin(-np.sin(H)*np.sin(delta)/np.cos(h)))

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

    return ((float(s[0]) + (float(s[1]) / 60) + float(s[2]) / 3600) * 15) % 360


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


def GMST(jd):
    """Calculate GMST 0h UT from julian date"""
    T_u = (jd - 2451545.0)/36525
    unit = 0.00416  # Seconds of time, to degrees in decimal
    res = 24110.54841 + 8640184.812866 * T_u + 0.093104 * T_u**2 - 6.2E-06 * T_u**3
    return res*unit


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
    time_start = hms2deg(time_start) + 180
    time_end = hms2deg(time_end) + 180
    times = list(crange(time_start, time_end, 360, bins))
    output = []
    for time in times:
        time = deg2hms(time)  # Hacky fix the fact that eq_to_hor takes HMS time (and instantly converts it into deg)
        output.append(eq_to_hor(alpha, delta, time, SUT0, lamb, phi))

    return np.column_stack(np.array(output)), np.array(list(times))


def crange2(start, end, modulo, bin):
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


def crange3(start, end, modulo, bin):
    """Generator of circular range"""
    return np.linspace(start, end + modulo, bin) % modulo


def crange(start, end, modulo, bin):
    return np.linspace(start, end + modulo, bin)
